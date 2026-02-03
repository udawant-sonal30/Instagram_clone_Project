from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import EditProfileForm
from .forms import PostForm
from .models import Like, Post, Comment
from .forms import CommentForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import redirect, get_object_or_404
from .models import Follow
from django.contrib.auth.models import User
from .forms import UserSearchForm
from django.contrib.auth import logout
from django.shortcuts import redirect
from .models import Profile
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.cache import never_cache


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect('feed')  
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})
@never_cache
@login_required
def profile_view(request):
    profile = request.user.profile
    user_posts = Post.objects.filter(author=request.user).order_by('-created_at')
    
    user_likes_post = {
        post.id: post.likes.filter(user=request.user).exists()
        for post in user_posts
    }
    context = {
        'profile': profile,
        'user_posts': user_posts,
        'user_likes_post': user_likes_post,
        'post_count': user_posts.count(),
        'followers_count': profile.followers.count(),
        'following_count': profile.following.count(),
    }
    return render(request, 'accounts/view_profile.html', context)
@login_required
def edit_profile_view(request):
    profile = request.user.profile  

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  
    else:
        form = EditProfileForm(instance=profile, user=request.user)

    return render(request, 'accounts/edit_profile.html', {'form': form})


@login_required
def create_post_view(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success'})
            return redirect('view_profile', username=request.user.username)
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error'})
    else:
        form = PostForm()
    return render(request, 'accounts/add_post.html', {
        'form': form,   
        'profile': profile,  
    })

@login_required
def feed_view(request):
    posts = Post.objects.all().order_by('-created_at')  # latest first
    return render(request, 'accounts/feed.html', {'posts': posts})    
@login_required
@require_POST
def like_unlike_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    existing_like = Like.objects.filter(user=request.user, post=post).first()
    if existing_like:
        existing_like.delete()
        liked = False
    else:
        Like.objects.create(user=request.user, post=post)
        liked = True

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'liked': liked,
            'likes_count': post.likes.count()
        })
    return redirect(request.META.get('HTTP_REFERER', 'feed'))

@login_required
@require_POST
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    text = request.POST.get('comment')
    if text:
        comment = Comment.objects.create(user=request.user, post=post, text=text)
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'username': comment.user.username,
                'text': comment.text
            })
        return redirect(request.META.get('HTTP_REFERER', 'feed'))
   

@login_required
def search_user_view(request):
    form = UserSearchForm(request.GET or None)
    results = []

    if form.is_valid():
        query = form.cleaned_data['query']
        results = User.objects.filter(username__icontains=query)

    return render(request, 'accounts/search_user.html', {'form': form, 'results': results}) 

@login_required
def follow_toggle_view(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    profile = request.user.profile

    if target_user.profile in profile.following.all():
        profile.following.remove(target_user.profile)  # Unfollow
    else:
        profile.following.add(target_user.profile)     # Follow
        followers_count = target_user.profile.followers.count()

    return redirect(request.META.get('HTTP_REFERER', '/'))  

def logout_view(request):
    logout(request)
    return redirect('login')    

@login_required
def view_profile(request, username):
    # Get user profile using username instead of ID
    profile = get_object_or_404(Profile, user__username=username)
    followers_count = profile.followers.count()
    following_count = profile.following.count()
    # Post count for this user
    post_count = profile.user.posts.count()  # Post model मध्ये related_name='posts' असल्यास
    user_posts =  user_posts = Post.objects.filter(author=profile.user).order_by('-created_at')

    # Add Post form
    if request.user == profile.user:  # फक्त logged-in user साठी
        post_form = PostForm(request.POST or None, request.FILES or None)
        if request.method == 'POST' and post_form.is_valid():
            new_post = post_form.save(commit=False)
            new_post.author= request.user
            new_post.save()
            return redirect('view_profile', username=username)
    else:
        post_form = None

    user_likes_post = {}
    for post in user_posts:
        user_likes_post[post.id] = post.likes.filter(user=request.user).exists()
    
    context = {
        'profile': profile,
        'followers_count': followers_count,
        'following_count': following_count,
        'post_count': profile.user.posts.count(),
        'user_posts': user_posts,
        'post_form': post_form, 
        'user_likes_post': user_likes_post,
    }
    return render(request, 'accounts/view_profile.html', context)

def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    
    if request.user == post.user:
        post.delete()
        messages.success(request, "Post deleted successfully.")
    else:
        messages.error(request, "You are not allowed to delete this post.")

    return redirect('profile', username=request.user.username)

def post_comments(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()

    if request.method == "POST":
        text = request.POST.get("comment")
        if text:
            Comment.objects.create(
                post=post,
                user=request.user,
                text=text
            )
            return redirect('post_comments', post_id=post_id)

    return render(request, "accounts/post_comments.html", {
        "post": post,
        "comments": comments
    })
