from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import RegisterUserSerializer
from .models import User


class RegisterUserView(APIView):
    
    def post(self, request):
        ser = RegisterUserSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save()

        return Response('Successfully registration')
    

@api_view(['GET'])
def activate_view(request, activation_code):
    user = get_object_or_404(User, activation_code=activation_code)
    user.is_active = True
    user.activation_code = None
    user.save()

    return Response('Congratulations!', status=200)