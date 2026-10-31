# Repository Guidelines

## Project Structure & Module Organization

This project collects Vietnamese FAM Trading livestream transcripts for a planned BTC analysis bot. `DESIGN.md` records the intended behavior, evaluation approach, and unresolved decisions; consult it before changing scope. The bot itself is not implemented yet.

- `cong_cu/lay_transcript.py`: Python downloader, subtitle converter, and Whisper fallback.
- `transcripts/phu_de/`: YouTube subtitles and converted text.
- `transcripts/whisper/`: generated Whisper output, created when needed.
- `transcripts/_cu/`: legacy transcript archive.
- `transcripts/danh_sach.tsv`: processing index keyed by video ID.

## Build, Test, and Development Commands

Run from the repository root. Prefix shell commands with `rtk`, as required by `/Users/badat/.codex/RTK.md`; use `rtk proxy` for unfiltered execution.

- `rtk proxy python3 cong_cu/lay_transcript.py --help`: inspect CLI options without downloading.
- `rtk proxy python3 cong_cu/lay_transcript.py --them 1`: stop after fetching one new video (subtitles or queued for Whisper); it still contacts YouTube, updates files, and then runs any pending Whisper jobs.
- `rtk proxy python3 cong_cu/lay_transcript.py --tu-ngay YYYY-MM-DD`: collect back to a different cutoff (default `2026-09-16`).
- `rtk proxy python3 cong_cu/lay_transcript.py --chuyen-lai`: offline; rebuild `.txt` from existing `.vtt` without contacting YouTube.
- `rtk proxy python3 cong_cu/lay_transcript.py`: collect transcripts back to the configured cutoff and process pending Whisper jobs.
- Options are exactly those printed by `--help` (`--tu-ngay`, `--them`, `--chuyen-lai`); there is no `--toi-da` flag (fixed 31/10).
- `rtk proxy python3 -m py_compile cong_cu/lay_transcript.py`: check Python syntax.

There is no build system or dependency manifest. Install `yt-dlp`, `ffmpeg`, and `whisper-cli` separately. Whisper expects the model and VAD files configured under `~/.cache/whisper/` in the script.

## Coding Style & Naming Conventions

Use four-space Python indentation, `snake_case` functions and variables, and uppercase constants. Follow the existing Vietnamese identifiers, comments, and documentation. Preserve UTF-8 text and the TSV column schema. Transcript pairs use `YYYY-MM-DD_HHMM_VIDEOID.txt` and `.vtt`, with timestamps in Vietnam time (UTC+7). No formatter or linter is configured.

## Testing Guidelines

No automated test suite or coverage threshold exists. For script changes, run the syntax and help checks above. Validate conversion changes with a local VTT sample, checking timestamp removal, adjacent duplicate suppression, and Vietnamese text preservation. Verify TSV round trips and video-ID skipping when changing index handling. Keep routine validation offline; use bounded downloads deliberately.

## Commit & Pull Request Guidelines

The Git repository has no commits, so no established message convention exists. Use short, imperative subjects such as `Fix duplicate subtitle handling`. Keep code and bulk transcript imports in separate commits. PRs should describe behavior changes, validation performed, and any transcript or TSV changes; link relevant issues when available.

## Collection Constraints

Preserve the 60-second YouTube request spacing, stop-on-block behavior, and Whisper `--vad` option. Keep raw subtitle provenance and the legacy archive intact.
