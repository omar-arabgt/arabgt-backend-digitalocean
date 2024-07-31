# utils.py
from itertools import chain
from django.db.models import Q, Value, CharField
from django.utils.dateparse import parse_date
from api.models import User, DeletedUser

def get_merged_user_data(query='', nationality=None, country=None, birthdate=None, gender=None, status=None):
    user_filters = Q(is_staff=False, is_superuser=False)
    if query:
        user_filters &= Q(username__icontains=query)
    if nationality:
        user_filters &= Q(nationality=nationality)
    if gender:
        user_filters &= Q(gender=gender)
    if country:
        user_filters &= Q(country=country)
    if birthdate:
        try:
            date = parse_date(birthdate)
            if date:
                user_filters &= Q(birth_date__gt=date)
        except ValueError:
            pass

    users = User.objects.filter(user_filters).values(
        'id', 'username', 'email', 'nick_name', 'phone_number', 'birth_date', 'gender', 'nationality', 'country',
        'has_business', 'has_car', 'car_type', 'hobbies', 'favorite_presenter', 'favorite_show'
    ).annotate(
        status=Value('active', output_field=CharField())
    )
    user_data = [
        dict(user, get_nationality_display=User.objects.get(pk=user['id']).get_nationality_display(),
             get_country_display=User.objects.get(pk=user['id']).get_country_display())
        for user in users
    ]

    deleted_user_filters = Q()
    if query:
        deleted_user_filters &= Q(username__icontains=query)
    if nationality:
        deleted_user_filters &= Q(nationality=nationality)
    if gender:
      deleted_user_filters &= Q(gender=gender)
    if country:
        deleted_user_filters &= Q(country=country)
    if birthdate:
        try:
            date = parse_date(birthdate)
            if date:
                deleted_user_filters &= Q(birth_date__gt=date)
        except ValueError:
            pass

    deleted_users = DeletedUser.objects.filter(deleted_user_filters).values(
        'id', 'username', 'email', 'nick_name', 'phone_number', 'birth_date', 'gender', 'nationality', 'country',
        'has_business', 'has_car', 'car_type', 'hobbies', 'favorite_presenter', 'favorite_show'
    ).annotate(
        status=Value('deleted', output_field=CharField())
    )
    deleted_user_data = [
        dict(user, get_nationality_display=DeletedUser.objects.get(pk=user['id']).get_nationality_display(),
             get_country_display=DeletedUser.objects.get(pk=user['id']).get_country_display())
        for user in deleted_users
    ]

    combined_queryset = sorted(
        chain(user_data, deleted_user_data),
        key=lambda instance: instance['id']
    )

    if status:
        combined_queryset = [user for user in combined_queryset if user['status'] == status]

    return combined_queryset
