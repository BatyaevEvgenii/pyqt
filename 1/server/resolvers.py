# будет находить все пары нашего решения action - actionnames внутри проекта,
# динамически по их имени

# позволит из коллекции получить одну запись
from functools import reduce


from settings import INSTALLED_MODULES


def get_server_actions():
    # список модулей
    modules = reduce(
        lambda value, item: value + [__import__(f'{item}.actions')],
        INSTALLED_MODULES, []
    )

    # список подмодулей
    submodules = reduce(
        lambda value, item: value + [getattr(item, 'actions', [])],
        modules, []
    )
    actionnames = reduce(
        lambda value, item: value + getattr(item, 'actionnames', []),
        submodules, []
    )
    return {itm.get('action'): itm.get('controller') for itm in actionnames}

def resolve(action_name, actions=None):
    actionnames = actions or get_server_actions()
    return actionnames.get(action_name)
