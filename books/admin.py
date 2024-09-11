from django.contrib import admin

from .models import Book
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'price', 'author']
    search_fields = ['title', 'author__username']
    list_filter = ['author']
# Register your models here.
admin.site.register(Book, BookAdmin)
