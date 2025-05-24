from django.contrib import admin

from departamento.models import Departamento

# Register your models here.

class DepartamentoAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('nome',)
    }
    list_display = ('nome', 'slug')
    search_fields = ('nome',)
    
admin.site.register(Departamento, DepartamentoAdmin)