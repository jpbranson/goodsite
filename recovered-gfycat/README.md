# Recovered Clips Collection videos

Recovered **25 of 25 unique clips** (26 references in the post). Total size: **234.4 MiB**.

Formats: 10 full-size MP4, 0 full-size WebM, 15 mobile MP4 copies.

The mobile copies have lower resolution. These are archived Gfycat encodes; they are not guaranteed to be the exact files originally uploaded.

**Verification:** every recovered file was inspected and fully decoded with FFmpeg/ffprobe. All files passed.

The download pass tried full-size MP4, then WebM, then mobile MP4. Archived API metadata supplied the original filenames. The JSON report records capture URLs, attempts, byte counts, SHA-256 hashes, metadata, and verification results.

## Files

| Clip | Copy | Resolution | Duration |
| --- | --- | --- | --- |
| [LeanUnevenBull](videos/LeanUnevenBull-mobile.mp4) | Mobile MP4 | 640 × 332 | 36.0 s |
| [UntriedSphericalAmazondolphin](videos/UntriedSphericalAmazondolphin-mobile.mp4) | Mobile MP4 | 640 × 332 | 25.8 s |
| [SmugSpiffyDegu](videos/SmugSpiffyDegu-mobile.mp4) | Mobile MP4 | 640 × 332 | 12.2 s |
| [AgedDimpledAmethystinepython](videos/AgedDimpledAmethystinepython.mp4) | MP4 | 2496 × 1292 | 8.2 s |
| [SillyTestyGraysquirrel](videos/SillyTestyGraysquirrel-mobile.mp4) | Mobile MP4 | 640 × 332 | 12.4 s |
| [AdeptCalmAlaskankleekai](videos/AdeptCalmAlaskankleekai.mp4) | MP4 | 2496 × 1292 | 37.2 s |
| [AgreeableAncientConure](videos/AgreeableAncientConure.mp4) | MP4 | 2496 × 1292 | 17.1 s |
| [BogusSharpIzuthrush](videos/BogusSharpIzuthrush.mp4) | MP4 | 2496 × 1292 | 11.8 s |
| [DistortedJealousBlackrhino](videos/DistortedJealousBlackrhino.mp4) | MP4 | 2496 × 1292 | 5.3 s |
| [RemoteSilentIsabellineshrike](videos/RemoteSilentIsabellineshrike-mobile.mp4) | Mobile MP4 | 640 × 332 | 5.3 s |
| [IllOpulentGuineapig](videos/IllOpulentGuineapig-mobile.mp4) | Mobile MP4 | 640 × 332 | 11.6 s |
| [TalkativeSpecificArabianwildcat](videos/TalkativeSpecificArabianwildcat.mp4) | MP4 | 2496 × 1292 | 7.5 s |
| [WeeklyUltimateAmethystgemclam](videos/WeeklyUltimateAmethystgemclam-mobile.mp4) | Mobile MP4 | 640 × 332 | 21.1 s |
| [FrequentEnragedBelugawhale](videos/FrequentEnragedBelugawhale.mp4) | MP4 | 2292 × 1210 | 18.1 s |
| [WindingPoliteIvorygull](videos/WindingPoliteIvorygull-mobile.mp4) | Mobile MP4 | 640 × 348 | 28.5 s |
| [BareFrighteningIbisbill](videos/BareFrighteningIbisbill.mp4) | MP4 | 2784 × 1418 | 16.2 s |
| [ZealousFastBullfrog](videos/ZealousFastBullfrog-mobile.mp4) | Mobile MP4 | 640 × 326 | 12.2 s |
| [SnivelingUnsightlyFlicker](videos/SnivelingUnsightlyFlicker.mp4) | MP4 | 1280 × 720 | 34.5 s |
| [DearPleasedIraniangroundjay](videos/DearPleasedIraniangroundjay-mobile.mp4) | Mobile MP4 | 640 × 360 | 10.7 s |
| [SneakyOddballBuck](videos/SneakyOddballBuck-mobile.mp4) | Mobile MP4 | 640 × 360 | 16.7 s |
| [AgedFrighteningLark](videos/AgedFrighteningLark-mobile.mp4) | Mobile MP4 | 640 × 360 | 10.7 s |
| [ParallelThickAntlion](videos/ParallelThickAntlion-mobile.mp4) | Mobile MP4 | 640 × 360 | 6.2 s |
| [OrderlyCandidGrub](videos/OrderlyCandidGrub-mobile.mp4) | Mobile MP4 | 640 × 360 | 12.7 s |
| [EnragedFluidFennecfox](videos/EnragedFluidFennecfox.mp4) | MP4 | 1280 × 720 | 23.7 s |
| [NeglectedNippyBarracuda](videos/NeglectedNippyBarracuda-mobile.mp4) | Mobile MP4 | 640 × 356 | 22.9 s |

The repeated `WeeklyUltimateAmethystgemclam` link is downloaded once. Both post sections are recorded in `recovery-report.json`.

Videos are in `videos/`; archived clip metadata is in `metadata/`.
The `videos/` directory is a local backup and is excluded from Git because of
its size. The file links above work after recovering the videos locally; keep
an additional backup outside this repository.

## Streamable uploads

All 25 recovered clips have been uploaded to Streamable. Processing was verified
in the dashboard for every clip, and playback was checked for
[LeanUnevenBull](https://streamable.com/qzqs2f).

`streamable-uploads.json` maps each original Gfycat ID and local filename to its
new Streamable ID. The share URL is `https://streamable.com/` followed by that ID.
Both `content/post/Clips-Collection.Rmd` and its generated `.html` now use the
responsive `streamable` shortcode in all 26 original positions. The repeated
`WeeklyUltimateAmethystgemclam` reference shares one upload in both locations.

The source replacements were applied with `scripts/apply_streamable_embeds.py`.
That migration requires all 25 uploads to be verified and the original 26 Gfycat
references to be present; it does not need to be run again. The original link
CSV and recovered video files remain available as a backup.

To repeat the recovery pass, run `python scripts/recover_gfycat.py` from the repository. Existing successful downloads are checked by hash and reused.
