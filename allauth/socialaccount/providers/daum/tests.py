import json

from allauth.socialaccount.tests import OAuth2TestsMixin
from allauth.tests import MockedResponse, TestCase

from .provider import DaumProvider


class DaumTests(OAuth2TestsMixin, TestCase):
    provider_id = DaumProvider.id

    def get_mocked_response(self):
        result = {
            "userid": "38DTh",
            "id": 46287445,
            "nickname": "xncbf",
            "bigImagePath": "https://img1.daumcdn.net/thumb/",
            "openProfile": "https://img1.daumcdn.net/thumb/",
        }

        body = {"code": 200, "message": "OK", "result": result}
        return MockedResponse(200, json.dumps(body))
