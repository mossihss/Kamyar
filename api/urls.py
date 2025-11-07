from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.urls import path

@api_view(['GET'])
def hello(request):
    return Response({"message": "API is working 🚀"})

urlpatterns = [
    path('', hello),
]

