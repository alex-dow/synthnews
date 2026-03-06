from synthnews.enums import DocumentRejectionReason


class RejectionError(Exception):
    reason: DocumentRejectionReason

    def __init__(self, message: str, reason: DocumentRejectionReason):
        super().__init__(message)
        self.reason = reason


class ModelNotFoundError(Exception):
    def __init__(self, model_path: str):
        super().__init__(f"Model file not found: {model_path}")


class TopicNotFoundError(Exception):
    topic: str

    def __init__(self, topic: str, message: str):
        super().__init__(message)
        self.topic = topic


class InvalidPlanError(Exception):
    plan: str

    def __init__(self, message: str, plan: str):
        super().__init__(message)
        self.plan = plan
