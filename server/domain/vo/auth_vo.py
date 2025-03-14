from dataclasses import dataclass

@dataclass
class LoginVO:
    token: str
    username: str
    user_id: int

@dataclass
class RegisterVO:
    user_id: int