from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('add/', views.AddPostCreateView.as_view(), name='add_book'),
    path('edit/<int:id>', views.EditBookView.as_view(), name='edit_book'),
    path('delete/<int:id>', views.DeleteBookView.as_view(), name='delete_book'),
    path('details/<int:id>/', views.DetailBooktView.as_view(), name='book_detail'),
]