from django import template


register = template.Library()


@register.simple_tag
def message_preview(message):
    if len(message) > 30:
        return message[:30] + '...'
    return message