"""social URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from media import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('index/', include('media.urls')),
    # USER AUTHENTICATION
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('register/', views.register, name='register'),
    # POSTS LIKE
    path('like/', views.like_post, name='like_post'),
    path('follow/', views.follow_user, name='follow_user'),
    # path('profile/<int:id>/followers/add', views.addFollower, name='add-follower'),
    # path('profile/<int:id>/followers/remove', views.removeFollower, name='remove-follower'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
