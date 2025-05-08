from fastapi import APIRouter, Depends
from dishka.integrations.fastapi import DishkaRoute, FromDishka

from app.api.dependencies import get_current_user
from app.repositories import UsersRepository
from app.schemas.users import UserPublic, UserUpdateRequest, UserDTO

router = APIRouter(prefix="/users", route_class=DishkaRoute)


@router.get("/me", response_model=list[UserPublic])
async def get_me(current_user: UserDTO = Depends(get_current_user)):
    """"""

    return current_user


@router.patch("/me", response_model=UserPublic)
async def update_me(
    request: UserUpdateRequest,
    users_repo: FromDishka[UsersRepository],
    current_user: UserDTO = Depends(get_current_user),
):
    """"""

    values = request.model_dump(exclude_unset=True)
    await users_repo.update(_id=current_user.id, values=values)

    return await users_repo.get_by_id(_id=current_user.id)


@router.get("/", response_model=list[UserPublic])
async def get_users(
    limit: int,
    offset: int,
    users_repo: FromDishka[UsersRepository],
):
    """"""

    return await users_repo.get_all(limit=limit, offset=offset)
