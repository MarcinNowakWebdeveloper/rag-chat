import pkgutil
import importlib
import backend.imports.splitters as splitters


def bootstrap():

    #   Splitters
    for module in pkgutil.iter_modules(splitters.__path__):
        importlib.import_module(f"backend.imports.splitters.{module.name}")
