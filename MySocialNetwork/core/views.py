from django.shortcuts import render ,redirect
from django.contrib import messages
from .models import Profile ,Tweet
from .forms import TweetForm
# Create your views here.

def home(request):
	if request.user.is_authenticated:
		form = TweetForm(request.POST or None)
		if request.method == "POST":
			if form.is_valid():
				Tweet = form.save(commit=False)
				Tweet.user = request.user
				Tweet.save()
				messages.success(request, ("Your Tweet Has Been Posted!"))
				return redirect('home')
		
		Tweets = Tweet.objects.all().order_by("-created_at")
		return render(request, 'home.html', {"Tweets":Tweets, "form":form})
	else:
		Tweets = Tweet.objects.all().order_by("-created_at")
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