from django import template
from zoook.catalog.models import ProductCategory

register = template.Library()

@register.inclusion_tag('catalog/tags/horizontal_menu.html')
def render_horizontal_menu():
    values = ProductCategory.objects.filter()

    for value in values:
        print "%s - %s" % (value.id, value.parent_id)

    return {
        'values': values,
    }
