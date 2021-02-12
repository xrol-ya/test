from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView, DetailView

from .forms import MyAuthenticationForm, RegistrationForm, ReviewForm, BorrowBookForm, RenewBookForm
from .models import Book, Author, BookInstance, Review
import datetime
from django.contrib.auth.models import Group


def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
    }

    return render(request, 'index.html', context=context)


class BookListView(LoginRequiredMixin, ListView):
    model = Book
    paginate_by = 1


class BookDetailView(LoginRequiredMixin, DetailView):
    model = Book


@csrf_protect
def auth_login(request):
    if request.method == 'POST':
        loginform = MyAuthenticationForm(request.POST)
        signupform = RegistrationForm(request.POST)
        if 'login' in request.POST:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request=request, username=username, password=password)

            if user is not None:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('books')
            else:
                render(request, 'registration/login.html', {'error': 'Wrong credentials'})
        elif signupform.is_valid() and 'sign-up' in request.POST:
            # Saving user to the database
            user = signupform.save()
            user.refresh_from_db()
            raw_password = signupform.cleaned_data.get('password')
            user.set_password(raw_password)
            user.save()

            # Automatically signing the user up
            raw_password = signupform.cleaned_data.get('password')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            # NEED ADD GROUP
            # group = Group.objects.get(name='Student/Teacher')
            # group.user_set.add(user)

            return redirect('books')
    else:
        loginform = MyAuthenticationForm()
        signupform = RegistrationForm()

    return render(request, 'registration/login.html', {'loginform': loginform, 'signupform': signupform})


def review_book(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review_text = form.cleaned_data['review']
            reviewer = request.user
            review = Review(review=review_text, reviewer=reviewer)
            review.save()
            book.reviews.add(review)
            book.save()
            return redirect('books')
    else:
        form = ReviewForm()
    context = {
        'form': form,
        'book': book,
    }
    return render(request, 'library_management/review_book.html', context)


def profile(request):
    bookinstance = BookInstance.objects.all()
    booksreviewed = Book.objects.all()

    context = {
        'bookinstance': bookinstance,
        'booksreviewed': booksreviewed,
    }

    return render(request, 'profile.html', context=context)


def borrow_book(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    if request.method == 'POST':

        form = BorrowBookForm(request.POST)

        if form.is_valid():
            due_date = form.cleaned_data['due_date']
            book_instance.borrower = request.user
            book_instance.due_back = due_date
            book_instance.status = 'r'

            book_instance.save()

            return redirect('profile')

    else:
        form = BorrowBookForm(initial={'due_date': datetime.date.today()})

    context = {
        'form': form,
        'book_instance': book_instance
    }

    return render(request, 'library_management/borrow_book.html', context)


def return_book(request, pk):
    # РЕАЛИЗАЦИЯ НА БУДУЖЕЕ
    pass

def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    if request.method == 'POST':
        form = RenewBookForm(request.POST)

        if form.is_valid():
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()
            return redirect('index')

    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'library_management/book_renew_librarian.html', context)


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'library_management/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(
            borrower=self.request.user
        ).filter(status__exact='r').order_by('due_back')
git clone https://vorofikini@bitbucket.org/vorofikini/hola.git

def about(request):
    return render(request, 'library_management/about.html', {})