from mezzanine.template import Library

register = Library()


@register.inclusion_tag("projects/inc/projects_form_field.html", takes_context=True)
def projects_form_field(context, field, private=False, left=True):
    """
    Renders a single field of the Projects form while keeping the forms context
    """
    return {"field": field, "private": private, "left": left}
