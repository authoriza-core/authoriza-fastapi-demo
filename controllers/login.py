from fastapi import Request
from oauth_client import oauth


async def get_login(request: Request):
    # URL куда вернет пользователя после успешного входа
    redirect_uri = request.url_for("callback_route")
    # Authlib сгенерирует PKCE и перенаправит
    return await oauth.authoriza.authorize_redirect(request, redirect_uri)