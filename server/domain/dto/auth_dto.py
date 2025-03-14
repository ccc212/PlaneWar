from dataclasses import dataclass


@dataclass
class LoginDTO:
    username: str
    password: str

    def __post_init__(self):
        if not self.username:
            raise ValueError('用户名不能为空')
        if not self.password:
            raise ValueError('密码不能为空')

@dataclass
class RegisterDTO:
    username: str
    password: str

    def __post_init__(self):
        if not self.username:
            raise ValueError('用户名不能为空')
        if not self.password:
            raise ValueError('密码不能为空')
        if not self.username.isalnum():
            raise ValueError('用户名只能包含字母和数字')