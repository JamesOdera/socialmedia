from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('follow/', views.follow, name='follow'),
    path('app/<int:id>/<slug>/', views.post_detail, name='post_detail'),
    path('post_create/', views.post_create, name='post_create'),
    path('<int:id>/post_edit/', views.post_edit, name='post_edit'),
    path('<int:id>/post_delete/', views.post_delete, name='post_delete'),
    path('profile/<int:id>/', views.profile, name='profile'),
    path('profile/<int:id>/followers/', views.ListFollowers, name='list-followers'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('notification/<int:notification_id>/post/<int:post_id>/<post_slug>', views.PostNotification, name='post-notification'),
    path('notification/<int:notification_id>/thread/<int:object_id>/', views.ThreadNotification, name='thread-notification'),
    path('notification/<int:notification_id>/profile/<int:profile_id>', views.FollowNotification, name='follow-notification'),
    path('notification/delete/<int:notification_id>', views.RemoveNotification, name='notification-delete'),
    path('inbox/', views.ListThreads.as_view(), name='inbox'),
    path('inbox/create-thread/', views.CreateThread.as_view(), name='create-thread'),
    path('inbox/<int:id>/', views.ThreadView.as_view(), name='thread'),
    path('inbox/<int:id>/create-message/', views.CreateMessage.as_view(), name='create-message'),
]