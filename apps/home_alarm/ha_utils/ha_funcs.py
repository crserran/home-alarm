import importlib
import pkgutil
import os


def import_modules(file_dir, package):
    pkg_dir = os.path.dirname(file_dir)
    for (_, name, _) in pkgutil.iter_modules([pkg_dir]):
        importlib.import_module("." + name, package)


def all_subclasses(cls_, package: str):
    subclasses = list(
        set(cls_.__subclasses__()).union(
            [s for c in cls_.__subclasses__() for s in all_subclasses(c, package)]
        )
    )
    return [subclass for subclass in subclasses if package in subclass.__module__]


def get_subclasses(file_dir: str, package: str, parent_class, excluded=None):
    if excluded is None:
        excluded = []
    import_modules(file_dir, package)
    subclasses = all_subclasses(parent_class, package)
    return [
        cls_
        for cls_ in subclasses
        if cls_ not in excluded and len(cls_.__subclasses__()) == 0
    ]
