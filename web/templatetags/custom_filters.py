from django import template

register = template.Library()

@register.filter(name='gender_translation')
def gender_translation(gender_code):
    translations = {
        'M': 'ذكر',
        'F': 'أنثى',
    }
    return translations.get(gender_code, '')

