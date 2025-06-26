from django.contrib import admin

from .models import Author, Book, Loan, Member

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Member)
admin.site.register(Loan)
