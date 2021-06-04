from django.shortcuts import render,redirect
from .forms import RegistrationForm,UserUpdateForm,ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
from .models import Profile

def user_registration(request):
    if request.user.is_authenticated:
        return redirect('/home/')
    else:    
        if request.method == "POST":
            form = RegistrationForm(request.POST,request.FILES)
            if form.is_valid():
                data = form.cleaned_data
                if data['password'] == data['confirm_password']:
                    obj = form.save(commit=False)
                    obj.set_password(obj.password)
                    obj.save()
                    username = form.cleaned_data.get('username')
                    messages.success(request, f'Account created for {username}!')
                    return redirect('login')
                else:
                    return render(request, "users/user_registration.html", {'form':form,'note':'Password not matched'})
        else:
            form = RegistrationForm()
            context= {
                'form':form
                }
    return render(request, "users/user_registration.html",context)


def user_login(request):
    if request.user.is_authenticated:
        return redirect('/home/')
    else:  
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request,user)
                return redirect('home')
            else:
                messages.warning(request, 'Invalid username or password!')
                return render(request, "users/user_login.html")
        else:
            return render(request, "users/user_login.html")


def user_logout(request):
    logout(request)
    return render(request,"users/user_logout.html")


@login_required
def profile(request):
    profile = Profile(user=request.user)
    if request.method == 'POST':   
        u_form = UserUpdateForm(request.POST, instance=request.user,) 
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)  

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')

    else:
        profile = Profile(user=request.user)
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile)

    context = { 
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/User_profile.html', context)



