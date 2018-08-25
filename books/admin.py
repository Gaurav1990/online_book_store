from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from books.models import Books

# Register your models here.
class AdminBooks(admin.ModelAdmin):
    list_display = ('name', 'type', 'isbn', 'description', 'author_name', 'release_date', 'signed', 'price')
    search_fields = ('name', 'type', 'isbn', 'description', 'author_name', 'release_date', 'signed', 'price')

admin.site.register(Books,AdminBooks)
