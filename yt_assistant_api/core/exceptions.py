from fastapi import HTTPException, status


class YTAssistantException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)


class YTAssistant400Exception(YTAssistantException):
    def __init__(self, detail: str):
        super().__init__(status.HTTP_400_BAD_REQUEST, detail)


class YTAssistant401Exception(YTAssistantException):
    def __init__(self, detail: str):
        super().__init__(status.HTTP_401_UNAUTHORIZED, detail)


class YTAssistant403Exception(YTAssistantException):
    def __init__(self, detail: str):
        super().__init__(status.HTTP_403_FORBIDDEN, detail)


class YTAssistant404Exception(YTAssistantException):
    def __init__(self, detail: str):
        super().__init__(status.HTTP_404_NOT_FOUND, detail)


class YTAssistant409Exception(YTAssistantException):
    def __init__(self, detail: str):
        super().__init__(status.HTTP_409_CONFLICT, detail)


# -------------------------------
# 400
# -------------------------------
EXC_400_INVALID_YT_ID = YTAssistant400Exception("Invalid YouTube video ID")

# -------------------------------
# 401
# -------------------------------
EXC_401_INVALID_TOKEN = YTAssistant401Exception("Invalid token")
EXC_401_NOT_AUTHENTICATED = YTAssistant401Exception("Not authenticated")

# -------------------------------
# 403
# -------------------------------
EXC_403_ACCOUNT_NOT_APPROVED = YTAssistant403Exception("Account not approved")

# -------------------------------
# 404
# -------------------------------
EXC_404_ACC_NOT_FOUND = YTAssistant404Exception("Account not found")
EXC_404_VID_NOT_ADDED = YTAssistant404Exception(
    "Video is not added yet. Please add the video first."
)
EXC_404_NO_VID_OR_TRANSCRIPT = YTAssistant404Exception(
    "Video not found or failed to fetch a transcript"
)
EXC_404_USER_VID_NOT_FOUND = YTAssistant404Exception("Video not found for this user")
EXC_404_SUMM_NOT_FOUND = YTAssistant404Exception(
    "Summary does not exist yet. Please create it first."
)
EXC_404_CONV_NOT_FOUND = YTAssistant404Exception("Conversation not found")
EXC_404_CONV_NOT_ADDED = YTAssistant404Exception(
    "Conversation is not added yet. Please add the conversation first."
)

# -------------------------------
# 409
# -------------------------------
EXC_409_ACC_ALREADY_EXISTS = YTAssistant409Exception("Account already exists")
EXC_409_VID_ALREADY_ADDED_TO_ACC = YTAssistant409Exception(
    "Video already added to the account"
)
EXC_409_SUMM_ALREADY_EXISTS = YTAssistant409Exception("Summary already exists")
EXC_409_CONV_ALREADY_EXISTS = YTAssistant409Exception("Conversation already exists")


# Helper function for responses
def create_responses(*exceptions: HTTPException) -> dict[int, dict[str, str]]:
    """
    Take any number of FastAPI HTTPException objects and return
    a dict suitable for the `responses` parameter in route decorators.

    Example:
        responses=create_responses(EXC_401_NOT_AUTHENTICATED, EXC_404_ACC_NOT_FOUND)
    """
    return {e.status_code: {"description": e.detail} for e in exceptions}
