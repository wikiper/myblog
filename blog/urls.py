from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('accounts/signup/', views.signup, name='signup'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('profile/', views.profile, name='profile'),
]
