from django.template import Library
from markdownx.utils import markdownify

register = Library()
@register.filter
def markdown(text):
    return markdownify(text)
register.filter('markdown', markdown)

