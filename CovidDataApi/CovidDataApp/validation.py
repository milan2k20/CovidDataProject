from CovidDataApp.models import User
import datetime


def validate_input(request):
    data = {
        'country': '',
        'start_date': '',
        'end_date': '',
        'difference': 0,
        'errorMessage': ''
    }
    country = request.query_params.get('country')
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')
    if start_date is not None:
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    if end_date is not None:
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    if country is None:
        current_user = request.user
        user_country = User.objects.filter(
            email=current_user).values_list('country').first()
        data['country'] = user_country[0]
    else:
        data['country'] = country

    if start_date is None and end_date is None:
        end_date = datetime.datetime.today().date()
        start_date = end_date - datetime.timedelta(14)
        data['end_date'] = datetime.datetime.strftime(end_date, "%Y-%m-%d")
        data['start_date'] = datetime.datetime.strftime(start_date, "%Y-%m-%d")
        data['difference'] = 15
        
    elif start_date is None and end_date is not None:
        data['errorMessage'] = 'Both start and end date are required for date range'
    elif start_date is not None and end_date is None:
        data['errorMessage'] = 'Both start and end date are required for date range'
    elif start_date > end_date:
        data['errorMessage'] = 'Start date must be less than end date'
    elif end_date > datetime.datetime.today():
        data['errorMessage'] = 'End date cannot be in future'
    else:
        data['end_date'] = datetime.datetime.strftime(end_date, "%Y-%m-%d")
        data['start_date'] = datetime.datetime.strftime(start_date, "%Y-%m-%d")
        data['difference'] = (end_date - start_date).days + 1

    return data
