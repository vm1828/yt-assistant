import httpx
from authlib.jose import JsonWebToken
from authlib.jose.errors import JoseError
from fastapi import HTTPException, Security, status
from fastapi.security import OAuth2PasswordBearer

from config import settings
from core.exceptions import EXC_403_ACCOUNT_NOT_APPROVED
from schemas.account import Auth0Payload

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
jwt = JsonWebToken(["RS256"])


async def get_jwk():
    """Fetch the JSON Web Key Set (JWKS) from Auth0 (used for JWT token validation)."""
    async with httpx.AsyncClient() as client:
        res = await client.get(f"https://{settings.AUTH0_DOMAIN}/.well-known/jwks.json")
        return res.json()


async def verify_jwt_token(token: str, audience: str, approved_claim: str) -> dict:
    """Verify the JWT token by decoding it with the Auth0 JWKS. Return claims."""
    try:
        jwks = await get_jwk()  # fetch jwks from auth0

        claims = jwt.decode(token, jwks)  # decode token using jwks
        claims.validate()  # raise an error if the token is expired or invalid

        if audience not in claims.get("aud"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid audience"
            )

        if not claims.get(approved_claim, False):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=EXC_403_ACCOUNT_NOT_APPROVED.detail,
            )

        return claims  # dict with account info
    except JoseError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )


async def get_current_account(token: str = Security(oauth2_scheme)):
    """Verify JWT token and extract current authenticated account"""
    aud = settings.AUTH0_AUDIENCE
    approved_claim = f"{aud}/approved"
    claims = await verify_jwt_token(token, aud, approved_claim)
    return Auth0Payload(sub=claims["sub"])
