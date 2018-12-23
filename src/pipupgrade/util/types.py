# pylint: disable=E1101

# imports - compatibility imports
from pipupgrade         import _compat
from pipupgrade._compat import zip

# imports - standard imports
import sys
import inspect

def merge_dict(*args):
    merged = dict()

    for arg in args:
        copy = arg.copy()
        merged.update(copy)

    return merged
    
def list_filter(v, filter_):
    filtered = filter(filter_, v)
    filtered = list(filtered)

    return filtered

def dict_from_list(keys, values):
    return dict(zip(keys, values))

def isdef(var, scope):
    return var in scope    

def get_function_arguments(fn):
    # https://stackoverflow.com/a/2677263
    params  = dict()
    success = False

    if _compat.PY2:
        argspec_getter = inspect.getargspec
        success        = True
    if _compat.PYTHON_VERSION >= (3,0) and _compat.PYTHON_VERSION <= (3,4):
        argspec_getter = inspect.getfullargspec
        success        = True

    if isdef("argspec_getter", scope = locals()):
        argspec   = argspec_getter(fn)
        params    = dict_from_list(argspec.args, argspec.defaults or [])

    if _compat.PYTHON_VERSION >= (3,5):
        signature  = inspect.signature(fn)
        parameters = signature.parameters

        params     = { k: v.default for k, v in _compat.iteritems(parameters) }

        success    = True

    if not success:
        raise ValueError("Unknown Python Version {} for fetching functional arguments.".format(sys.version))

    return params