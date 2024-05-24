from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .services import *
@csrf_exempt
def identify(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        phone_number = data.get('phoneNumber')

        if not email and not phone_number:
            return JsonResponse({"error": "Either email or phoneNumber must be provided"}, status=400)

        contact = Service.find_or_create_contact(email, phone_number)
        return JsonResponse({"contact": contact}, status=200)

    return JsonResponse({"error": "Invalid request method"}, status=405)