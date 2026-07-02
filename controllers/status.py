from fastapi import Request
from session_service import restore_session
from token_service import check_token


async def get_status(request: Request):
    await restore_session(request)  # восстановление сессии
    await check_token(request)

    token = request.session.get("token")

    if not token:
        return {
            "authenticated": False,
        }

    return {
        "authenticated": True,
        "login_time": request.session.get("login_time"),
        "last_refresh_time": request.session.get("last_refresh_time"),
        "access_token_expires_at": request.session.get("access_token_expires_at"),
        "refresh_token_expires_at": request.session.get("refresh_token_expires_at"),
        "token_type": token.get("token_type"),
        "scope": token.get("scope"),
    }