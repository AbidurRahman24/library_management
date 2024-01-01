from django.shortcuts import render
from books.models import Book
from categories.models import Category
def home(request, category_slug = None): # initially dhore nicchi je category_slug None thakbe karon hocche user first time home page e asle se normal page dekhbe, se filter korte chaile category te click korlei sei category er slug ta capture korbo ar seta tokhn ar None thakbe na
    
    data = Book.objects.all() 
    if category_slug is not None:
        category = Category.objects.get(slug = category_slug) 
        data = Book.objects.filter(category  = category) 
    categories = Category.objects.all() 
    return render(request, 'index.html', {'data' : data, 'category' : categories})