from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth.provider import OAuthProvider


class TumblrAccount(ProviderAccount):
    def get_profile_url_(self):
        return f'http://{self.account.extra_data.get("name")}.tumblr.com/'

    def to_str(self):
        dflt = super(TumblrAccount, self).to_str()
        return self.account.extra_data.get("name", dflt)


class TumblrProvider(OAuthProvider):
    id = "tumblr"
    name = "Tumblr"
    account_class = TumblrAccount

    def extract_uid(self, data):
        return data["name"]

    def extract_common_fields(self, data):
        return dict(
            first_name=data.get("name"),
        )


provider_classes = [TumblrProvider]
