from django import forms
from django import forms
from .models import Article, Comment

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'body', 'author', 'photo']  # Asegúrate de listar solo los campos existentes

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['article', 'comment', 'author']  # Campos existentes en el modelo Comment
