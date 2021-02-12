from django.urls import path
from django.urls import include

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
    path('book/<uuid:pk>/borrow', views.borrow_book, name='borrow'),
    path('book/<int:pk>/review/', views.review_book, name='book-review'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),

    path('accounts/', include('django.contrib.auth.urls')),
    path('login/', views.auth_login, name='auth-login'),
    path('accounts/profile/', views.profile, name='profile'),
    path('about/', views.about, name='about'),
]