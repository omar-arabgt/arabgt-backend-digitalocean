from django import template

register = template.Library()

@register.filter(name='gender_translation')
def gender_translation(gender_code):
    translations = {
        'M': 'ذكر',
        'F': 'أنثى',
    }
    return translations.get(gender_code, '')

@register.filter(name='get_display')
def get_display(value, choices):
    if value:
        return ', '.join([dict(choices).get(val, val) for val in value])
    return 'لا توجد بيانات'