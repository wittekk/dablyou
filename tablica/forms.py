from django import forms
from .models import Comment, Post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('user', 'email', 'komentarz')


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('temat', 'tekst', 'category', 'status')
