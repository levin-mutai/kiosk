# custom_oidc_auth.py
import requests
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from kiosk import settings

class CustomOIDCAuthentication(BaseAuthentication):
    def authenticate(self, request):
        access_token = self.get_access_token(request)
        if access_token is None:
            return None

        user_info = self.get_user_info(access_token)
        if user_info is None:
            return None

        return (user_info, None)

    def get_access_token(self, request):
        code = request.query_params.get('code')

        if code is None:
            return None

        token_url = f'{settings.GITHUB_OIDC_ENDPOINT}access_token'
        data = {
            'client_id': settings.GITHUB_OIDC_CLIENT_ID,
            'client_secret': settings.GITHUB_OIDC_CLIENT_SECRET,
            'code': code,
        }

        response = requests.post(token_url, data=data, headers={'Accept': 'application/json'})
        response_data = response.json()

        if 'access_token' in response_data:
            return response_data['access_token']
        else:
            return None

    def get_user_info(self, access_token):
        user_url = 'https://api.github.com/user'
        headers = {'Authorization': f'Bearer {access_token}'}

        response = requests.get(user_url, headers=headers)
        if response.status_code == 200:
            user_info = response.json()
            return user_info
        else:
            return None
