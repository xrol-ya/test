import uuid

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from .review import Review
from .genre import Genre


class Book(models.Model):
    isbn = models.CharField(
        'ISBN',
        max_length=13,
        help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>'
    )
    title = models.CharField(max_length=200)
    author = models.ForeignKey(
        'Author',
        on_delete=models.SET_NULL,
        null=True
    )
    summary = models.TextField(
        max_length=1000,
        help_text='Enter a brief description of the book'
    )
    genre = models.ManyToManyField(
        Genre,
        help_text='Select a genre for this book'
    )
    reviews = models.ManyToManyField(
        Review,
        help_text='Leave a review for this book'
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    def display_review(self):
        return ', '.join(reviews.review + ' - ' + reviews.reviewer.username for reviews in self.reviews.all()[:3])


class BookInstance(models.Model):
    BOOK_STATUS = (
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text='Unique ID for this particular book across whole library'
    )
    book = models.ForeignKey(
        'Book',
        on_delete=models.CASCADE,
        null=True
    )
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(
        null=True,
        blank=True
    )
    borrower = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=1,
        choices=BOOK_STATUS,
        blank=True,
        default='a',
        help_text='Book availability',
    )

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        return f'{self.id} ({self.book.title})'
