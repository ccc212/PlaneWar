class AuthManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init()
        return cls._instance

    def _init(self):
        self.token = None
        self.username = None
        self.GUEST = 'guest'

    def set_token(self, token):
        self.token = token

    def get_token(self):
        return self.token

    def set_username(self, username):
        self.username = username

    def get_username(self):
        return self.username