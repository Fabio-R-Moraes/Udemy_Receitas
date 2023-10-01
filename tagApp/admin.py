from django.contrib import admin
from .models import Tag

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = 'id', 'nome', 'slug'
    list_display_links = 'id', 'slug'
    search_fields = 'id', 'nome', 'slug'
    list_per_page = 10
    list_editable = 'nome',
    ordering = '-id',
    prepopulated_fields = {
        'slug': ('nome',),
    }
