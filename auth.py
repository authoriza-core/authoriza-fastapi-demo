from fastapi import APIRouter, Request
from controllers import callback, home, login, logout, refresh, status

router = APIRouter()


# главная страница
@router.get("/")
async def home_route(request: Request):
    return await home.get_home(request)


@router.get("/login")
async def login_route(request: Request):
    return await login.get_login(request)


@router.get("/callback")
async def callback_route(request: Request):
    return await callback.get_callback(request)


@router.get("/status")
async def status_route(request: Request):
    return await status.get_status(request)


@router.get("/refresh")
async def refresh_route(request: Request):
    return await refresh.get_refresh(request)


# выход из аккаунта
@router.get("/logout")
async def logout_route(request: Request):
    return await logout.get_logout(request)