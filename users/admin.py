from django.contrib import admin
from .models import Profile, Skills, Message


# admin.site.register(Profile)
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'username', 'created')
    # list_filter = ('host', 'name', 'topic')
    # fields = ['host', ('topic', 'name'), 'description', 'participants']
    # exclude =
    # fieldsets = (
    #     (None, {
    #         'fields': ('book', 'imprint', 'id')
    #     }),
    #     ('Availability', {
    #         'fields': ('status', 'due_back')
    #     }),
    # ! )<------------------- grouping


# admin.site.register(Skills)
@admin.register(Skills)
class SkillsAdmin(admin.ModelAdmin):
    list_display = ('owner', 'name', 'created')


# admin.site.register(Message)
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'name', 'is_read', 'created')
