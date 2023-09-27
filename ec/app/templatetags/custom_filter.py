from django import template

register = template.Library()

@register.filter(name='get_item')
def get_item(lst, i):
    try:
        return lst[i]
    except (IndexError, KeyError):
        return None
    
@register.simple_tag
def old(request, field_name, init_value=""):
    return request.POST.get(field_name, init_value)