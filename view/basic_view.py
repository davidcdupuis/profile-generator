
from jinja2 import Environment, FileSystemLoader, select_autoescape
from jinja2 import Template

import report_generator.view.templates as templates

#env = Environment(
#    loader = PackageLoader('report_generator','view/templates'),
#    autoescape=select_autoescape(['html','xml'])
#)

"""
template = Template(filename='templates/page.html')

print(template.render(title='Test',content='Hello World!'))
"""

file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)
template = env.get_template('page.html')

print(template.render(title='Test',content='Hello World!'))

def to_html(sample: dict, stats_object: dict) -> str:
    """Generate a HTML report from summary statistics and a given sample

    Parameters:
    -----------
        sample: A dict containing the samples to print.
        stats_object: Statistics to use for the overview, variables, correlations and missing values

    Returns:
    --------
        The profile report in HTML format
    """
    if not isinstance(sample, dict):
        raise TypeError("sample must be of type dict")

    if not isinstance(stats_object, dict):
        raise TypeError(
            "stats_object must be of type dict. Did you generate this using the "
            "correct function?"
        )

    """
    sections = [
        {
            "title": "Overview",
            "anchor_id": "overview",
            "content": render_overview_section(stats_object)
        },
        {
            "title": "Variables",
            "anchor_id":"variables",
            "content":render_variables_section(stats_object)
        },
        ...
    ]
    """
    return templates.template("base.html").render(
        section=sections, full_width=confi["style"]["full_width"].get(bool)
    )
