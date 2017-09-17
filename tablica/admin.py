from django.contrib import admin
from .models import Post, Category, Comment


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, CategoryAdmin)


class PostAdmin(admin.ModelAdmin):
    list_display = ('temat', 'author', 'published', 'status')
    list_filter = ('status', 'created', 'published', 'author')
    search_fields = ('temat', 'tekst')
    prepopulated_fields = {'slug': ('temat',)}

admin.site.register(Post, PostAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'approved')

admin.site.register(Comment, CommentAdmin)
