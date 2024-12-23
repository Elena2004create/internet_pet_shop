from fastapi import APIRouter, Depends
from psycopg import connect

from infra.dependencies import (
    get_connection,
    encode_token,
    decode_token,
    get_current_user,
    get_password,
)
from infra.models.user import UserCreateDTO
from server.infra.models.product import Cart
from server.infra.userRepo import UserRepo


user_router = APIRouter(prefix="/users", tags=["User"])


@user_router.get("/")
async def get_users(name):
    return encode_token(name)


@user_router.get("/get2")
async def get_users2(name):
    return get_password(name)


@user_router.get("/cart", response_model=Cart)
async def get_cart(conn=Depends(get_connection)):
    user_repo = UserRepo(conn)
    return user_repo.get_cart()


@user_router.post("/cart")
async def add_to_cart(article: int, quantity: int, conn=Depends(get_connection)):
    user_repo = UserRepo(conn)
    return user_repo.add_to_cart(article, quantity)


@user_router.delete("/cart")
async def add_to_cart(article: int, conn=Depends(get_connection)):
    user_repo = UserRepo(conn)
    return user_repo.remove_from_cart(article)

