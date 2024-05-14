import inspect
from sqlalchemy.orm import DeclarativeBase

# from db_models import base_model
import sys
import importlib


def module_factory():
    module_name = "src.dinamo.base_model"
    # Checking if a module can be imported
    if module_name in sys.modules:
        module = sys.modules[module_name]
        print(f"{module_name!r} already in sys.modules")
        return class_factory(module_name, module)

    elif (spec := importlib.util.find_spec(module_name)) is not None:
        # If you chose to perform the actual import ...
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        print(f"{module_name!r} has been imported")
        return class_factory(module_name, module)

    else:
        print(f"can't find the {module_name!r} module")
        return None


def class_factory(module_name, module, super_cls: type = None, **kwargs):
    exclude_clss = ["Base", "DeclarativeBase"]
    cls_names = [
        cls_name
        for cls_name, cls_obj in inspect.getmembers(sys.modules[module_name])
        if inspect.isclass(cls_obj)
        and DeclarativeBase in inspect.getmro(cls_obj)
        and cls_name not in exclude_clss
    ]
    return cls_names


if __name__ == "__main__":
    print(module_factory())
