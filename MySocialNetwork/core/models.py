from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField("self", related_name='followed_by',symmetrical=False,blank=True)
    date_modified = models.DateTimeField(User, auto_now=True)	
    profile_image = models.ImageField(null=True,blank=True,upload_to="images/")
    profile_bio = models.CharField(null=True, blank=True, max_length=500)
    homepage_link = models.CharField(null=True, blank=True, max_length=100)
    facebook_link = models.CharField(null=True, blank=True, max_length=100)
    instagram_link = models.CharField(null=True, blank=True, max_length=100) 
    linkedin_link = models.CharField(null=True, blank=True, max_length=100) 
    
    
    def __str__(self) -> str:
        return self.user.username
    

def create_profile(sender, instance, created, **kwarge):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        user_profile.follows.set([instance.profile.id])

post_save.connect(create_profile,sender=User)

class Tweet(models.Model):
    user = models.ForeignKey(User, related_name="tweets",on_delete=models.DO_NOTHING)
    body = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="tweet_like", blank=True)


    def number_of_likes(self):
        return self.likes.count()
   
    def __str__(self) -> str:
        return (
            f"{self.user}"
            f"{self.created_at}"
            f"{self.body}"
        )