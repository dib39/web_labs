from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Получение значения из словаря по ключу в шаблоне"""
    return dictionary.get(key)