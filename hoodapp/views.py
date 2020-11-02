from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import Profile,Neighborhood,Business,Join,Post,
from .forms import NewProfileForm,AddBusinessForm,AddHoodForm,AddPostForm
import datetime as dt
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
# from .models import *
# from .forms import *
# from .email import *


def homepage(request):
    if request.user.is_authenticated:
        if Join.objects.filter(user_id=request.user).exists():
            hood = Neighborhood.objects.get(pk=request.user.join.hood_id.id)
            posts = Post.objects.filter(post_hood=request.user.join.hood_id.id)
            businesses = Business.objects.filter(
                biz_hood=request.user.join.hood_id.id)
            return render(request, 'current_hood.html', {"hood": hood, "businesses": businesses, "posts": posts})
        else:
            hoods = Neighborhood.all_neighborhoods()
            return render(request, 'index.html', {"hoods": hoods})
    else:
        hoods = Neighborhood.all_neighborhoods()
        return render(request, 'index.html', {"hoods": hoods})


@login_required(login_url='/accounts/login/')
def add_profile(request):
    current_user = request.user
    if request.method == 'POST':
        form = NewProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = current_user
            profile.save()
        return redirect('homepage')

    else:
        form = NewProfileForm()
    return render(request, 'new_profile.html', {"form": form})


@login_required(login_url='/accounts/login/')
def add_hood(request):
    current_user = request.user
    if request.method == 'POST':
        form = AddHoodForm(request.POST, request.FILES)
        if form.is_valid():
            hood = form.save(commit=False)
            hood.user_profile = current_user
            hood.save()
        return redirect('homepage')

    else:
        form = AddHoodForm()
    return render(request, 'new_hood.html', {"form": form})


@login_required(login_url='/accounts/login/')
def add_business(request):
    current_user = request.user
    if request.method == 'POST':
        form = AddBizForm(request.POST, request.FILES)
        if form.is_valid():
            biz = form.save(commit=False)
            biz.biz_owner = current_user
            biz.biz_hood = request.user.join.hood_id
            biz.save()
        return redirect('homepage')

    else:
        form = AddBizForm()
    return render(request, 'new_business.html', {"form": form})


@login_required(login_url='/accounts/login/')
def join_hood(request, hood_id):
    '''
    This view function will implement adding 
    '''
    neighborhood = Neighborhood.objects.get(pk=hood_id)
    if Join.objects.filter(user_id=request.user).exists():

        Join.objects.filter(user_id=request.user).update(hood_id=neighborhood)
    else:

        Join(user_id=request.user, hood_id=neighborhood).save()

    return redirect('homepage')


@login_required(login_url='/accounts/login/')
def leave_hood(request, hood_id):
    '''
    This function will delete a neighbourhood instance in the join table
    '''
    if Join.objects.filter(user_id=request.user).exists():
        Join.objects.get(user_id=request.user).delete()
        # messages.error(request, 'You have left this awesome neighborhood ;-(')
        return redirect('homepage')


@login_required(login_url='/accounts/login/')
def user_profile(request, username):
    profile = User.objects.get(username=username)
    try:
        profile_info = Profile.get_profile(profile.id)
    except:
        profile_info = Profile.filter_by_id(profile.id)
    businesses = Business.get_profile_businesses(profile.id)
    title = f'@{profile.username}'
    return render(request, 'profile.html', {'title': title, 'profile': profile, 'profile_info': profile_info, 'businesses': businesses})


@login_required(login_url='/accounts/login/')
def add_post(request):
    current_user = request.user
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.poster = current_user
            post.post_hood = request.user.join.hood_id
            post.save()
        return redirect('homepage')

    else:
        form = AddPostForm()
    return render(request, 'new_post.html', {"form": form})

# def view_biz(request, biz_hood):
#     current_user = request.user
#     hood=Neighborhood.objects.get(id=biz_hood)
#     businesses= Business.get_neighborhood_businesses(biz_hood = hood.id)

#     return redirect (request, 'businesses.html', {"business":businesses})


def search_results(request):

    if 'business' in request.GET and request.GET["business"]:
        search_term = request.GET.get("business")
        business_results = Business.search_by_name(search_term)
        message = f"{search_term}"

        return render(request, 'search.html', {"message": message, "businesses": business_results})

    else:
        message = "Please enter a search term"
        return render(request, 'search.html', {"message": message})