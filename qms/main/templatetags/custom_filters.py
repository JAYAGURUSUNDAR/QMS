# In your Django app, create a 'templatetags' folder if not already present,
# and create a Python file (e.g., custom_filters.py) inside it.

# custom_filters.py
from django import template

register = template.Library()

@register.filter(name='percentage')
def percentage(value1, value2):
    return f"{(value1/value2)*100:.2f}%"
