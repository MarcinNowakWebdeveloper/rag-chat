import pkgutil
import importlib
import os


def load_models():
    package = __name__
    path = __path__[0]
    dirs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]

    for dir in dirs:
        for _, module_name, _ in pkgutil.iter_modules([path + "/" + dir]):
            importlib.import_module(f"{package}.{dir}.{module_name}")
