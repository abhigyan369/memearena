from django.contrib import admin
from .models import Tag, Meme, MemeOfDay

@admin.register(Meme)
class MemeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'score')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(MemeOfDay)
class MemeOfDayAdmin(admin.ModelAdmin):
    list_display = ('date', 'meme')
