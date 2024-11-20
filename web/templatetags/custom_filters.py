from django import template
from django.utils.timesince import timesince
from django.utils.translation import gettext as _

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

@register.filter
def arabic_timesince(value):
    time = timesince(value)
    time = time.replace('years', 'سنوات').replace('year', 'سنة')
    time = time.replace('months', 'أشهر').replace('month', 'شهر')
    time = time.replace('weeks', 'أسابيع').replace('week', 'أسبوع')
    time = time.replace('days', 'أيام').replace('day', 'يوم')
    time = time.replace('hours', 'ساعات').replace('hour', 'ساعة')
    time = time.replace('minutes', 'دقائق').replace('minute', 'دقيقة')
    time = time.replace('seconds', 'ثواني').replace('second', 'ثانية')
    return f"منذ {time}"

@register.simple_tag
def query_transform(request, **kwargs):
    updated = request.GET.copy()
    for k, v in kwargs.items():
        updated[k] = v
    return updated.urlencode()