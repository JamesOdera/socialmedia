from django.shortcuts import get_object_or_404, redirect, render
from .models import *
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.views import View
from django.forms import modelformset_factory
from django.template.loader import render_to_string
from django.db.models import Q

def index(request):
    logged_in_user = request.user
    posts = Post.objects.all()
    profile = Profile.objects.filter(
        followers__in=[logged_in_user.id]
    )[0:3]
    notifications = Notification.objects.filter(to_user=request.user.id).exclude(user_has_seen=True).order_by('-date')
    
    query = request.GET.get('q')
    if query:
        posts = Post.objects.filter(
            Q(author__username=query) |
            Q(body__icontains=query)
        )
    
    context = {
        'posts': posts,
        'profile': profile,
        'notifications': notifications,
    }
    return render(request, 'index.html', context)

def follow(request):
    profile = Profile.objects.all().exclude(user=request.user.id)
    follow = Profile.objects.filter(
        followers__in=[request.user.id]
    )
    
    context = {
        'profile': profile,
        'follow': follow,
    }
    return render(request, 'media/follow.html', context)

class ListThreads(View):
    def get(self, request, *args, **kwargs):
        threads = ThreadModel.objects.filter(Q(user=request.user) | Q(receiver=request.user))
        context = {
            'threads': threads,
        }
        return render(request, 'media/inbox.html', context)

class CreateThread(View):
    def get(self, request, *args, **kwargs):
        form = ThreadForm()
        context = {
            'form': form,
        }
        return render(request, 'media/create_thread.html', context)

    def post(self, request, *args, **kwargs):
        form = ThreadForm(request.POST)
        username = request.POST.get('username')
        try:
            receiver = User.objects.get(username=username)
            if ThreadModel.objects.filter(user=request.user, receiver=receiver).exists():
                thread = ThreadModel.objects.filter(user=request.user, receiver=receiver)[0]
                return redirect('thread', id=thread.id)
            elif ThreadModel.objects.filter(user=receiver, receiver=request.user).exists():
                thread = ThreadModel.objects.filter(user=receiver, receiver=request.user)[0]
                return redirect('thread', id=thread.id)
            if form.is_valid():
                thread = ThreadModel(user=request.user, receiver=receiver)
                thread.save()
                return redirect('thread', id=thread.id)
        except:
            messages.error(request, 'User Does Not Exist')
            return redirect('create-thread')

class ThreadView(View):
    def get(self, request, id, *args, **kwargs):
        form = MessageForm()
        thread = ThreadModel.objects.get(id=id)
        message_list = MessageModel.objects.filter(thread__id__contains=id)
        context = {
            'form': form,
            'thread': thread,
            'message_list': message_list,
        }
        return render(request, 'media/thread.html', context)

class CreateMessage(View):
    def post(self, request, id, *args, **kwargs):
        form = MessageForm(request.POST, request.FILES)
        thread = ThreadModel.objects.get(id=id)
        if thread.receiver == request.user:
            receiver = thread.user
        else:
            receiver = thread.receiver
        if form.is_valid():
            message = form.save(commit=False)
            message.thread = thread
            message.sender_user = request.user
            message.receiver_user = receiver
            message.save()
        notification = Notification.objects.create(notification_type=4, from_user=request.user, to_user=receiver, thread=thread)
        return redirect('thread', id=id)

def PostNotification(request, notification_id, post_id, post_slug):
    notification = Notification.objects.get(id=notification_id)
    post = Post.objects.get(id=post_id, slug=post_slug)
    
    notification.user_has_seen = True
    notification.save()
    
    return redirect('post_detail', id=post_id, slug=post_slug)

def FollowNotification(request, notification_id, profile_id):
    notification = Notification.objects.get(id=notification_id)
    profile = Profile.objects.get(id=profile_id)
    
    notification.user_has_seen = True
    notification.save()

def ThreadNotification(request, notification_id, object_id):
    notification = Notification.objects.get(id=notification_id)
    thread = ThreadModel.objects.get(id=object_id)
    
    notification.user_has_seen = True
    notification.save()
    
    return redirect('thread', id=object_id)

def RemoveNotification(request, notification_id):
    notification = Notification.objects.get(id=notification_id)
    
    notification.user_has_seen = True
    notification.save()
    
    return HttpResponse('success', content_type='text/plain')

def post_detail(request, id, slug):
    post = get_object_or_404(Post, id=id, slug=slug)
    comments = Comment.objects.filter(post=post, reply=None).order_by('-id')
    likes = post.likes.all()[0:4]
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        is_liked = True
        
    if request.method == 'POST':
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            content = request.POST.get('content')
            reply_id = request.POST.get('comment_id')
            comment_qs = None
            if reply_id:
                comment_qs = Comment.objects.get(id=reply_id)
            comment = Comment.objects.create(
                post=post, user=request.user, content=content, reply=comment_qs)
            comment.save()
            notification = Notification.objects.create(notification_type=2, from_user=request.user, to_user=post.author, post=post)
            # return HttpResponseRedirect(post.get_absolute_url())
    else:
        comment_form = CommentForm()
    
    context = {
        'post': post,
        'is_liked': is_liked,
        'total_likes': post.total_likes(),
        'comments': comments,
        'likes': likes,
        'comment_form': comment_form,
    }
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('media/comments.html', context, request=request)
        return JsonResponse({'form': html})

    return render(request, 'media/post_detail.html', context)

def like_post(request):
    post = get_object_or_404(Post, id=request.POST.get('id'))
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        is_liked = False
    else:
        post.likes.add(request.user)
        is_liked = True
        notification = Notification.objects.create(notification_type=1, from_user=request.user, to_user=post.author, post=post)
    context = {
        'is_liked': is_liked,
        'post': post,
        'total_likes': post.total_likes(),
    }
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('media/like_section.html', context, request=request)
        return JsonResponse({'form': html})
    # return HttpResponseRedirect(post.get_absolute_url())

def post_create(request):
    if request.method == 'POST':
        form = PostCreateForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = (request.user)
            post.save()
            
            return redirect('index')
    else:
        form = PostCreateForm()

    context = {
        'form': form,
    }
    return render(request, 'media/post_create.html', context)

def post_edit(request, id):
    post = get_object_or_404(Post, id=id)
    if post.author != request.user:
        raise Http404()
    if request.method == 'POST':
        form = PostEditForm(request.POST or None, request.FILES or None, instance=post)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(post.get_absolute_url())
    else:
        form = PostEditForm(instance=post)
    context = {
        'form': form,
        'post': post,
    }
    return render(request, 'media/post_edit.html', context)

def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    if request.user != post.author:
        raise Http404()
    post.delete()
    return redirect('index')

# USER AUTHENTICATION
def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return HttpResponse('User is not Active')
            else:
                return HttpResponse('User is None')
    else:
        form = UserLoginForm()
    context = {
        'form': form,
    }
    return render(request, 'media/login.html', context)


def user_logout(request):
    logout(request)
    return redirect('home')


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            return redirect('user_login')
    else:
        form = UserRegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'media/register.html', context)

def profile(request, id):
    profile = Profile.objects.get(id=id)
    user = profile.user
    posts = Post.objects.filter(author=user).order_by('created')
    is_followed = False
    if profile.followers.filter(id=request.user.id).exists():
        is_followed = True
    
    # followers = profile.followers.all()
    
    # if len(followers) == 0:
    # is_following = False
    
    # for follower in followers:
    #     if follower == request.user:
    #         is_following = True
    #         break
    #     else:
    #         is_following = False
            
    # number_of_followers = len(followers)
    
    context = {
        'user': user,
        'profile': profile,
        'posts': posts,
        # 'number_of_followers': number_of_followers,
        # 'is_following': is_following,
        'is_followed': is_followed,
        'total_followers': profile.total_followers(),
    }
    
    return render(request, 'media/profile.html', context)

def follow_user(request):
    profile = get_object_or_404(Profile, id=request.POST.get('id'))
    is_followed = False
    if profile.followers.filter(id=request.user.id).exists():
        profile.followers.remove(request.user)
        is_followed = False
    else:
        profile.followers.add(request.user)
        is_followed = True
        notification = Notification.objects.create(notification_type=3, from_user=request.user, to_user=profile.user)
    context = {
        'profile': profile,
        'is_followed': is_followed,
        'total_followers': profile.total_followers(),
    }
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('media/follow_section.html', context, request=request)
        return JsonResponse({'form': html})
    # return redirect('profile', id=profile.id)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserEditForm(
            data=request.POST or None, instance=request.user)
        profile_form = ProfileEditForm(
            data=request.POST or None, instance=request.user.profile, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponseRedirect(reverse('edit_profile'))
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'media/edit_profile.html', context)


def ListFollowers(request, id):
    profile = Profile.objects.get(id=id)
    followers = profile.followers.all()
    context = {
        'profile': profile,
        'followers': followers,
        'total_followers': profile.total_followers(),
    }
    return render(request, 'media/followers_list.html', context)
