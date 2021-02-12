from django.contrib import admin

from .models import Author, Genre, Book, BookInstance, Review


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'middle_name', 'last_name', 'date_of_birth', 'date_of_death')


class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 2


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author') # 'display_genre', 'display_review'
    inlines = [BooksInstanceInline]
    exclude = ('reviews',)


class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')
    exclude = ('borrower', 'status', 'due_back')

    # fieldsets = (
    #     (None, {
    #         'fields': ('book','imprint', 'id')
    #     }),
    #     ('Availability', {
    #         'fields': ('status', 'due_back','borrower')
    #     }),
    # )


# admin.site.register(Book)
# admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Review)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(BookInstance, BookInstanceAdmin)
