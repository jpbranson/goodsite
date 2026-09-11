"""Apply verified Streamable upload IDs to both versions of Clips Collection.

Usage: python scripts/apply_streamable_embeds.py
Populate recovered-gfycat/streamable-uploads.json after uploading the clips.
Both files are validated before either is changed. The original CSV remains
the record of the Gfycat links.
"""

import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
MAPPING = ROOT / 'recovered-gfycat' / 'streamable-uploads.json'
SOURCE = ROOT / 'content/post/Clips-Collection.Rmd'
HTML = ROOT / 'content/post/Clips-Collection.html'


def main():
    entries = json.loads(MAPPING.read_text(encoding='utf-8'))['clips']
    clips = {}
    for entry in entries:
        shortcode = entry.get('streamable_id')
        if not isinstance(shortcode, str) or not re.fullmatch(r'[A-Za-z0-9]+', shortcode):
            raise ValueError(f"Upload ID is missing or invalid for {entry['gfycat_id']}")
        if entry.get('status') != 'ready':
            raise ValueError(f"Streamable processing is not verified for {entry['gfycat_id']}")
        if not (isinstance(entry['width'], int) and entry['width'] > 0
                and isinstance(entry['height'], int) and entry['height'] > 0):
            raise ValueError('Video dimensions must be positive integers')
        key = entry['gfycat_id'].lower()
        if key in clips:
            raise ValueError(f'Duplicate mapping: {key}')
        clips[key] = entry
    source = SOURCE.read_bytes().decode('utf-8')
    html = HTML.read_bytes().decode('utf-8')
    rmd_pattern = re.compile(r"blogdown::shortcode_html\('gfycat',\s*'([^']+)'\)")
    html_pattern = re.compile(r'{{<\s*gfycat\s+"([^"]+)"\s*>}}')
    source_ids = [match.group(1).lower() for match in rmd_pattern.finditer(source)]
    html_ids = [match.group(1).lower() for match in html_pattern.finditer(html)]
    if source_ids != html_ids or len(source_ids) != 26 or set(source_ids) != set(clips):
        raise ValueError('Expected the same 26 Gfycat references in source and HTML, mapped to all 25 uploads')

    def rmd_embed(match):
        item = clips[match.group(1).lower()]
        return (f"blogdown::shortcode_html('streamable', '{item['streamable_id']}', "
                f"{item['width']}, {item['height']})")

    def html_embed(match):
        item = clips[match.group(1).lower()]
        return ('{{< streamable "' + item['streamable_id'] + '" "' + str(item['width'])
                + '" "' + str(item['height']) + '" >}}')

    updated_source = rmd_pattern.sub(rmd_embed, source)
    updated_html = html_pattern.sub(html_embed, html)
    if len(re.findall(r"shortcode_html\('streamable'", updated_source)) != 26:
        raise ValueError('Incorrect replacement count')
    SOURCE.write_bytes(updated_source.encode('utf-8'))
    HTML.write_bytes(updated_html.encode('utf-8'))
    print('Replaced 26 embeds in each file using 25 verified Streamable uploads.')


if __name__ == '__main__':
    main()
