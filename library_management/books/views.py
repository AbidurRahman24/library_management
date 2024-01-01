from django.shortcuts import render, redirect
from . import forms
from . import models
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView,UpdateView,DeleteView,DetailView
from django.urls import reverse_lazy
# Create your views here.
@method_decorator(login_required, name='dispatch')
def add_book(request):
    if request.method == 'POST': # user post request koreche
        book_form = forms.BookForm(request.POST)
        if book_form.is_valid():
            book_form.save()
            print(book_form)
            return redirect('add_book')
    
    else: # user normally website e gele blank form pabe
        book_form = forms.BookForm()
    return render(request, 'add_book.html', {'form' : book_form})


@method_decorator(login_required, name='dispatch')
class AddPostCreateView(CreateView):
    model = models.Book
    form_class = forms.BookForm
    template_name = 'add_book.html'
    success_url = reverse_lazy('add_book')
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    

@method_decorator(login_required, name='dispatch')
class DetailBooktView(DetailView):
    model = models.Book
    pk_url_kwarg = 'id'
    template_name = 'book_details.html'

    def post(self, request, *args, **kwargs):
        comment_form = forms.ReviewForm(data=self.request.POST)
        post = self.get_object()
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
        return self.get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object # post model er object ekhane store korlam
        comments = post.comments.all()
        comment_form = forms.ReviewForm()
        
        context['comments'] = comments
        context['comment_form'] = comment_form
        return context
    
@method_decorator(login_required, name='dispatch')
class EditBookView(UpdateView):
    model = models.Book
    form_class = forms.BookForm
    template_name = 'add_book.html'
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('home')

@method_decorator(login_required, name='dispatch')
class DeleteBookView(DeleteView):
    model = models.Book
    template_name = 'delete.html'
    success_url = reverse_lazy('home')
    pk_url_kwarg = 'id'