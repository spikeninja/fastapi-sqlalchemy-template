from fastapi import APIRouter, HTTPException, status
from dishka.integrations.fastapi import FromDishka, DishkaRoute

from app.core.config import Config
from app.gateways.users import UsersGateway
from app.core.security import verify_password, create_access_token
from app.schemas.auth import AuthResponse, RegisterRequest, LoginRequest

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    route_class=DishkaRoute,
)


@router.post("/login", response_model=AuthResponse)
async def login(
    request: LoginRequest,
    config: FromDishka[Config],
    users_gateway: FromDishka[UsersGateway],
):
    """"""

    user = await users_gateway.get_by_email(email=request.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    passwords_matched = await verify_password(
        password=request.password,
        hashed=user.hashed_password,
    )

    if not passwords_matched:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    token = await create_access_token(
        payload={"sub": user.id},
        minutes=config.access_token_expire_minutes,
    )

    return {"token": token, "user": user}


@router.post("/register", response_model=AuthResponse)
async def register(
    request: RegisterRequest,
    config: FromDishka[Config],
    users_gateway: FromDishka[UsersGateway],
):
    """"""

    user = await users_gateway.get_by_email(email=request.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User with this email already exists",
        )

    user = await users_gateway.create(
        name=request.name,
        email=request.email,
        password=request.password,
    )

    token = await create_access_token(
        payload={"sub": user.id},
        minutes=config.access_token_expire_minutes,
    )

    return {"token": token, "user": user}
