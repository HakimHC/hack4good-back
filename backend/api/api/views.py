from django.http import JsonResponse
from rest_framework.decorators import api_view
import api.settings as settings
import requests
import json


@api_view(['PUT'])
def set_user_settings(request, *args, **kwargs):
    required_fields = [
        'height',
        'weight',
        'age',
        'sex',
        'physical_activity',
        'vegan_or_vegetarian',
        'allergies'
    ]

    body: dict = request.data
    missing_fields = set(required_fields) - set(body.keys())

    if missing_fields:
        return JsonResponse({
            "status": 403,
            "message": f"Missing required information: {missing_fields}"
        }, status=403)

    settings.USER_OPTIONS = body

    return JsonResponse({
        "status": 200,
        "message": "User information successfully updated",
        "data": settings.USER_OPTIONS
    }, status=200)


@api_view(['GET'])
def get_user_settings(request, *args, **kwargs):
    return JsonResponse(settings.USER_OPTIONS)


@api_view(['POST'])
def search(request, *args, **kwargs):
    try:
        data = request.data
        print(f'Data: {data}')
        response = requests.post('http://langchain:8080', json=data)
        print(response.json())
        our_response = JsonResponse(response.json())
        return our_response
    except Exception as e:
        print(e)
        return JsonResponse({})
    # return JsonResponse({})
