from django import template        

register = template.Library()


@register.filter(name='access')    
def access(value, arg):    
    return value.get(arg, value.get(str(arg), None))