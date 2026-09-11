"""Recover the Clips Collection videos from the Internet Archive.

Uses the standard library and curl. Run from any directory with Python 3.
Successful downloads are reused on subsequent runs; the site is not modified.
"""

import csv
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import shutil
import subprocess
import time
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "recovered-gfycat"
CURL = shutil.which("curl.exe") or shutil.which("curl")
LAST_REQUEST = 0.0
RATE_LIMITS = 0


def save_report(report):
    temporary = OUTPUT / "recovery-report.json.tmp"
    temporary.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(OUTPUT / "recovery-report.json")


def fetch(original_url, destination):
    global LAST_REQUEST, RATE_LIMITS
    if urlsplit(original_url).hostname not in {
        "api.gfycat.com", "giant.gfycat.com", "thumbs.gfycat.com", "gfycat.com"
    }:
        raise ValueError("Unexpected media host")
    archived_url = "https://web.archive.org/web/0id_/" + original_url
    for attempt in range(3):
        time.sleep(max(0, 1.5 - (time.monotonic() - LAST_REQUEST)))
        result = subprocess.run(
            [CURL, "--silent", "--show-error", "--location", "--max-redirs", "8",
             "--connect-timeout", "10", "--max-time", "120",
             "--output", str(destination), "--write-out",
             "%{http_code}\t%{content_type}\t%{url_effective}", archived_url],
            capture_output=True, text=True,
        )
        LAST_REQUEST = time.monotonic()
        parts = result.stdout.strip().split("\t", 2)
        status = int(parts[0]) if parts and parts[0].isdigit() else 0
        response = {
            "original_url": original_url, "archive_url": parts[2] if len(parts) > 2 else archived_url,
            "http_status": status, "content_type": parts[1] if len(parts) > 1 else "",
            "curl_exit_code": result.returncode,
        }
        if result.stderr:
            response["error"] = result.stderr.strip()
        if status == 429:
            RATE_LIMITS += 1
            if RATE_LIMITS >= 3:
                raise RuntimeError("Internet Archive rate limit persisted; stopped for a later retry.")
            print("Archive rate limit; pausing for 45 seconds before retrying.", flush=True)
            time.sleep(45)
            continue
        RATE_LIMITS = 0
        if (result.returncode or status in {500, 502, 503, 504}) and attempt < 2:
            time.sleep(5 * (attempt + 1))
            continue
        return response
    return response


def container_type(path):
    with path.open("rb") as stream:
        header = stream.read(16)
    if len(header) >= 12 and header[4:8] == b"ftyp":
        return "mp4"
    if header[:4] == b"\x1aE\xdf\xa3":
        return "webm"
    return None


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    if not CURL:
        raise RuntimeError("curl is required")
    OUTPUT.mkdir(exist_ok=True)
    (OUTPUT / "videos").mkdir(exist_ok=True)
    (OUTPUT / "metadata").mkdir(exist_ok=True)
    with (ROOT / "clips-collection-gfycat-links.csv").open(encoding="utf-8-sig", newline="") as stream:
        references = list(csv.DictReader(stream))
    clips = {}
    for row in references:
        clip_id = urlsplit(row["gfycat_url"]).path.strip("/")
        if not re.fullmatch(r"[A-Za-z]+", clip_id):
            raise ValueError(f"Unexpected clip ID: {clip_id}")
        clips.setdefault(clip_id.lower(), {"id": clip_id, "sections": []})["sections"].append(row["section"])
    previous = {}
    report_path = OUTPUT / "recovery-report.json"
    if report_path.exists():
        previous = {item["id"].lower(): item for item in json.loads(report_path.read_text(encoding="utf-8"))["clips"]}
    report = {"source": "clips-collection-gfycat-links.csv", "reference_count": len(references),
              "unique_clip_count": len(clips), "clips": [], "complete": False}
    for ordinal, (key, clip) in enumerate(clips.items(), 1):
        old = previous.get(key)
        if old and old.get("status") == "recovered":
            saved = OUTPUT / old["file"]
            if saved.is_file() and sha256(saved) == old["sha256"]:
                report["clips"].append(old)
                print(f"[{ordinal}/{len(clips)}] Reusing {saved.name}", flush=True)
                continue
        entry = {**clip, "status": "checking", "attempts": []}
        report["clips"].append(entry)
        save_report(report)
        print(f"[{ordinal}/{len(clips)}] {clip['id']}", flush=True)
        metadata_path = OUTPUT / "metadata" / f"{key}.json"
        metadata = None
        if metadata_path.exists():
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        try:
            if metadata is None:
                temporary = OUTPUT / "metadata" / f"{key}.part"
                response = fetch(f"https://api.gfycat.com/v1/gfycats/{key}", temporary)
                entry["attempts"].append(response)
                if response["http_status"] == 200 and response["curl_exit_code"] == 0:
                    try:
                        candidate = json.loads(temporary.read_text(encoding="utf-8"))
                        if str(candidate.get("gfyItem", {}).get("gfyId", "")).lower() == key:
                            metadata = candidate
                            temporary.replace(metadata_path)
                    except (ValueError, UnicodeError):
                        pass
                temporary.unlink(missing_ok=True)
            item = (metadata or {}).get("gfyItem", {})
            name = item.get("gfyName") or clip["id"]
            if not re.fullmatch(r"[A-Za-z]+", name):
                raise ValueError("Unexpected archived filename")
            entry["canonical_id"] = name
            entry["title"] = item.get("title", "")
            entry["metadata_file"] = f"metadata/{key}.json" if metadata else None
            content = item.get("content_urls", {})
            variants = [
                ("mp4", item.get("mp4Url") or f"https://giant.gfycat.com/{name}.mp4"),
                ("webm", item.get("webmUrl") or f"https://giant.gfycat.com/{name}.webm"),
                ("mobile", item.get("mobileUrl") or f"https://thumbs.gfycat.com/{name}-mobile.mp4"),
            ]
            for variant, original in variants:
                temporary = OUTPUT / "videos" / f"{name}-{variant}.part"
                response = fetch(original, temporary)
                response["variant"] = variant
                entry["attempts"].append(response)
                detected = container_type(temporary) if temporary.exists() else None
                if response["http_status"] == 200 and response["curl_exit_code"] == 0 and detected:
                    destination = OUTPUT / "videos" / f"{name}{'-mobile' if variant == 'mobile' else ''}.{detected}"
                    temporary.replace(destination)
                    details = content.get(variant, {})
                    entry.update({
                        "status": "recovered", "variant": variant,
                        "file": destination.relative_to(OUTPUT).as_posix(),
                        "bytes": destination.stat().st_size, "sha256": sha256(destination),
                        "archive_url": response["archive_url"],
                        "archived_width": details.get("width"), "archived_height": details.get("height"),
                        "archived_size": details.get("size"),
                    })
                    print(f"  Recovered {variant}: {destination.stat().st_size:,} bytes", flush=True)
                    break
                temporary.unlink(missing_ok=True)
                print(f"  {variant}: HTTP {response['http_status']}", flush=True)
                save_report(report)
            if entry["status"] != "recovered":
                entry["status"] = "not_recovered"
        except RuntimeError as error:
            entry.update({"status": "retry_needed", "error": str(error)})
            report["stopped_reason"] = str(error)
            save_report(report)
            print(str(error), flush=True)
            break
        save_report(report)
    else:
        report["complete"] = True
    report["recovered_count"] = sum(item["status"] == "recovered" for item in report["clips"])
    save_report(report)
    print(json.dumps({"recovered": report["recovered_count"], "total": len(clips),
                      "complete": report["complete"], "output": str(OUTPUT)}), flush=True)
    print("Optional video inspection libraries:",
          {name: importlib.util.find_spec(name) is not None for name in ["av", "cv2"]}, flush=True)


if __name__ == "__main__":
    main()
