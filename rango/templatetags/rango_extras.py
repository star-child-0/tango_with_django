from os import register_at_fork
from django import template
from rango.models import Category

register = template.Library()


@register_at_fork.inclusion_tag('rango/cats.html')
def get_category_list(cat=None):
	return {'cats': Category.objects.all(), 'act_cat': cat}
