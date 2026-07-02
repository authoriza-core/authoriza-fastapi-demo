from fastapi import Request
from fastapi.templating import Jinja2Templates
from session_service import restore_session
from token_service import check_token, decode_token_payload

templates = Jinja2Templates(directory="templates")


async def get_home(request: Request):
    await restore_session(request)  # восстановление сессии
    await check_token(request)

    token = request.session.get("token")
    login_time = request.session.get("login_time")

    id_token_payload = None
    access_token_payload = None

    if token:
        # Декодируем ID Token для отображения
        id_token_payload = decode_token_payload(token.get("id_token"))
        # Декодируем Access Token для отображения
        access_token_payload = decode_token_payload(token.get("access_token"))

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "authenticated": token is not None,
            "id_token_payload": id_token_payload,
            "access_token_payload": access_token_payload,
            "login_time": login_time,
        },
    )