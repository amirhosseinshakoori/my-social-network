from django.shortcuts import render ,redirect ,get_object_or_404
from django.contrib import messages
from .models import Profile ,Tweet
from .forms import TweetForm ,SignUpForm,ProfilePicForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


# Create your views here.

def home(request):
	if request.user.is_authenticated:
		form = TweetForm(request.POST or None)
		if request.method == "POST":
			if form.is_valid():
				tweet = form.save(commit=False)
				tweet.user = request.user
				tweet.save()
				messages.success(request, ("Your Tweet Has Been Posted!"))
				return redirect('home')
		
		Tweets = tweet.objects.all().order_by("-created_at")
		return render(request, 'home.html', {"Tweets":Tweets, "form":form})
	else:
		Tweets = tweet.objects.all().order_by("-created_at")
		return render(request, 'home.html', {"Tweets":Tweets})

def profile_list(request):
	if request.user.is_authenticated:
		profiles = Profile.objects.exclude(user=request.user)
		return render(request, 'profile_list.html', {"profiles":profiles})
	else:
		messages.success(request, ("You Must Be Logged In To View This Page..."))
		return redirect('home')
	

def profile(request, pk):
	if request.user.is_authenticated:
		profile = Profile.objects.get(user_id=pk)
		Tweets = Tweet.objects.filter(user_id=pk).order_by("-created_at")

		if request.method == "POST":
			current_user_profile = request.user.profile
			action = request.POST['follow']
			if action == "unfollow":
				current_user_profile.follows.remove(profile)
			elif action == "follow":
				current_user_profile.follows.add(profile)
			current_user_profile.save()



		return render(request, "profile.html", {"profile":profile, "Tweets":Tweets})
	else:
		messages.success(request, ("You Must Be Logged In To View This Page..."))
		return redirect('home')	
	

def login_user(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, ("You Have Been Logged In!  Get TweetING!"))
			return redirect('home')
		else:
			messages.success(request, ("There was an error logging in. Please Try Again..."))
			return redirect('login')

	else:
		return render(request, "login.html", {})


def logout_user(request):
	logout(request)
	messages.success(request, ("You Have Been Logged Out. Sorry to Tweet You Go..."))
	return redirect('home')

def register_user(request):
	form = SignUpForm()
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']

			user = authenticate(username=username, password=password)
			login(request,user)
			messages.success(request, ("You have successfully registered! Welcome!"))
			return redirect('home')
	
	return render(request, "register.html", {'form':form})

def update_user(request):
	if request.user.is_authenticated:
		current_user = User.objects.get(id=request.user.id)
		profile_user = Profile.objects.get(user__id=request.user.id)
		user_form = SignUpForm(request.POST or None, request.FILES or None, instance=current_user)
		profile_form = ProfilePicForm(request.POST or None, request.FILES or None, instance=profile_user)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()

			login(request, current_user)
			messages.success(request, ("Your Profile Has Been Updated!"))
			return redirect('home')

		return render(request, "update_user.html", {'user_form':user_form, 'profile_form':profile_form})
	else:
		messages.success(request, ("You Must Be Logged In To View That Page..."))
		return redirect('home')
	


def tweet_like(request, pk):
	if request.user.is_authenticated:
		tweet = get_object_or_404(Tweet, id=pk)
		if tweet.likes.filter(id=request.user.id):
			tweet.likes.remove(request.user)
		else:
			tweet.likes.add(request.user)
		
		return redirect(request.META.get("HTTP_REFERER"))


	else:
		messages.success(request, ("You Must Be Logged In To View That Page..."))
		return redirect('home')
	

def tweet_show(request, pk):
	tweet = get_object_or_404(Tweet, id=pk)
	if tweet:
		return render(request, "show_tweet.html", {'tweet':tweet})
	else:
		messages.success(request, ("That tweet Does Not Exist..."))
		return redirect('home')	