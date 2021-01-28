import importlib
import os
import logging


available_components = {}
# Changes dir to the components directory
# TODO: Add an include option to add more component folder on simulation.json
for component in os.listdir('./components'):
    file_name, extension = os.path.splitext(component)
    if not extension == '.py':
        continue
    if file_name.startswith('__') and file_name.endswith('__'):
        continue
    module = importlib.import_module(f'components.{file_name}')
    available_components[file_name] = module


def init_component(component_name, args):
    logger = logging.getLogger(__name__)
    logger.info(f'Initing component {component_name} with values {args}')
    if component_name not in available_components:
        raise Exception(f"Component {component_name} is not available")
    module = available_components[component_name]
    return module.__dict__[component_name](*args)
