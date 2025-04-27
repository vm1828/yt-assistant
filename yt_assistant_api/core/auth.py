from fastapi import HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from authlib.jose import JsonWebToken
from authlib.jose.errors import JoseError
from config import settings
import httpx

from schemas.account import Auth0Payload

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
jwt = JsonWebToken(["RS256"])


async def get_jwk():
    """Fetch the JSON Web Key Set (JWKS) from Auth0 (used for JWT token validation)."""
    async with httpx.AsyncClient() as client:
        res = await client.get(f"https://{settings.AUTH0_DOMAIN}/.well-known/jwks.json")
        return res.json()


async def verify_jwt_token(token: str) -> dict:
    """Verify the JWT token by decoding it with the Auth0 JWKS. Return claims."""
    try:
        jwks = await get_jwk()  # fetch jwks from auth0

        claims = jwt.decode(token, jwks)  # decode token using jwks
        claims.validate()  # raise an error if the token is expired or invalid

        return claims  # dict with account info
    except JoseError:
        raise HTTPException(status_code=401, detail="Invalid token")


async def get_current_account(token: str = Security(oauth2_scheme)):
    """Verify JWT token and extract current authenticated account"""
    claims = await verify_jwt_token(token)
    return Auth0Payload(sub=claims["sub"])
