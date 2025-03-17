import socket
import urllib3
import requests
from client.src.managers.auth_manager import AuthManager

# 参考https://blog.csdn.net/as23751782/article/details/127243514
# 强制使用 IPv4
def allowed_gai_family():
    return socket.AF_INET
    
urllib3.util.connection.allowed_gai_family = allowed_gai_family

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

    @staticmethod
    def put(url, data=None):
        try:
            response = requests.put(
                url,
                json=data,
                headers=HttpClient.get_headers()
            )
            return response
        except Exception as e:
            raise Exception('网络错误，请稍后重试')
    
