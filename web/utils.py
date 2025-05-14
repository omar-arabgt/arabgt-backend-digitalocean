from itertools import chain
from django.db.models import Q, Value, CharField, F
from django.utils.dateparse import parse_date
from allauth.socialaccount.models import SocialAccount
from api.models import User, DeletedUser
from api.choices import UserRank, CAR_SORTING_ITEMS, COUNTRIES


    

def get_merged_user_data(query='', nationality=None, country=None, birthdate=None, gender=None, status=None, rank=None, page=None, paginate_by=None):
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
    user_filters = Q(is_staff=False, is_superuser=False, emailaddress__verified=True)
    deleted_user_filters = Q()
    
    if query:
        user_filters &= Q(Q(username__icontains=query) | Q(email__icontains=query) | 
                        Q(first_name__icontains=query) | Q(last_name__icontains=query) | 
                        Q(nick_name__icontains=query))
        deleted_user_filters &= Q(Q(username__icontains=query) | Q(email__icontains=query) | 
                                Q(first_name__icontains=query) | Q(last_name__icontains=query) | 
                                Q(nick_name__icontains=query))
    
    if nationality:
        user_filters &= Q(nationality=nationality)
        deleted_user_filters &= Q(nationality=nationality)
    
    if gender:
        user_filters &= Q(gender=gender)
        deleted_user_filters &= Q(gender=gender)
    
    if country:
        user_filters &= Q(country=country)
        deleted_user_filters &= Q(country=country)
    
    if rank:
        user_filters &= Q(point__gte=rank)
        deleted_user_filters &= Q(point__gte=rank)
        next_rank_value = UserRank.next_rank_value(int(rank))
        if next_rank_value:
            user_filters &= Q(point__lt=next_rank_value)
            deleted_user_filters &= Q(point__lt=next_rank_value)
    
    if birthdate:
        try:
            date = parse_date(birthdate)
            if date:
                user_filters &= Q(birth_date=date)
                deleted_user_filters &= Q(birth_date=date)
        except ValueError:
            pass
    
    # Create empty result sets by default
    users_result = []
    deleted_users_result = []
    
    # Only query active users if needed
    if not status or status == 'active':
        # Use select_related to optimize the query
        users = User.objects.filter(user_filters).select_related('nationality', 'country')
        
        # Apply sorting for consistency
        users = users.order_by('id')
        
        # Annotate in the database rather than individually
        users = users.annotate(
            status=Value('active', output_field=CharField()),
            delete_reason=Value('', output_field=CharField())
        )
        
        # Extract only the needed fields
        users_result = list(users.values(
            'id', 'first_name', 'last_name', 'nick_name', 'birth_date', 'gender',
            'status', 'delete_reason', 'nationality', 'country', 'point'
        ).annotate(
            get_nationality_display=F('nationality'),
            get_country_display=F('country'),
            rank=F('point')
        ))
        
        # Fix display values for nationality and country in one batch
        country_dict = dict(COUNTRIES)
        for user in users_result:
            user['get_nationality_display'] = country_dict.get(user['nationality'], user['nationality'])
            user['get_country_display'] = country_dict.get(user['country'], user['country'])
    
    # Only query deleted users if needed
    if not status or status == 'deleted':
        # Similar optimizations for deleted users
        deleted_users = DeletedUser.objects.filter(deleted_user_filters).select_related('nationality', 'country')
        deleted_users = deleted_users.order_by('id')
        
        deleted_users = deleted_users.annotate(
            status=Value('deleted', output_field=CharField())
        )
        
        deleted_users_result = list(deleted_users.values(
            'id', 'user_id', 'first_name', 'last_name', 'nick_name', 'birth_date', 
            'gender', 'delete_reason', 'status', 'nationality', 'country', 'rank'
        ))
        
        # Fix display values for deleted users
        for user in deleted_users_result:
            user['get_nationality_display'] = country_dict.get(user['nationality'], user['nationality'])
            user['get_country_display'] = country_dict.get(user['country'], user['country'])
    
    # Combine results 
    combined_results = users_result + deleted_users_result
    
    # Sort in memory (only sorting the current page results)
    combined_results.sort(key=lambda x: x.get('id', 0))
    
    # Implement pagination if requested
    if page is not None and paginate_by is not None:
        start_idx = (page - 1) * paginate_by
        end_idx = start_idx + paginate_by
        return combined_results[start_idx:end_idx]
    
    return combined_results

def get_signup_method(user_id):
    social_account = SocialAccount.objects.filter(user_id=user_id).first()
    if social_account:
        return social_account.provider
    return "email"


CAR_SORTING_LIST = [i for i,_ in CAR_SORTING_ITEMS]

def get_car_sorting_index(user_sorting):
    car_index_list = []
    for car in CAR_SORTING_LIST:
        try:
            idx = user_sorting.index(car) + 1
        except:
            idx = "-"
        car_index_list.append(idx)
    return car_index_list
