from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from datetime import datetime
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
import math
from cloudinary.models import CloudinaryField


class Post(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User,  on_delete=models.CASCADE)
    body = models.TextField(max_length=1000)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    slug = models.SlugField(max_length=120)
    image = CloudinaryField('image')

    class Meta:
        ordering = ['-id']
        
    def total_likes(self):
        return self.likes.count()
    
    def likes_as_flat_user_id_list(self):
        return self.likes.values_list('id', flat=True)

    def get_absolute_url(self):
        return reverse('post_detail', args=[self.id, self.slug])

    def whenpublished(self):
        now = timezone.now()

        diff = now - self.created

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds = diff.seconds

            if seconds == 1:
                return "NOW"

            else:
                return str(seconds) + " SEC"

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes = math.floor(diff.seconds/60)

            if minutes == 1:
                return str(minutes) + " MIN"

            else:
                return str(minutes) + " MIN"

        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours = math.floor(diff.seconds/3600)

            if hours == 1:
                return str(hours) + " HOUR"

            else:
                return str(hours) + " HOURS"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days = diff.days

            if days == 1:
                return str(days) + " DAY"

            else:
                return str(days) + " DAYS AGO"

        if diff.days >= 30 and diff.days < 365:
            months = math.floor(diff.days/30)

            if months == 1:
                return str(months) + " MONTH AGO"

            else:
                return str(months) + " MONTHS AGO"

        if diff.days >= 365:
            years = math.floor(diff.days/365)

            if years == 1:
                return str(years) + " YEAR"

            else:
                return str(years) + " YEARS AGO"


@receiver(pre_save, sender=Post)
def pre_save_slug(sender, **kwargs):
    slug = slugify(kwargs['instance'].author)
    kwargs['instance'].slug = slug
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    photo = CloudinaryField('image-profile')
    # photo = models.ImageField(upload_to='profile_pictures', default='default.jpg', blank=True, null=True)
    followers = models.ManyToManyField(User, related_name='followers', blank=True)

    def __str__(self):
        return "Profile of User {}".format(self.user.username)
    
    def total_followers(self):
        return self.followers.count()
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reply = models.ForeignKey('Comment', null=True, related_name='replies', on_delete=models.CASCADE)
    content = models.TextField(max_length=160)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}'.format(str(self.user.username))

class Notification(models.Model):
    notification_type = models.IntegerField()
    to_user = models.ForeignKey(User, related_name='notification_to', on_delete=models.CASCADE, null=True)
    from_user = models.ForeignKey(User, related_name='notification_from', on_delete=models.CASCADE, null=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    thread = models.ForeignKey('ThreadModel', on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    user_has_seen = models.BooleanField(default=False)
    
    def __str__(self):
        return '{}'.format(str(self.notification_type))
    
class ThreadModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    
class MessageModel(models.Model):
    thread = models.ForeignKey('ThreadModel', on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    sender_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    receiver_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    body = models.TextField(max_length=500)
    image = CloudinaryField('image')
    date = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)
    
    # class Meta:
    #     ordering = ['-id']
