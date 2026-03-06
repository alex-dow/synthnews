from enum import StrEnum


class DocumentRejectionReason(StrEnum):
    TOO_SHORT = "too_short"
    TOO_SIMILAR = "too_similar"
    INVALID_PLAN = "invalid_plan"
    UNKNOWN_ERROR = "unknown_error"
