from typing import Callable, Dict, List
from client.src.enums.even_type import EventType
from client.src.enums.game_state import MenuState, GameState

class GameStateManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init()
        return cls._instance

    def _init(self):
        self.menu_state = MenuState.MAIN
        self.game_state = GameState.NOT_STARTED
        self.listeners: Dict[EventType, List[Callable]] = {}

    def set_menu_state(self, new_state: MenuState):
        self.menu_state = new_state
        self._notify_listeners(EventType.UI_STATE_CHANGE, new_state)

    def set_game_state(self, new_state: GameState):
        self.game_state = new_state
        self._notify_listeners(EventType.GAME_STATE_CHANGE, new_state)

    def get_menu_state(self):
        return self.menu_state

    def get_game_state(self):
        return self.game_state

    def _notify_listeners(self, event_type: EventType, new_state: GameState | MenuState):
        if event_type in self.listeners:
            for callback in self.listeners[event_type]:
                callback(new_state)
                
    # 监听事件
    def add_listener(self, event_type: EventType, callback: Callable):
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(callback)

    # 移除监听事件
    def remove_listener(self, event_type: EventType, callback: Callable):
        if event_type in self.listeners and callback in self.listeners[event_type]:
            self.listeners[event_type].remove(callback)
