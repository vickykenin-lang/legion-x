# LEGION-X Architecture

## Command Flow

1. **Oracle** reads historical performance and proposes ideas.
2. **Scripter** converts selected ideas into hooks, scripts, scenes, and prompts.
3. **Forge** generates or gathers approved assets and assembles vertical MP4 output.
4. **Guardian** runs technical and content checks.
5. **Flash** queues approved reels for platform publishing.
6. **Vision** collects metrics and calculates performance scores.
7. **Phoenix** produces meaningful variations from proven winners.

## Free-First Stack

| Layer | Initial choice | Fallback |
| --- | --- | --- |
| Orchestration | n8n Community Edition | Local scheduled scripts |
| Database | SQLite | CSV/Google Sheets |
| Text intelligence | Local/open model | Legitimate free tier |
| Visual production | Local/open tools | Free tier or still-image animation |
| Editing | FFmpeg | None required |
| Voice | Local TTS | Licensed free-tier voice |
| Subtitles | Script-derived SRT | Local speech recognition |
| Source control | Private GitHub repository | Local Git mirror |
| Media storage | Local/approved drive | Object storage after validation |

## Content State Machine

`IDEA → SCORED → SCRIPTED → ASSETS_READY → ASSEMBLED → QA_PENDING → APPROVED → QUEUED → PUBLISHED → MEASURED`

Failure states:

- `MANUAL_REVIEW`
- `REJECTED`
- `RETRYABLE_ERROR`
- `PERMANENT_ERROR`

## Guardian Gate

Publishing is prohibited unless all mandatory checks pass:

- 1080 × 1920, 9:16
- 15–30 seconds
- Audio present and normalized
- No blank/corrupt ending
- Subtitle safe area
- Clear first-two-second hook
- Story clarity and character consistency
- No unwanted watermark or duplicate storyline
- Family-friendly and sufficiently original
- Platform-policy classification recorded

## Performance Score

Initial formula:

`30% retention + 20% completion/rewatch + 20% shares + 10% comments + 10% likes + 10% followers generated`

Thresholds will be calibrated using real data.
