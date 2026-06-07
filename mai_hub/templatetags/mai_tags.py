from django import template
import mai_hub.views as views
from mai_hub.models import Category, TagPost
from mai_hub.utils import menu

register = template.Library()


@register.simple_tag
def get_menu():
    return menu


@register.inclusion_tag('mai_hub/list_categories.html')
def show_categories(cat_selected=0):
    cats = Category.objects.all()
    return {'cats': cats, 'cat_selected': cat_selected}


@register.inclusion_tag('mai_hub/list_tags.html')
def show_all_tags():
    return {'tags': TagPost.objects.all()}