from django import template

from catalog.models import ProductCategory
from catalog.views import collect_children

register = template.Library()

@register.inclusion_tag('catalog/tags/horizontal_menu.html')
def render_horizontal_menu():
    root_category = ProductCategory.objects.filter(parent=None)

    oldlevel = 0
    values = []
    if len(root_category) > 0:
        categories = collect_children(root_category[0].id, 1, None)

        for (category, level) in categories:
            values.append((ProductCategory.objects.get(id=category), level, oldlevel))
            oldlevel = level

    return {
        'values': values,
        'lastlevel': oldlevel,
    }
