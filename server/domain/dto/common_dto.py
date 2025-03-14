from dataclasses import dataclass
from typing import TypeVar, Generic, Optional

T = TypeVar('T')  # 定义泛型类型

@dataclass
class Result(Generic[T]):
    code: int = 200  # HTTP状态码
    msg: str = "success"  # 提示信息
    data: Optional[T] = None  # 响应数据
    
    @staticmethod
    def success(data: T = None, msg: str = "success") -> 'Result[T]':
        return Result(200, msg, data)
    
    @staticmethod
    def error(msg: str, code: int = 400) -> 'Result[None]':
        return Result(code, msg, None)