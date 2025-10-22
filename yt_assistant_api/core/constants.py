from enum import Enum


# -------------------------------
# Enums
# -------------------------------
class Env(Enum):
    LOCAL = "local"
    DEV = "dev"
    TEST = "test"
    PROD = "prod"


# -------------------------------
# Reusable HTTP response dicts
# -------------------------------
RESP_401_NOT_AUTHENTICATED = {"description": "Not authenticated"}
RESP_403_ACCOUNT_NOT_APPROVED = {"description": "Account not approved"}
RESP_400_INVALID_YT_ID = {"description": "Invalid YouTube video ID"}
