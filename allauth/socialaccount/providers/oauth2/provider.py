from urllib.parse import parse_qsl

from django.urls import reverse
from django.utils.http import urlencode

from allauth.socialaccount.providers.base import Provider


class OAuth2Provider(Provider):
    def get_login_url(self, request, **kwargs):
        url = reverse(f"{self.id}_login")
        if kwargs:
            url = f"{url}?{urlencode(kwargs)}"
        return url

    def get_auth_params(self, request, action):
        settings = self.get_settings()
        ret = dict(settings.get("AUTH_PARAMS", {}))
        if dynamic_auth_params := request.GET.get("auth_params", None):
            ret |= dict(parse_qsl(dynamic_auth_params))
        return ret

    def get_scope(self, request):
        settings = self.get_settings()
        scope = list(settings.get("SCOPE", self.get_default_scope()))
        if dynamic_scope := request.GET.get("scope", None):
            scope.extend(dynamic_scope.split(","))
        return scope

    def get_default_scope(self):
        return []
