from django.contrib import admin
from .models import Project, Review, Tag


# admin.site.register(Project)
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'created')


# admin.site.register(Review)
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('owner', 'body', 'created')


# admin.site.register(Tag)
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'created')
