from django.contrib import admin
from . import models

# Register your models here.
class DarbaiInLine(admin.TabularInline):
    model = models.Darbas
    readonly_fields = ["pavadinimas", "pastabos", "kaina"]
    extra = 0

class ProjektasAdmin(admin.ModelAdmin):
    list_display = ("pavadinimas", "datapr", "datapb", "klientas", "vadovas", "display_darbuotojai")
    list_filter = ("pavadinimas", "klientas", "vadovas")
    search_fields = ("pavadinimas", "klientas", "vadovas")
    inlines = [DarbaiInLine]

class KlientasAdmin(admin.ModelAdmin):
    list_display = ("vardas", "pavarde", "imone", "email", "telnr")

class DarbuotojasAdmin(admin.ModelAdmin):
    list_display = ("vardas", "pavarde", "pareigos")

class DarbasAdmin(admin.ModelAdmin):
    list_display = ("pavadinimas", "pastabos", "projektas", "kaina")

class SaskaitaAdmin(admin.ModelAdmin):
    list_display = ("projektas", "data", "suma")


# Register your models here.
admin.site.register(models.Projektas, ProjektasAdmin)
admin.site.register(models.Klientas, KlientasAdmin)
admin.site.register(models.Darbuotojas, DarbuotojasAdmin)
admin.site.register(models.Darbas, DarbasAdmin)
admin.site.register(models.Saskaita, SaskaitaAdmin)
