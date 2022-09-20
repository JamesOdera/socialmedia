from django.contrib import admin
from .models import *


class PostAdmin(admin.ModelAdmin):
    list_display = ('author',)
    list_filter = ('created', 'updated')
    search_fields = ('author__username',)
    date_hierarchy = ('created')
    
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'birth_date', 'location', 'photo', 'bio')
    
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'reply', 'content', 'timestamp')
    
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('notification_type', 'to_user', 'from_user', 'post', 'comment', 'date', 'user_has_seen')
    
class ThreadModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'receiver')
    
class MessageModelAdmin(admin.ModelAdmin):
    list_display = ('thread', 'sender_user', 'receiver_user', 'body', 'image', 'date', 'is_read')

admin.site.register(Post, PostAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(ThreadModel, ThreadModelAdmin)
admin.site.register(MessageModel, MessageModelAdmin)