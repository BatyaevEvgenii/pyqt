# свяжем контроллеры и функции

from .controllers import echo_controller

actionnames = [
    # action - имя action, controller - соответствующая функция
    {'action':'echo', 'controller':echo_controller},
]