from django.http.response import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

@login_required
def home(request):
    voters=User.objects.all().exclude(is_superuser=True,is_staff=True).count()
    positions=Position.objects.all().count()
    candidates=Candidate.objects.all().count()
    voted=ControlVote.objects.all().count()
    context={
        'voters':voters,
        'positions':positions,
        'candidates':candidates,
        'voted':voted,
    }
    return render(request, "election/home.html",context)

    
@login_required
def position(request):
    positions=Position.objects.all()
    result_date = ElectionDate.objects.first()
    result_date_value = result_date.result_date if result_date else None
    context={
        'positions':positions,
        "result_date": result_date_value
    }
    return render(request, "election/position.html", context)


@login_required
def add_position(request):
    if request.method=="POST":
        p_form=PositionForm(request.POST)
        if p_form.is_valid():
            post=p_form.save()
            post.save()
            title=p_form.cleaned_data.get('title')
            messages.success(request,f'Position:{title} added')
            return redirect('/position/',pk=post.pk)
        else:
            messages.warning(request, 'Position already exists')
            return redirect('add_position')

    context={
        'p_form':PositionForm()
    }
    return render(request,'election/add_position.html',context)


@login_required
def edit_position(request,pk):
    instance=get_object_or_404(Position,pk=pk)
    if request.method=='POST':
        form=PositionForm(request.POST,instance=instance)
        if form.is_valid():
            post=form.save()
            post.save()
            return redirect('/position/',pk=post.pk)
    else:
        context={
            'form':PositionForm(instance=instance)
        }
        return render(request,'election/edit_position.html',context)


@login_required
def delete_position(request,pk):
    position=get_object_or_404(Position,pk=pk)
    position.delete()
    messages.warning(request,f'Position:{position} removed')
    return redirect('/position/')


@login_required
def candidate(request,pk):
    obj = get_object_or_404(Position, pk=pk)
    if request.method == "POST":

        temp = ControlVote.objects.get_or_create(user=request.user, position=obj)[0]

        if temp.status == False:
            temp2 = Candidate.objects.get(pk=request.POST.get(obj.title))
            temp2.total_vote += 1
            temp2.save()
            temp.status = True
            temp.save()
            messages.success(request,f'Vote done to {obj.title}')
            return redirect('position')
        else:
            messages.warning(request, 'You already voted this position.')
            context={
                'obj':obj
            }
            return render(request, 'election/candidate.html', context)
    else:
        context={
                'obj':obj
            }
        return render(request, 'election/candidate.html',context)


@login_required
def add_candidate(request):
    if request.method=="POST":
        c_form=CandidateForm(request.POST,request.FILES)
        if c_form.is_valid():
            post=c_form.save()
            post.save()
            name=c_form.cleaned_data.get('name')
            messages.success(request,f'Candidate:{name} added')
            return redirect('candidate_detail',pk=post.pk)
        else:
            messages.warning(request, 'Candidate already exists')
            return redirect('/add_candidate/')

    context={
        'c_form':CandidateForm()
    }
    return render(request,'election/add_candidate.html',context)


@login_required
def candidate_detail(request, pk):
    details = get_object_or_404(Candidate, pk=pk)
    context={
        'details':details
    }
    return render(request, "election/candidate_detail.html", context)


@login_required
def delete_candidate(request,pk):
    candidate=get_object_or_404(Candidate,pk=pk)
    candidate.delete()
    messages.warning(request,f'Candidate:{candidate} deleted')
    return redirect('/position/')    


@login_required
def edit_candidate(request,pk):
    instance=get_object_or_404(Candidate,pk=pk)
    if request.method=='POST':
        e_form=CandidateForm(request.POST,request.FILES,instance=instance)
        if e_form.is_valid():
            post=e_form.save()
            post.save()
            return redirect('candidate_detail',pk=post.pk)
    else:
        context={
            'e_form':CandidateForm(instance=instance)
        }
        return render(request,'election/edit_candidate.html',context)        


@login_required   
def result(request):
    result = Candidate.objects.all().order_by('position','-total_vote')
    result_date = ElectionDate.objects.first()
    page = request.GET.get('page', 1)
    paginator = Paginator(result, 5)
    result_date_value = result_date.result_date if result_date else None
    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        results = paginator.page(1)
    except EmptyPage:
        results = paginator.page(paginator.num_pages)
    context={
        'results':results,
        "result_date": result_date_value
    }
    return render(request, "election/result.html", context)

def search_result(request):
    qur=request.GET.get('search')
    results=[item for item in Candidate.objects.all().order_by('position','-total_vote') if qur in item.name.lower() or qur in item.position.title.lower()]
    return render(request,'election/search.html',{'results':results})

def view_log(request):
    logs=ControlVote.objects.all()
    return render(request,'election/activity_logs.html',{'logs':logs})
    
@login_required
def voters(request):
    voter=User.objects.all().order_by('-is_superuser','-is_staff')
    page = request.GET.get('page', 1)
    paginator = Paginator(voter, 5)
    try:
        voters = paginator.page(page)
    except PageNotAnInteger:
        voters = paginator.page(1)
    except EmptyPage:
        voters = paginator.page(paginator.num_pages)
    context={
        'voters':voters,
    }
    return render(request,'election/voters_list.html',context)

@login_required
def update_voter(request,pk):
    instance=get_object_or_404(User,pk=pk)
    if request.method=='POST':
        v_form=CustomUserChangeForm(request.POST,request.FILES,instance=instance)
        if v_form.is_valid():
            post=v_form.save()
            post.save()
            return redirect('/voters/',pk=post.pk)
    else:
        context={
            'v_form':CustomUserChangeForm(instance=instance)
        }
        return render(request,'election/update_voter.html',context)

def search_voter(request):
    qur=request.GET.get('search').lower()
    voters=[item for item in User.objects.all() if qur in item.username.lower() or qur in item.email.lower()]
    return render(request,'election/search.html',{'voters':voters})

@login_required
def add_email(request):
    if request.method=='POST':
        form=EmailRegistrationForm(request.POST)
        if form.is_valid():
            obj=form.save()
            obj.save()
            email=request.POST.get('email')
            messages.success(request,f'{email} added successfully')
        else:
            messages.warning(request,'email already exists')
            return redirect('/add_email/')
    form=EmailRegistrationForm()
    email=VerifiedEmail.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(email, 5)
    try:
        emails = paginator.page(page)
    except PageNotAnInteger:
        emails = paginator.page(1)
    except EmptyPage:
        emails = paginator.page(paginator.num_pages)
    context={
        'form':form,
        'emails':emails
    }
    return render(request,'election/add_email.html',context)

@login_required
def update_email(request,pk):
    instance=get_object_or_404(VerifiedEmail,pk=pk)
    if request.method=='POST':
        form=EmailRegistrationForm(request.POST,instance=instance)
        if form.is_valid():
            post=form.save()
            post.save()
            return redirect('/add_email/',pk=post.pk)
  
    context={
            'form':EmailRegistrationForm(instance=instance)
        }
    return render(request,'election/update_email.html',context)

def search_email(request):
    qur=request.GET.get('search').lower()
    emails=VerifiedEmail.objects.filter(email__contains=qur)
    return render(request,'election/search.html',{'emails':emails})

@login_required
def about(request):
    return render(request,'election/about.html')

@login_required
def set_vote_date(request):
    # Fetch the existing result date or create a new one
    date_instance = ElectionDate.objects.first() or ElectionDate()

    if request.method == "POST":
        d_form = ElectionDateForm(request.POST, instance=date_instance)
        if d_form.is_valid():
            d_form.save()
            messages.success(request, "Vote end date has been set successfully!")
            return redirect("home")
    else:
        d_form = ElectionDateForm(instance=date_instance)

    return render(request, "election/set_vote_date.html", {"d_form": d_form})



    



