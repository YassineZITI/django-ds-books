"""itbook URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from . import views

urlpatterns = [
    path('discussions/<category>/<topic>/', views.TopicPostListView.as_view(), name='topic-posts'),
    path('discussions/<category>/', views.CategoryPostListView.as_view(), name='category-posts'),
    path('discussions/', views.PostListView.as_view(), name='posts'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('discussions/<category>/<topic>/new_post/', views.PostCreateView.as_view(), name='post-create'),
    
    path('post/<int:pk>/update', views.PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete', views.PostDeleteView.as_view(), name='post-delete'),
    path('discussions/<category>/', views.discussion, name='discussion-topics' ),
    path('submit_comment/<int:post_id>', views.submit_comment, name='submit-comment' ),
    
    
    
]
