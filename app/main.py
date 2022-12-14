import logging

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2AuthorizationCodeBearer
from fastapi.middleware.cors import CORSMiddleware
from app.db import database, User
from keycloak import KeycloakOpenID
from starlette.responses import RedirectResponse

app = FastAPI(title="Fast api, Docker")

# Keycloak auth

keycloak_openId = KeycloakOpenID(
    server_url="http://localhost:8080/auth/",
    client_id="myclient",
    realm_name="myrealm",
    client_secret_key="ePLbGH6LZOWzzDB7CNNVJDoIl2LFirbR"
)
keycloak_url = "http://127.0.0.1:8080/auth/"
realm = "myrealm"

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="",  # f"{keycloak_url}realms/{realm}/protocol/openid_connect/auth"
    tokenUrl="")  # f"{keycloak_url}realm/{realm}/protocol/openid_connect/token"


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        KEYCLOAK_PUBLIC_KEY = (
                "----Begin with public key-------\n" +
                keycloak_openId.public_key() +
                "\n--------End with public key-------\n"
        )

        return keycloak_openId.decode_token(
            token, key=KEYCLOAK_PUBLIC_KEY,
            options={"verify signature ": True, "verify_aud": False, "exp": True}
        )
    except Exception as e:
        logging.ERROR(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Auth credentials",
            headers={"WWW_Authenticate": "Bearer"}
        )


@app.get("/user")
async def get_user(current_user: dict = Depends(get_current_user)):
    logging.info(current_user)
    return current_user


@app.get("/")
async def read_root():
    return await User.objects.all()


@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()

    await User.objects.get_or_create(email='test@gmail.com')


@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()
