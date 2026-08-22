# MoneyPrinterTurbo v1.3.4 Reuse Assessment

## Live evaluation

Two videos were generated during the evaluation. The relevant topic-based test
used five local illustrations and produced a 24.7-second, 1080x1920 H.264/AAC
video with automatic image zoom, subtitle timing, background music, and final
assembly. The technical pipeline completed, but the creative result was rejected.

Microsoft Edge TTS timed out during the live environment test. A no-voice fallback
completed the render, proving that network-dependent voice services require a
provider fallback and a QA gate.

## Upstream components worth referencing

| Upstream area | Reusable idea | LEGION-X owner |
| --- | --- | --- |
| `app/services/video.py` | FFmpeg/MoviePy assembly, resizing, image-to-clip conversion | Forge |
| `app/services/voice.py` | Pluggable TTS and subtitle timing | Forge |
| `app/services/material.py` | Local/stock material provider boundary | Forge |
| `app/models/llm_provider.py` | Provider registry instead of hard-coded LLM | Oracle/Scripter |
| `app/controllers/manager/` | Bounded concurrent task queue | Victor/Forge |
| `app/services/state.py` | Memory/Redis task-state abstraction | Victor |
| `app/services/upload_post.py` | Publisher adapter concept | Flash |
| `app/services/llm.py` social metadata | Title/caption/hashtag output contract | Flash |

## Important upstream risks

1. API authentication is not enabled by default in the evaluated controller.
2. Default task state is in-memory and disappears after a process restart.
3. Cross-platform publishing is process-thread based and interrupted jobs do not
   resume after restart.
4. Auto-upload occurs after rendering and does not implement LEGION-X's Guardian
   plus Human Approval requirement.
5. Fixed character identity, emotional storytelling, originality scoring,
   performance learning, and revenue feedback are not solved.
6. Bundled music must not be assumed copyright-safe.

## Reuse rule

Do not copy the upstream repository wholesale. Reimplement only a required
interface after a real LEGION-X test proves that the component improves quality,
reliability, or cost.

## Upstream attribution

Project: MoneyPrinterTurbo by Harry

Source: https://github.com/harry0703/MoneyPrinterTurbo

License: MIT

