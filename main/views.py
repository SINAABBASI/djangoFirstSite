from django.contrib.auth.password_validation import password_changed
from django.http.response import HttpResponse
from main.models import Tutorial
from django.shortcuts import redirect, render
from .models import Tutorial, TutorialCategory, TutorialSeries
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import NewUserForm # from django.http import HttpResponse

# def homepage(request):
#     return HttpResponse("Hello <strong>Sina<strong/>")




def single_slug(request,single_slug):
    categories = [c.category_slug for c in TutorialCategory.objects.all()]
    
    if single_slug in categories:
        matching_series = TutorialSeries.objects.all().filter(tutorial_category__category_slug = single_slug)
        series_url={}
        for m in matching_series.all():
            tutPart = Tutorial.objects.all().filter(tutorial_series__tutorial_series = m.tutorial_series).earliest("tutorial_published")
            series_url[m] = tutPart.tutorial_slug

        return render(
            request,
            template_name="main/category.html",
            context={"tutPart": series_url}            
        )
    
    tutorials = [t.tutorial_slug for t in Tutorial.objects.all()]
    if single_slug in tutorials:
        this_tutorial = Tutorial.objects.get(tutorial_slug = single_slug)
        tutorial_from_series = Tutorial.objects.filter(tutorial_series__tutorial_series = this_tutorial.tutorial_series).order_by("tutorial_published")
        this_tutorial_idx = list(tutorial_from_series).index(this_tutorial)
        return render(
            request,
            "main/tutorial.html",
            context={"tutorial": this_tutorial,
                     "sidebar": tutorial_from_series,
                     "this_tut_idx": this_tutorial_idx}
        )


    return HttpResponse(f"{single_slug} does not corrospond to anything!")

def homepage(request):
    return render(
        request= request,
        template_name= "main/categories.html",
        context= {"categories": TutorialCategory.objects.all},
    )
def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f"New account created: {username}")
            login(request,user)
            return redirect("main:homepage")
        else:
            for msg in form.error_messages:
                messages.error(request,f"{msg}:{form.error_messages[msg]}")
    
    form = NewUserForm()
    return render(
        request,
        "main/register.html",
        context={"form":form}
    )

def login_req(request):
    if request.method == "POST":
        form = AuthenticationForm(request,data = request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                messages.success(request,"Loged in successfully!")
                return redirect("main:homepage")
            else:
                messages.error(request,"Invalid password or username")    
        else:
            messages.error(request,"Invalid password or username")

    form = AuthenticationForm()
    return render(
        request,
        "main/login.html",
        context={"form":form}
    )

def logout_req(request):
    logout(request)
    messages.info(request,"Loged out successfully!")
    return redirect("main:homepage")

