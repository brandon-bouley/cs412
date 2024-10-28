from django.db import models
from django.urls import reverse

class Profile(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    city = models.CharField(max_length=50)
    email = models.EmailField()
    profile_image_url = models.URLField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_status_messages(self):
        return self.statusmessage_set.all().order_by('-timestamp')

    def get_absolute_url(self):
        return reverse('show_profile', kwargs={'pk': self.pk})
    
    def get_friends(self): # New for Assignment 8
        friends = Friend.objects.filter(models.Q(profile1=self) | models.Q(profile2=self))
        friend_profiles = []
        for friend in friends:
            if friend.profile1 == self:
                friend_profiles.append(friend.profile2)
            else:
                friend_profiles.append(friend.profile1)
        return friend_profiles

    def add_friend(self, other):
        if self != other:
            if not Friend.objects.filter(models.Q(profile1=self, profile2=other) | models.Q(profile1=other, profile2=self)).exists():
                Friend.objects.create(profile1=self, profile2=other)

    def get_friend_suggestions(self):
        all_profiles = Profile.objects.exclude(pk=self.pk)
        current_friends = self.get_friends()
        suggestions = [profile for profile in all_profiles if profile not in current_friends]
        return suggestions
    
    def get_news_feed(self):
        friends = self.get_friends()
        news_feed = StatusMessage.objects.filter(profile__in=friends).order_by('-timestamp')
        return news_feed

    
    
    

    

class StatusMessage(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f"Status by {self.profile.first_name} at {self.timestamp}"

    def get_images(self):
        return self.image_set.all()

class Image(models.Model):
    image_file = models.ImageField(upload_to='images/')
    timestamp = models.DateTimeField(auto_now_add=True)
    status_message = models.ForeignKey(StatusMessage, on_delete=models.CASCADE)

    def __str__(self):
        return f"Image for {self.status_message} at {self.timestamp}"

class Friend(models.Model): # New for Assignment 8
    profile1 = models.ForeignKey(Profile, related_name='profile1', on_delete=models.CASCADE)
    profile2 = models.ForeignKey(Profile, related_name='profile2', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.profile1.first_name} {self.profile1.last_name} & {self.profile2.first_name} {self.profile2.last_name}"