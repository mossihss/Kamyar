from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm

# برای ایمیل فعال‌سازی
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from .models import CustomUser



# ثبت نام
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # تا وقتی ایمیل تأیید نشده، غیرفعال می‌مونه
            user.save()

            # ارسال ایمیل فعال‌سازی
            current_site = get_current_site(request)
            subject = 'فعال‌سازی حساب کاربری شما'
            message = render_to_string('accounts/activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            send_mail(subject, message, 'hoseiniiiiiimohsen@gmail.com', [user.email])

            return render(request, 'accounts/check_email.html')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})


# ورود
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'accounts/login.html', {'error': 'نام کاربری یا رمز اشتباه است'})
    return render(request, 'accounts/login.html')


# خانه
@login_required
def home_view(request):
    return render(request, 'accounts/home.html')


# خروج
def logout_view(request):
    logout(request)
    return redirect('login')


# فعال‌سازی از طریق لینک ایمیل
def activate_view(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.is_verified = True  # فیلد جدیدی که تو مدل گذاشتیم
        user.save()
        return redirect('login')
    else:
        return render(request, 'accounts/activation_failed.html')

