from django.contrib import admin
from library.models import Author, Book, Customer, CustomerBook

"""
For this admin site there will be only two types of access layers 
librarian: have full access to database such as delete books, add books, and more
employee:  The employee will only have access to get information from the database
"""


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    model_fields = [field.name for field in Author._meta.get_fields()][1:]
    list_display = model_fields
    search_fields = model_fields
    list_filter = model_fields
    ordering = ['name']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    pass


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    pass

@admin.register(CustomerBook)
class CustomerBookAdmin(admin.ModelAdmin):
    pass