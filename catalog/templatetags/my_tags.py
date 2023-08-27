from django import template

register = template.Library()


@register.filter(name='mymedia')
def mymedia_filter(val):
    if val:
        return f'/media/{val}'

    return '#'
