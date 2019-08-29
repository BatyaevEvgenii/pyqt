import os
import yaml
import logging
import functools
from argparse import ArgumentParser

from app import Application
from handlers import handle_default_request
# from database import Base
# from settings import INSTALLED_MODULES, BASE_DIR


parser = ArgumentParser()

parser.add_argument(
    '-c', '--config', type=str,
    required=False, help='Sets config file path'
)

# parser.add_argument(
#     '-m', '--migrate', action='store_true'
# )

args = parser.parse_args()

default_config = {
    'host': 'localhost',
    'port': 8000,
    'buffersize': 1024
}

if args.config:
    with open(args.config) as file:
        file_config = yaml.load(file, Loader=yaml.Loader)
        default_config.update(file_config)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('server.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

# if args.migrate:
#     module_name_list = [f'{item}.models' for item in INSTALLED_MODULES]
#     module_path_list = (os.path.join(BASE_DIR, item, 'models.py') for item in INSTALLED_MODULES)
#     for index, path in enumerate(module_path_list):
#         if os.path.exists(path):
#             __import__(module_name_list[index])
#     Base.metadata.create_all()
#
# else:
with Application(default_config.get('host'),
                default_config.get('port'),
                default_config.get('buffersize'),
                handle_default_request) as app:
    app.bind()
    app.run()
