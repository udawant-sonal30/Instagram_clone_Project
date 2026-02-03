from django.urls import path
from .views import signup_view, profile_view,edit_profile_view
from django.contrib.auth import views as auth_views
from .views import create_post_view, feed_view
from .views import like_unlike_post, add_comment, search_user_view, follow_toggle_view, view_profile
from . import views
urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login', http_method_names=['get', 'post']), name='logout'),
    path('profile/edit/', edit_profile_view, name='edit_profile'),
   
] 
urlpatterns += [
    path('', views.feed_view, name='feed'),
    path('post/<int:post_id>/like/', like_unlike_post, name='like_unlike_post'),
    path('post/<int:post_id>/comment/', add_comment, name='add_comment'),
    path('search/', search_user_view, name='search_user'),
    path('follow/<int:user_id>/', follow_toggle_view, name='follow_toggle'),         
    path('profile/<str:username>/', views.view_profile, name='view_profile'), 
    path('add_post/', views.create_post_view, name='add_post'),
    path('profile/', views.profile_view, name='profile'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('post/<int:post_id>/comments/',views.post_comments, name='post_comments'),


]