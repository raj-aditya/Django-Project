from django.shortcuts import render
from django.http import HttpResponse
from .models import User
from .serializers import UserSerializer
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.crypto import get_random_string
import datetime
from datetime import timezone
from .decorators import check_authorization




# Create your views here.
@csrf_exempt
def user_registration(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data['email']
        try:
          user = User.objects.get(email=email)
        except User.DoesNotExist:
          user = None
        if user != None:
            return JsonResponse({'error': 'User Already Exist'}, status=401)
        else:
            serializer = UserSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=200)
            else:
                return JsonResponse(serializer.errors, status=400)
    else:
        return JsonResponse({'error': 'Invalid Method'}, status=404)
        
@csrf_exempt
def user_login(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data['email']
        password = data['password']
        try:
          user = User.objects.filter(email=email, password=password).first()
        except User.DoesNotExist:
          user = None
        if user is not None:
          create_token(user)
          data = dict()
          data['access_token']= user.access_token
          return JsonResponse(data, safe=False, status=200)
        else:
          return JsonResponse({'error': 'Email or Password is Incorrect'}, status=401)
    else:
        return JsonResponse({'error': 'Invalid Method'}, status=404)

def create_token(user):
  unique_id = get_random_string(length=32)
  user.access_token = unique_id
  user.access_token_created_at = datetime.datetime.now(timezone.utc) 
  user.save()
  return user.access_token

@csrf_exempt
@check_authorization
def user_index(request):
    if (request.method != 'GET'):
        return HttpResponse("Invalid Method", status=404)
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return JsonResponse(serializer.data, safe=False)

@csrf_exempt
@check_authorization
def user_detail(request, id):
  try:
        user = User.objects.get(id=id)
  except:
        return JsonResponse({'error': 'user_not_found'}, status=404)

  # GET
  if request.method == 'GET':
      serializer = UserSerializer(user)
      return JsonResponse(serializer.data)
  # PUT
  elif request.method == 'PUT':
      data = json.loads(request.body)
      serializer = UserSerializer(user, data=data)
      if serializer.is_valid():
          serializer.save()
          return JsonResponse(serializer.data, status=200)
      else:
          return JsonResponse(serializer.errors, status=400)
  # PATCH
  elif request.method == "PATCH":
      data = json.loads(request.body)
      serializer = UserSerializer(user, data=data, partial=True)
      if serializer.is_valid():
          serializer.save()
          return JsonResponse(serializer.data, status=200)
      else:
          return JsonResponse(serializer.errors, status=400)
    # DELETE
  elif request.method == 'DELETE':
      user.delete()
      return JsonResponse({'message': 'successfully deleted'}, status=204)
  else:
      return JsonResponse({'message': 'Invalid Request'}, status=405)