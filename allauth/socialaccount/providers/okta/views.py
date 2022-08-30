import requests

from allauth.socialaccount import app_settings
from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
)

from .provider import OktaProvider


class OktaOAuth2Adapter(OAuth2Adapter):
    provider_id = OktaProvider.id

    settings = app_settings.PROVIDERS.get(provider_id, {})
    okta_base_url = settings.get("OKTA_BASE_URL")

    @property
    def access_token_url(self):
        return f"https://{self.okta_base_url}/oauth2/v1/token"

    @property
    def authorize_url(self):
        return f"https://{self.okta_base_url}/oauth2/v1/authorize"

    @property
    def userinfo_url(self):
        return f"https://{self.okta_base_url}/oauth2/v1/userinfo"

    @property
    def access_token_method(self):
        return "POST"

    def complete_login(self, request, app, token, **kwargs):
        """
        Get the user info from userinfo endpoint and return a
        A populated instance of the `SocialLogin` model (unsaved)

        :param request:
        :param app:
        :param token:
        :param kwargs:
        :return:
        """

        resp = requests.get(
            self.userinfo_url, headers={"Authorization": f"Bearer {token.token}"}
        )


        resp.raise_for_status()
        extra_data = resp.json()
        return self.get_provider().sociallogin_from_response(request, extra_data)


oauth2_login = OAuth2LoginView.adapter_view(OktaOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(OktaOAuth2Adapter)
