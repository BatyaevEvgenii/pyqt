# импортируем .controllers - из текущей директории
from .controllers import server_error_controller

actionnames = [
    {'action':'servererror', 'controller': server_error_controller},
]