from django.forms import BaseModelForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse, HttpResponseForbidden
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy, reverse
from .models import Article
from .models import Comment
from .forms import CommentForm
from .forms import ArticleForm

# Create your views here.
class CommentGet(LoginRequiredMixin, DeleteView):
    model = Article
    template_name = "article_detail.html"
    
    def get_context_data(self, **Kwargs):
        context = super().get_context_data(**Kwargs)
        context['form'] = CommentForm()
        return context
        
class CommentPost(LoginRequiredMixin, FormView):
    model = Article
    form_class = CommentForm
    template_name = "article_detail.html"
    
    def get_object(self):
        # Accede al artículo por su pk (primary key) desde la URL
        article_pk = self.kwargs['pk']
        return get_object_or_404(Article, pk=article_pk)
    
    def post(self, request, *args, **kwargs):
        # Aquí utilizamos get_object para obtener el artículo asociado
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)
    
    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.article = self.object  # Asociamos el comentario con el artículo
        comment.author = self.request.user  # Establecemos el autor como el usuario actual
        comment.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        # Después de guardar el comentario, redirige al detalle del artículo
        article = self.get_object()
        return reverse('article_detail', kwargs={'pk': article.pk})
        
class ArticleDetailView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        view = CommentGet.as_view()
        return view(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        view = CommentPost.as_view()
        return view(request, *args, **kwargs)
         
class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = Article
    fields = (
        "title",
        "body",
    )
    template_name = "article_edit.html"
    
    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    model = Article
    template_name = "article_delete.html"
    success_url = reverse_lazy("article_list")
    
    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    template_name = 'article_new.html'
    fields =(
        'title',
        'body',
        'photo',
    )
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class CommentEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ['comment']
    template_name = 'comment_edit.html'

    def get_success_url(self):
        return reverse('article_detail', kwargs={'pk': self.object.article.pk})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author or self.request.user == comment.article.author

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'comment_delete.html'

    def get_success_url(self):
        return reverse('article_detail', kwargs={'pk': self.object.article.pk})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author or self.request.user == comment.article.author
