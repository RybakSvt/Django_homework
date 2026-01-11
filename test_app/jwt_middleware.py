import time
from datetime import datetime, timezone
from typing import Callable, Optional
from django.conf import settings

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken


class JWTAuthMiddleware:
    """
    Автоматизирует работу с JWT из cookies:
    - Добавляет Authorization: Bearer <access> из cookie.
    - При отсутствии/скором истечении access — пытается выпустить новый по refresh.
    - Ставит новый access в cookie на ответе, если он выпускался.
    """

    # За сколько секунд до истечения access выпускать новый (защитный буфер)
    refresh_window_seconds = 60

    def __init__(self, get_response: Callable):
        self.get_response = get_response

    def __call__(self, request: Request) -> Response:
        access_cookie = request.COOKIES.get("access_token")
        refresh_cookie = request.COOKIES.get("refresh_token")

        # Флаг и значение для последующей установки нового access в cookies
        minted_access: Optional[str] = None
        access_expiry_dt: Optional[datetime] = None

        # 1) Если есть access в cookies — подставим Authorization
        if access_cookie:
            request.META["HTTP_AUTHORIZATION"] = f"Bearer {access_cookie}"

            # 2) Если access скоро истечет — попробуем заранее обновить
            if self._is_access_expiring(access_cookie) and refresh_cookie:
                new_access = self.refresh_access_token(refresh_cookie)
                if new_access:
                    # Подменим Authorization «на лету», чтобы текущий запрос прошёл уже с новым access
                    request.META["HTTP_AUTHORIZATION"] = f"Bearer {new_access}"
                    minted_access = new_access
                    # Рассчитываем expires для cookie из нового access
                    try:
                        exp_ts = AccessToken(new_access).get("exp")
                        access_expiry_dt = datetime.fromtimestamp(exp_ts, timezone.utc)
                    except Exception:
                        access_expiry_dt = None

        # 3) Если access отсутствует, но есть refresh — попробуем выпустить новый access
        elif refresh_cookie:
            new_access = self.refresh_access_token(refresh_cookie)
            if new_access:
                request.META["HTTP_AUTHORIZATION"] = f"Bearer {new_access}"
                minted_access = new_access
                try:
                    exp_ts = AccessToken(new_access).get("exp")
                    access_expiry_dt = datetime.fromtimestamp(exp_ts, timezone.utc)
                except Exception:
                    access_expiry_dt = None

        # Передаём управление дальше по цепочке
        response = self.get_response(request)

        # 4) Если мы выпустили новый access — установим/обновим cookie на ответе
        if minted_access:
            response.set_cookie(
                key="access_token",
                value=minted_access,
                httponly=True,
                #secure=not settings.DEBUG,
                secure=True,
                samesite="Strict",
                #samesite="Lax" if settings.DEBUG else 'Strict',
                expires=access_expiry_dt,
                path="/",
            )

        return response

    def refresh_access_token(self, refresh_token: Optional[str]) -> Optional[str]:
        """
        Пытаемся выпустить новый access из refresh.
        Возвращаем строку access или None при неуспехе.
        """
        if not refresh_token:
            return None
        try:
            refresh = RefreshToken(refresh_token)
            return str(refresh.access_token)
        except TokenError:
            return None

    def _is_access_expiring(self, access_token_str: str) -> bool:
        """
        Проверяем, истекает ли access в ближайшее время (заданное refresh_window_seconds).
        Считываем 'exp' из тела токена.
        """
        try:
            token = AccessToken(access_token_str)
            exp_ts = int(token.get("exp"))
            now_ts = int(time.time())
            return exp_ts <= now_ts + self.refresh_window_seconds
        except Exception:
            # Если не удалось прочитать exp — считаем, что истекает/недействителен
            return True