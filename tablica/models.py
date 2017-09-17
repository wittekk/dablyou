from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_absolute_url(self):
        return reverse('tablica:list_of_post_by_category', args=[self.slug])

    def __str__(self):
        return self.name


class Post(models.Model):
    STATUS_CHOICES = (
        ('roboczy', 'Roboczy'),
        ('opublikowany', 'Opublikowany')
    )
    category = models.ForeignKey(Category)
    temat = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)
    tekst = models.TextField()
    author = models.ForeignKey(User, related_name='tablica_post')
    published = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='roboczy')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.temat)
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('tablica:post_detail', args=[self.slug])

    class Meta:
        ordering = ['-published']

    def __str__(self):
        return self.temat


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments')
    user = models.CharField(max_length=250)
    email = models.EmailField()
    komentarz = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def approved(self):
        self.approved = True
        self.save()

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.user



