from auth_storage import clear_auth_data
from fastapi import Request
from fastapi.responses import RedirectResponse


async def get_logout(request: Request):
    request.session.clear()  # очищение сессии
    clear_auth_data()  # удаление файла сессии (json)
    return RedirectResponse(url="/")