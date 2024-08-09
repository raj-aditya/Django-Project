import datetime
from datetime import date, timezone
from datetime import timedelta
from django.http import JsonResponse
from .models import User

def check_authorization(view_func):
    def wrapper(request, *args, **kwargs):
        if 'Authorization' in request.headers:
            access_token = request.headers['Authorization']
            try:
              user = User.objects.get(access_token=access_token)
            except User.DoesNotExist:
              user = None
              return JsonResponse({'error': 'Unauthorized'}, status=404)
            if user.access_token_created_at is not None:
                if (datetime.datetime.now(timezone.utc) - user.access_token_created_at) > timedelta(hours=24):
                    return JsonResponse({'error': 'Token expired'}, status=401)
                else:
                    return view_func(request, *args, **kwargs)
            else:
                return JsonResponse({'error': 'Unauthorized'}, status=404)
        else:
            return JsonResponse({'error': 'Unauthorized'}, status=404)
    return wrapper