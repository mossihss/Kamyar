from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from accounts.models import CustomUser

@api_view(['GET'])
def hello(request):
    return Response({"message": "API is working 🚀"})

@api_view(['POST'])
def api_signup(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if not username or not email or not password:
        return Response({'error': 'تمام فیلدها الزامی هستند'}, status=400)

    if CustomUser.objects.filter(username=username).exists():
        return Response({'error': 'این نام کاربری قبلاً ثبت شده'}, status=400)

    user = CustomUser.objects.create_user(username=username, email=email, password=password)
    user.is_active = True
    user.save()

    return Response({'message': 'ثبت‌نام با موفقیت انجام شد ✅'}, status=201)


@api_view(['POST'])
def api_login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)
    if user is not None:
        return Response({'message': 'ورود موفقیت‌آمیز ✅', 'username': user.username})
    else:
        return Response({'error': 'نام کاربری یا رمز اشتباه است'}, status=401)
