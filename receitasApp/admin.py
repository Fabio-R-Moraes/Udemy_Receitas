from django.contrib import admin
from .models import Categoria, Receitas

class CategoriaAdmin(admin.ModelAdmin):
    ...

admin.site.register(Categoria, CategoriaAdmin)

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
    autocomplete_fields = 'tags',
