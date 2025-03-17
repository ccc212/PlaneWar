import requests
from client.src.managers.auth_manager import AuthManager


class HttpClient:
    @staticmethod
    def get_headers():
        token = AuthManager().get_token()
        headers = {
            'Content-Type': 'application/json'
        }
        if token:
            headers['Authorization'] = f'Bearer {token}'
        return headers

    @staticmethod
    def post(url, data=None):
        try:
            response = requests.post(
                url,
                json=data,
                headers=HttpClient.get_headers()
            )
            return response
        except Exception as e:
            raise Exception('网络错误，请稍后重试')

    @staticmethod
    def get(url):
        try:
            response = requests.get(
                url,
                headers=HttpClient.get_headers()
            )
            return response
        except Exception as e:
            raise Exception('网络错误，请稍后重试')