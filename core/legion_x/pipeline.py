from __future__ import annotations

import hashlib
import json
import sqlite3
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path


CHARACTERS = {
    "minku": "a naughty but kind baby elephant",
    "chiku": "a brave little chick",
    "bobo": "a tiny construction worker",
}

IDEAS = (
    ("cartoon", "Minku saves a puppy from the rain", "A tiny umbrella flies away!"),
    ("tiny_world", "Bobo repairs a broken toy car", "The giant wheel starts rolling!"),
    ("cartoon", "Chiku returns a lost glowing star", "A star falls into Chiku's nest!"),
)


@dataclass(frozen=True)
class ContentPackage:
    content_id: str
    character: str
    category: str
    story: str
    hook: str
    scenes: list[dict[str, str]]
    title: str
    caption: str
    status: str
    qa_score: int
    qa_reasons: list[str]
    created_at: str


@dataclass(frozen=True)
class MediaReview:
    decision: str
    score: int
    reasons: list[str]


def oracle(seed: str) -> dict[str, str]:
    """Select an idea deterministically so local runs are reproducible."""
    index = int(hashlib.sha256(seed.encode()).hexdigest(), 16) % len(IDEAS)
    category, story, hook = IDEAS[index]
    character = story.split()[0].lower()
    return {"character": character, "category": category, "story": story, "hook": hook}


def scripter(idea: dict[str, str]) -> dict[str, object]:
    hero = idea["character"].title()
    scenes = [
        {"time": "0-2", "beat": "hook", "visual": idea["hook"]},
        {"time": "2-7", "beat": "problem", "visual": f"{hero} notices a friend needs help."},
        {"time": "7-15", "beat": "escalation", "visual": f"{hero} tries a clever but funny solution."},
        {"time": "15-22", "beat": "payoff", "visual": "The problem is solved with a warm surprise."},
        {"time": "22-25", "beat": "loop", "visual": "The opening movement begins again naturally."},
    ]
    return {
        **idea,
        "scenes": scenes,
        "title": f"{hero}'s Tiny Rescue",
        "caption": f"Can {hero} save the day? #Shorts #FamilyFriendly #OriginalStory",
    }


def guardian(package: dict[str, object]) -> tuple[int, list[str]]:
    score = 100
    reasons: list[str] = []
    if len(str(package.get("hook", "")).strip()) < 10:
        score -= 25
        reasons.append("hook_too_weak")
    scenes = package.get("scenes", [])
    if not isinstance(scenes, list) or len(scenes) != 5:
        score -= 30
        reasons.append("invalid_story_structure")
    if str(package.get("character", "")) not in CHARACTERS:
        score -= 20
        reasons.append("unknown_character")
    if not str(package.get("caption", "")).strip():
        score -= 15
        reasons.append("missing_caption")
    return max(score, 0), reasons


def guardian_media(metadata: dict[str, object]) -> MediaReview:
    """Block uncompetitive video outputs before publishing.

    This is intentionally stricter than the early story check. A reel may have
    a good script but still be rejected for being static, silent, watermarked,
    or missing a first-two-second visual pattern break.
    """
    score = 100
    reasons: list[str] = []
    required_true = {
        "has_real_motion": "static_or_insufficient_motion",
        "has_voiceover": "missing_voiceover",
        "has_licensed_music_or_sfx": "missing_sound_design",
        "has_first_two_second_pattern_break": "weak_opening_hook",
        "has_subtitles": "missing_subtitles",
        "is_1080x1920": "incorrect_output_format",
    }
    for field, reason in required_true.items():
        if metadata.get(field) is not True:
            score -= 18
            reasons.append(reason)
    if metadata.get("has_provider_watermark") is True:
        score = 0
        reasons.append("provider_watermark")
    if float(metadata.get("average_shot_length_seconds", 99)) > 2.5:
        score -= 15
        reasons.append("slow_edit_pacing")
    if int(metadata.get("distinct_visual_beats", 0)) < 8:
        score -= 15
        reasons.append("insufficient_visual_beats")
    decision = "APPROVED" if score >= 85 and not reasons else "REJECTED"
    return MediaReview(decision=decision, score=max(score, 0), reasons=reasons)


def init_database(path: Path) -> sqlite3.Connection:
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path)
    connection.execute(
        """CREATE TABLE IF NOT EXISTS content (
        content_id TEXT PRIMARY KEY, character TEXT, category TEXT, story TEXT,
        hook TEXT, package_json TEXT, status TEXT, qa_score INTEGER, created_at TEXT
        )"""
    )
    return connection


def run_pipeline(seed: str, database_path: str | Path) -> ContentPackage:
    drafted = scripter(oracle(seed))
    score, reasons = guardian(drafted)
    status = "APPROVED" if score >= 80 else "MANUAL_REVIEW"
    digest = hashlib.sha256(json.dumps(drafted, sort_keys=True).encode()).hexdigest()[:12]
    result = ContentPackage(
        content_id=f"LX-{digest}", status=status, qa_score=score,
        qa_reasons=reasons, created_at=datetime.now(timezone.utc).isoformat(), **drafted
    )
    connection = init_database(Path(database_path))
    with connection:
        connection.execute(
            "INSERT OR REPLACE INTO content VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (result.content_id, result.character, result.category, result.story,
             result.hook, json.dumps(asdict(result)), result.status,
             result.qa_score, result.created_at),
        )
    connection.close()
    return result
