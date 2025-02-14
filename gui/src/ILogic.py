from abc import ABC, abstractmethod
from typing import Any


class LogicResult:
    def __init__(self, success: bool, value: Any = None, error: str = ""):
        self.success = success
        self.value = value
        self.error = error


class ILogic(ABC):
    @abstractmethod
    def execute(self, *args, **kwargs) -> LogicResult:
        """
        Logicモジュールの共通メソッド
        """
        pass
