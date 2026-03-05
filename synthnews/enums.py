from enum import Enum


class DocumentRejectionReason(Enum):
    TOO_SHORT = ("too_short",)
    TOO_SIMILAR = "too_similar"
