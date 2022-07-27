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
    path('', views.Home, name='home' ),
    path('search/', views.SearchBook, name='search' ),
    path('categories/', views.CategoryListView.as_view(), name='category-list' ),
    path('categories/<category>', views.category, name='category-books' ),
    path('Free/', views.Free, name='free' ),
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('book/new/', views.BookCreateView.as_view(), name='add-book'),
    path('submit_review/<int:book_id>', views.submit_review, name='submit-review' ),
    
    
]
