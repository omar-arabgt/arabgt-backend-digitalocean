from itertools import chain
from django.db.models import Q, Value, CharField
from django.utils.dateparse import parse_date
from api.models import User, DeletedUser

def get_merged_user_data(query='', nationality=None, country=None, birthdate=None, gender=None, status=None):
    """
    Merges and filters data from the User and DeletedUser models based on the provided criteria.

    Input:
    - query: A string to search for in the username field.
    - nationality: A filter for the nationality of users.
    - country: A filter for the country of users.
    - birthdate: A filter for users born after a certain date.
    - gender: A filter for the gender of users.
    - status: A filter for the status of users ('active' or 'deleted').

    Functionality:
    - Applies filters to the User and DeletedUser models based on the input criteria.
    - Annotates each user with a 'status' field to indicate whether the user is active or deleted.
    - Combines and sorts the filtered data from both models.
    - Optionally filters the combined data by status.

    Output:
    - Returns a combined, sorted, and filtered list of dictionaries containing user data.
    """
    
    # Filtering active users
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

    # Querying active users and annotating them with status 'active'
    users = User.objects.filter(user_filters).values(
        'id', 'first_name', 'last_name', 'nick_name', 'birth_date', 'gender',
    ).annotate(
        status=Value('active', output_field=CharField()),
        delete_reason=Value('', output_field=CharField())
    )

    # Adding display fields for nationality and country
    user_data = [
        dict(user, get_nationality_display=User.objects.get(pk=user['id']).get_nationality_display(),
             get_country_display=User.objects.get(pk=user['id']).get_country_display(),
             rank=User.objects.get(pk=user['id']).rank)
        for user in users
    ]

    # Filtering deleted users
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

    # Querying deleted users and annotating them with status 'deleted'
    deleted_users = DeletedUser.objects.filter(deleted_user_filters).values(
        'id', 'first_name', 'last_name', 'nick_name', 'birth_date', 'gender', 'delete_reason', 'rank'
    ).annotate(
        status=Value('deleted', output_field=CharField())
    )

    # Adding display fields for nationality and country
    deleted_user_data = [
        dict(user, get_nationality_display=DeletedUser.objects.get(pk=user['id']).get_nationality_display(),
             get_country_display=DeletedUser.objects.get(pk=user['id']).get_country_display())
        for user in deleted_users
    ]

    # Combining and sorting the user data and deleted user data
    combined_queryset = sorted(
        chain(user_data, deleted_user_data),
        key=lambda instance: instance['id']
    )

    # Filtering by status if specified
    if status:
        combined_queryset = [user for user in combined_queryset if user['status'] == status]

    return combined_queryset
