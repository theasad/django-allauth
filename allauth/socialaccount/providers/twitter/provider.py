from allauth.socialaccount.providers.base import AuthAction, ProviderAccount
from allauth.socialaccount.providers.oauth.provider import OAuthProvider


class TwitterAccount(ProviderAccount):
    def get_screen_name(self):
        return self.account.extra_data.get("screen_name")

    def get_profile_url(self):
        return (
            f"http://twitter.com/{screen_name}"
            if (screen_name := self.get_screen_name())
            else None
        )

    def get_avatar_url(self):
        return (
            profile_image_url.replace("_normal", "")
            if (
                profile_image_url := self.account.extra_data.get(
                    "profile_image_url"
                )
            )
            else None
        )

    def to_str(self):
        screen_name = self.get_screen_name()
        return screen_name or super(TwitterAccount, self).to_str()


class TwitterProvider(OAuthProvider):
    id = "twitter"
    name = "Twitter"
    account_class = TwitterAccount

    def get_auth_url(self, request, action):
        return (
            "https://api.twitter.com/oauth/authorize"
            if action == AuthAction.REAUTHENTICATE
            else "https://api.twitter.com/oauth/authenticate"
        )

    def extract_uid(self, data):
        return data["id"]

    def extract_common_fields(self, data):
        return dict(
            username=data.get("screen_name"),
            name=data.get("name"),
            email=data.get("email"),
        )


provider_classes = [TwitterProvider]
