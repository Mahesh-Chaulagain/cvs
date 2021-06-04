from django.shortcuts import render,redirect,get_object_or_404
from .models import Position,ControlVote,Candidate
from .forms import PositionForm,CandidateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


@login_required
def home(request):
    voters=User.objects.all().count()
    positions=Position.objects.all().count()
    candidates=Candidate.objects.all().count()
    context={
        'voters':voters,
        'positions':positions,
        'candidates':candidates,
    }
    return render(request, "election/home.html",context)

    
@login_required
def position(request):
    positions=Position.objects.all()
    context={
        'positions':positions
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
            return redirect('/add_position/')

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
    messages.warning(request,f'Position:{position}removed')
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
            return redirect('/result/')
        else:
            messages.success(request, 'You already voted this position.')
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
    results = Candidate.objects.all().order_by('position','-total_vote')
    context={
        'results':results
    }
    return render(request, "election/result.html", context)



    



