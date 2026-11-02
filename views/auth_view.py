import secrets
import time

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from lore.models import UserProfileModel
from django.core.exceptions import ValidationError

OTP_EXPIRE = 10 * 60
MAX_ATTEMPTS = 5
RESEND_COOLDOWN = 60


#==============Register View================#
def register_view(request):

    if request.method == 'POST':

        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if not username or not email or not password or not confirm_password:
            messages.error(request, 'Please fill in all fields.')
            return redirect('account')

        try:
            validate_email(email)
            
        except ValidationError:
            
            messages.error(request, 'Please enter a valid email address.')
            return redirect('account')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('account')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('account')

        if User.objects.filter(email__iexact=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('account')

        try:
            validate_password(password)
            
        except Exception as e:
            
            messages.error(request, e.messages[0])
            return redirect('account')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        
        UserProfileModel.objects.create(user=user)

        user.is_active = False
        user.save()

        otp = str(secrets.randbelow(900000) + 100000)

        html_message = render_to_string(
            'website/otp_mail.html',
            {
                'otp': otp,
                'user': user,
            }
        )
        try:
            sent = send_mail(
                subject='AG-Enterprise Verification Code',
                message=f'Your verification code is {otp}',
                from_email=None,
                recipient_list=[email],
                html_message=html_message,
                )
            
            if sent != 1:
                raise Exception('Email could not be sent.')

        except Exception:
            
            user.delete()
            messages.error(request,'Unable to sent verification mail.Please try again.')
            return redirect('account')

        request.session['otp_user_id'] = user.id
        request.session['otp_code'] = otp
        request.session['otp_time'] = int(time.time())
        request.session['otp_attempts'] = 0
        request.session['otp_last_sent'] = int(time.time())
        
        messages.success(request, 'Verification code has been sent to your email.')

        return redirect('verify_otp')

    return render(request, 'website/account.html')


#==============Verify OTP=================#
def verify_otp(request):

    user_id = request.session.get('otp_user_id')
    otp_code = request.session.get('otp_code')
    otp_time = request.session.get('otp_time')
    attempts = request.session.get('otp_attempts', 0)

    if not user_id or not otp_code or not otp_time:
        messages.error(request, 'Verification session expired.')
        return redirect('account')

    if request.method == 'POST':

        otp = request.POST.get('otp', '').strip()

        if int(time.time()) - otp_time > OTP_EXPIRE:
            messages.error(request, 'OTP has expired. Please request a new code.')
            return redirect('verify_otp')

        if attempts >= MAX_ATTEMPTS:
            messages.error(request, 'Too many incorrect attempts.')
            return redirect('account')

        # Check OTP
        if otp != otp_code:

            request.session['otp_attempts'] = attempts + 1

            messages.error(request, 'Invalid verification code.')
            return redirect('verify_otp')

        # Create account
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            messages.error(request, 'User not found.')
            return redirect('account')

        user.is_active = True
        user.save()

        # Clear OTP session
        del request.session['otp_user_id']
        del request.session['otp_code']
        del request.session['otp_time']
        del request.session['otp_attempts']
        del request.session['otp_last_sent']

        messages.success(request, 'Account verified successfully. You can now login.')

        return redirect('account')

    return render(request, 'website/verify_otp.html')


#===============OTP resend================#
@require_POST
def resend_otp(request):

    user_id = request.session.get('otp_user_id')

    if not user_id:
        messages.error(request, 'Verification session expired.')
        return redirect('account')

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, 'User not found.')
        return redirect('account')

    last_sent = request.session.get('otp_last_sent', 0)

    # OTP resend seconds cooldown
    if int(time.time()) - last_sent < RESEND_COOLDOWN:
        messages.error(request, 'Please wait before requesting another code.')
        return redirect('verify_otp')

    # New OTP
    otp = str(secrets.randbelow(900000) + 100000)

    # Send email
    html_message = render_to_string('website/otp_mail.html',{'otp': otp,'user': user,})

    try:
        sent = send_mail(
                subject='AG-Enterprise New Verification Code',
                message=f'Your new verification code is {otp}',
                from_email=None,
                recipient_list=[user.email],
                html_message=html_message,
            )
        
        if sent != 1:
            raise Exception('Email could not be sent.')
        
    except Exception:
        messages.error(request,'Unable to sent verification code.')
        return redirect('verify_otp')
    
    request.session['otp_code'] = otp
    request.session['otp_time'] = int(time.time())
    request.session['otp_attempts'] = 0
    request.session['otp_last_sent'] = int(time.time())

    messages.success(request, 'A new verification code has been sent.')

    return redirect('verify_otp')


#==============Login View=================#
def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        if not username or not password:
            messages.error(request, 'Please enter username/email and password.')
            return redirect('account')

        # Login by username
        user = authenticate(
            request,
            username=username,
            password=password
        )

        # Login by email
        if user is None:
            try:
                email_user = User.objects.get(email__iexact=username)

                user = authenticate(
                    request,
                    username=email_user.username,
                    password=password
                )
            except User.DoesNotExist:
                user = None

        if user is None:
            messages.error(request, 'Invalid username/email or password.')
            return redirect('account')

        UserProfileModel.objects.get_or_create(user = user)
        
        login(request, user)
          
        if user.is_superuser or user.is_staff:
            messages.success(request, f'Welcome back {user.username}')
            return redirect('dashboard')

        messages.success(request,f'Welcome back {user.username}')
        return redirect('home')
    
    if request.GET.get('next'):
        messages.warning(request,'Please login first to access this page.')
        
    return render(request, 'website/account.html')


#=================Logout Veiw==================#
@require_POST
def logout_view(request):

    logout(request)

    messages.success(request, 'You have been logged out.')
    return redirect('home')