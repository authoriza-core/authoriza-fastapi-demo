from fastapi import Request
from fastapi.responses import JSONResponse, RedirectResponse
from token_service import refresh_tokens


async def get_refresh(request: Request):
    try:
        ok = await refresh_tokens(request)

        if not ok:
            return JSONResponse(
                status_code=401,
                content={
                    "status": "error",
                    "message": "User is not authenticated",
                },
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