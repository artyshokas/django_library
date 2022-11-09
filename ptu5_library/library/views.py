from django.shortcuts import render
from django.http import HttpResponse
from . models import Genre, Author, Book, BookInstance

def index(request):
   # return HttpResponse("Welcome to Library")
   book_count = Book.objects.count()
   book_isinstance_count = BookInstance.objects.count()
   book_instance_available_count = BookInstance.objects.filter(status='a').count()
   author_count = Author.objects.count()

   context = {
    'book_count': book_count,
    'book_instance_count': book_isinstance_count,
    'book_instance_available_count': book_instance_available_count,
    'author_count': author_count,
    'genre_count': Genre.objects.count() # ne per kintamaji
   }

   return render(request, 'library/index.html', context=context)
