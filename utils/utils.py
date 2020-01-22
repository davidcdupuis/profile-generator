"""Useful for Jupyter notebook"""

def full_width():
    """Resize the notebook to use it's full width"""
    from IPython.core.display import display, HTML
    displayHTML(HTML("<style>.container {width:100% !important;}</style>"))

"""Useful paths"""
from pathlib import Path
def get_project_root() -> Path:
    """Returns the path to the project root folder
    """
    return Path(__file__).parent.parent.parent

def get_config_default() -> Path():
    """Return the path to the config file
    """
    return Path(__file__).parent.parent / "config.yaml"

"""OTHER"""
import numpy as np
def to_json(o, level = 0) -> str:
    INDENT = 3
    SPACE = " "
    NEWLINE = "\n"
    ret = ""
    if isinstance(o, dict):
        ret += "{" + NEWLINE
        comma = ""
        for k,v in o.items():
            ret += comma
            comma = ",\n"
            ret += SPACE * INDENT * (level+1)
            ret += '"' + str(k) + '":' + SPACE
            ret += to_json(v, level + 1)

        ret += NEWLINE + SPACE * INDENT * level + "}"
    elif isinstance(o, str):
        ret += '"' + o + '"'
    elif isinstance(o, list):
        ret += "[" + ",".join([to_json(e, level+1) for e in o]) + "]"
    elif isinstance(o, bool):
        ret += "true" if o else "false"
    elif isinstance(o, int):
        ret += str(o)
    elif isinstance(o, float):
        ret += '%.7g' % o
    elif isinstance(o, np.ndarray) and np.issubdtype(o.dtype, np.integer):
        ret += "[" + ','.join(map(str, o.flatten().tolist())) + "]"
    elif isinstance(o, np.ndarray) and np.issubdtype(o.dtype, np.inexact):
        ret += "[" + ','.join(map(lambda x: '%.7g' % x, o.flatten().tolist())) + "]"
    elif o is None:
        ret += 'null'
    else:
        raise TypeError("Unknown type '%s' for json serialization" % str(type(o)))
    return ret
