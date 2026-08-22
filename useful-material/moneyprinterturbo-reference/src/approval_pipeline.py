"""Approval-safe state transitions for LEGION-X video jobs.

Rendering completion never authorizes publishing. Guardian QA and explicit human
approval are independent gates.
"""

from enum import StrEnum


class VideoState(StrEnum):
    DRAFT = "draft"
    RENDERING = "rendering"
    QA_PENDING = "qa_pending"
    QA_REJECTED = "qa_rejected"
    APPROVAL_PENDING = "approval_pending"
    APPROVED = "approved"
    POST_PENDING = "post_pending"
    POSTING = "posting"
    POSTED = "posted"
    POST_FAILED = "post_failed"


ALLOWED_TRANSITIONS: dict[VideoState, set[VideoState]] = {
    VideoState.DRAFT: {VideoState.RENDERING},
    VideoState.RENDERING: {VideoState.QA_PENDING},
    VideoState.QA_PENDING: {VideoState.QA_REJECTED, VideoState.APPROVAL_PENDING},
    VideoState.QA_REJECTED: {VideoState.DRAFT},
    VideoState.APPROVAL_PENDING: {VideoState.APPROVED, VideoState.QA_REJECTED},
    VideoState.APPROVED: {VideoState.POST_PENDING},
    VideoState.POST_PENDING: {VideoState.POSTING},
    VideoState.POSTING: {VideoState.POSTED, VideoState.POST_FAILED},
    VideoState.POST_FAILED: {VideoState.POST_PENDING},
    VideoState.POSTED: set(),
}


def transition(current: VideoState, requested: VideoState) -> VideoState:
    """Return the requested state only when the transition is explicitly safe."""
    if requested not in ALLOWED_TRANSITIONS[current]:
        raise ValueError(f"unsafe video state transition: {current} -> {requested}")
    return requested


def may_publish(state: VideoState, guardian_passed: bool, human_approved: bool) -> bool:
    """Publishing requires both independent approvals and the correct state."""
    return state in {VideoState.APPROVED, VideoState.POST_PENDING} and guardian_passed and human_approved

