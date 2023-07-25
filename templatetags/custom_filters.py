from django import template
from django.utils.safestring import mark_safe
import re

register = template.Library()

@register.filter
def highlight(text, search_query):
    pattern = re.compile(f'({re.escape(search_query)})', re.IGNORECASE)
    return mark_safe(pattern.sub(r'<span class="highlight">\1</span>', text))
