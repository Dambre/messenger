from django import template


register = template.Library()


@register.simple_tag
def message_preview(message):
    if len(message) > 50:
        return message[:50] + '...'
    return message