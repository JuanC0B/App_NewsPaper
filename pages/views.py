from django.shortcuts import render, redirect
from articles.models import Article, Comment
from articles.forms import CommentForm
from django.contrib.auth.decorators import login_required
# Create your views here.

#renderizacion de la pagina principal 
@login_required
def HomePageView(request):
    articles = Article.objects.all()
    form = CommentForm()

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            # Guardar el comentario sin comprometerlo a la base de datos todavía
            comment = form.save(commit=False)
            # Asignar el artículo y el autor al comentario
            article_id = request.POST.get("article_id")  # Capturar el ID del artículo desde el formulario
            comment.article = Article.objects.get(id=article_id)
            comment.author = request.user
            comment.save()
            return redirect("home")  # Recargar la página principal

    return render(request, "home.html", {
        'articles': articles,
        'form': form
    })