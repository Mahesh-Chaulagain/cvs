from django.http.response import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
from .models import *
from django.core.mail import send_mail
from django .conf import settings
import random
import uuid
from election.models import VerifiedEmail

def user_registration(request):
    if request.user.is_authenticated:
        return redirect('/home/')
    else:    
        if request.method == "POST":
            form = RegistrationForm(request.POST,request.FILES)
            username = request.POST.get('username')
            email = request.POST.get('email')

            try:
                if User.objects.filter(username = username).first():
                    messages.warning(request, 'Username is taken.')
                    return redirect('/register')

                if User.objects.filter(email = email).first():
                    messages.warning(request, 'Email is taken.')
                    return redirect('/register')

                if form.is_valid():
                    data = form.cleaned_data
                    if data['password'] == data['confirm_password']:
                        obj = form.save(commit=False)
                        obj.set_password(obj.password)
                        email=form.cleaned_data.get('email')
                        image=form.cleaned_data.get('image')
                        if VerifiedEmail.objects.filter(email=email).exists():
                            obj.save()
                            auth_token = str(uuid.uuid4())
                            profile_obj = Profile.objects.create(user = obj , auth_token = auth_token,image=image)
                            profile_obj.save()
                            send_mail_after_registration(email , auth_token)
                            return redirect('/token')
                            
                        else:
                            messages.warning(request,'Email not found in college Database-Enter valid email ')
                            return redirect('/register/')

                    else:
                        return render(request, "users/user_registration.html", {'form':form,'note':'Password not matched'})

            except Exception as e:
                        print(e)
          
        form = RegistrationForm()
        context= {
                'form':form
                }
        return render(request, "users/user_registration.html",context)

def success(request):
    return render(request , 'users/success.html')

def token_send(request):
    return render(request , 'users/token_send.html')

def verify(request , auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()
    
        if profile_obj:
            if profile_obj.is_verified:
                messages.warning(request, 'Your account is already verified.')
                return redirect('login')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified.')
            return redirect('login')
        else:
            return redirect('/error')
    except Exception as e:
        print(e)
        return redirect('/')

def error_page(request):
    return  render(request , 'users/error.html')

def send_mail_after_registration(email , token):
    subject = 'Your accounts need to be verified'
    message = f'Hi click the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list )

def user_login(request):
    if request.user.is_authenticated:
        return redirect('/home/')
    
    if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')

            try:

                user = authenticate(request, username=username, password=password)
                get_otp=request.POST.get('otp')

                if get_otp:
                    get_usr=request.POST.get('usr')
                    usr=User.objects.get(username=get_usr)
                    if int(get_otp)==UserOTP.objects.filter(user=usr).last().otp:
                        login(request,usr)
                        return redirect('home')
                    else:
                        messages.warning(request,f"you entered a wrong OTP")
                        return render(request,"users/user_login.html",{'otp':True,'usr':usr})
                
                user_obj = User.objects.filter(username = username).first()
                if user_obj is None:
                    messages.success(request, 'User not found.')
                    return redirect('login')
                    
                profile_obj = Profile.objects.filter(user = user_obj ).first()
                if not profile_obj.is_verified:
                    messages.success(request, 'Profile is not verified check your mail.')
                    return redirect('login')

                if user is not None:
                    usr=User.objects.get(username=username)   
                    user_otp=random.randint(1000,9999)
                    UserOTP.objects.create(user=usr,otp=user_otp)
                    mess=f"Hello {usr.first_name},\nYour OTP is {user_otp}\n Thanks!"
                    send_mail(
                        "Welcome to College Voting System - Verify your email",
                        mess,
                        settings.EMAIL_HOST_USER,
                        [usr.email],
                        fail_silently=False
                    )
                    return render(request, "users/user_login.html",{'otp':True,'usr':usr})
                
                elif not User.objects.filter(username=username).exists():
                    messages.warning(request, 'Invalid username or password!')
                    return render(request, "users/user_login.html")

            except Exception as e:
                        print(e)

    return render(request, "users/user_login.html")


def user_logout(request):
    logout(request)
    return render(request,"users/user_logout.html")


@login_required
def profile(request):
    if request.method == 'POST':   
        u_form = UserUpdateForm(request.POST, instance=request.user)  
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)  

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your profile has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = { 
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/user_profile.html', context)






