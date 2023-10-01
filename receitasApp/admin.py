from django.contrib import admin
from .models import Categoria, Receitas
from tagApp.models import Tag
from django.contrib.contenttypes.admin import GenericStackedInline

class CategoriaAdmin(admin.ModelAdmin):
    ...

admin.site.register(Categoria, CategoriaAdmin)

class TagInline(GenericStackedInline):
    model = Tag
    fields = 'nome',
    extra = 1

@admin.register(Receitas)
class ReceitasAdmin(admin.ModelAdmin):
    list_display = ['id', 'titulo', 'criado_em', 'autor', 'esta_publicado']
    list_display_links = ['titulo', 'criado_em']
    search_fields = ['id', 'titulo', 'criado_em', 'descricao', 'slug', 'modo_preparo']
    list_filter = ['categoria', 'autor', 'esta_publicado', \
                   'modo_preparo_html']
    list_per_page = 8
    list_editable = ['esta_publicado']
    ordering = ['criado_em', 'autor']
    prepopulated_fields = {
        "slug": ('titulo',)
    }
    inlines = [
        TagInline,
    ]