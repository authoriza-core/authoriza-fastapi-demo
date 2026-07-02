from datetime import datetime, timedelta
from auth_storage import save_auth_data
from fastapi import Request
from fastapi.responses import JSONResponse, RedirectResponse
from oauth_client import oauth
from token_service import get_refresh_expires_at


async def get_callback(request: Request):
    # Пользователь или провайдер вернул ошибку
    error = request.query_params.get("error")
    if error:
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "error": error,
                "error_description": request.query_params.get("error_description"),
            },
        )

    try:
        # Обмен code на токены
        token = await oauth.authoriza.authorize_access_token(request)

        if not token:
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": "Token exchange failed",
                },
            )

        now = datetime.now()

        # Создаём пользовательскую сессию и сохраняем в неё
        request.session["token"] = token
        request.session["login_time"] = now.isoformat()

        # время истечения токена
        request.session["access_token_expires_at"] = (
            now + timedelta(seconds=token["expires_in"])
        ).isoformat()

        # пытаемся достать срок жизни refresh_token
        if "refresh_expires_in" in token:  # если в самом токене есть
            request.session["refresh_token_expires_at"] = (
                now + timedelta(seconds=token["refresh_expires_in"])
            ).isoformat()
        else:  # то декодируем как JWT
            request.session["refresh_token_expires_at"] = get_refresh_expires_at(token)

        # сохранение данных после логина
        save_auth_data(
            request.session["token"],
            request.session["login_time"],
            request.session["access_token_expires_at"],
            request.session["refresh_token_expires_at"],
        )

        return RedirectResponse(url="/")

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": str(e),
            },
        )