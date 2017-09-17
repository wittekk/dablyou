from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages

from .models import Post, Category
from .forms import CommentForm, PostForm


def list_of_post_by_category(request, category_slug):
    categories = Category.objects.all()
    post = Post.objects.filter(status='opublikowany')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        post = post.filter(category=category)
    template = 'tablica/category/list_of_post_by_category.html'
    context = {'categories': categories, 'post': post, 'category_slug': category_slug}
    return render(request, template, context)


def list_of_post(request):
    post = Post.objects.filter(status='opublikowany')
    categories = Category.objects.all()
    paginator = Paginator(post, 10)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    template = 'tablica/post/list_of_post.html'
    context = {'posts': posts, 'page': page, 'categories': categories}
    return render(request, template, context)


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    context = {'post': post}
    if post.status == 'opublikowany':
        template = 'tablica/post/post_detail.html'
        return render(request, template, context)
    else:
        template = 'tablica/post/post_preview.html'
        return render(request, template, context)


def add_comment(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('tablica:post_detail', slug=post.slug)
    else:
        form = CommentForm()
    template = 'tablica/post/add_comment.html'
    context = {'form': form}
    return render(request, template, context)


def new_post(request):
    if not request.user.is_authenticated():
        return render(request, 'albumbum/login.html')

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('tablica:post_detail', slug=post.slug)
    else:
        form = PostForm()
    template = 'tablica/backend/new_post.html'
    context = {'form': form}
    return render(request, template, context)


def list_of_post_backend(request):
    if not request.user.is_authenticated():
        return render(request, 'albumbum/login.html')

    post = Post.objects.all()
    paginator = Paginator(post, 15)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    template = 'tablica/backend/list_of_post_backend.html'
    context = {'posts': posts, 'page': page}
    return render(request, template, context)


def edit_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('tablica:list_of_post_backend')
    else:
        form = PostForm(instance=post)
    template = 'tablica/backend/new_post.html'
    context = {'form': form}
    return render(request, template, context)


def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.delete()
    messages.success(request, "Wpis został usunięty  uff...")
    return redirect('tablica:list_of_post_backend')

