from importlib import import_module
from flask import Blueprint
from util.file_util import read_json

api = Blueprint('api', __name__)

routing_config = read_json(f'core/routing/routing_config.json')

for routing in routing_config.get('routing', []):
    for im in routing["import"]:
        module = "{}.{}".format(routing["from"], im)
        import_module(module)
