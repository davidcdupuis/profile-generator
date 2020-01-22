"""Contains all templates used for generating the HTML report"""

import jinja2
from jinja2 import Environment, FileSystemLoader

from report_generator.view.formaters import (
    fmt_percent,
    fmt_bytesize,
    fmt_numeric,
    fmt_array,
    fmt,
)

# Initializing Jinja
file_loader = FileSystemLoader('templates')
env = Environment(lstrip_blocks=True, trim_blocks=True, loader=file_loader)
env.filters["fmt_percent"]  = fmt_percent
env.filters["fmt_bytesize"] = fmt_bytesize
env.filters["fmt_numeric"]  = fmt_numeric
env.filters["fmt_array"]    = fmt_array
env.filters["fmt"]          = fmt

def template(template_name: str) -> jinja2.Template:
    """Get the template object given the name

    Parameters:
    -----------
        template_name: The name of the template file (.html)

    Returns:
    --------
        The jinja2 environment

    """
    return env.get_template(template_name)
