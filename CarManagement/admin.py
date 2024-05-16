from django.contrib import admin
from .models import (
    Technicien, Vehicule, Client,
     EntrePanne, EntreVehicule,
    Panne, Piece, SortieVehicule
)
class EntrePanneInline(admin.TabularInline):
    model = EntrePanne

@admin.register(EntreVehicule)
class EntreVehiculeAdmin(admin.ModelAdmin):
    inlines = [EntrePanneInline]

admin.site.register(Technicien)
admin.site.register(Vehicule)
admin.site.register(Client)
admin.site.register(SortieVehicule) 
admin.site.register(EntrePanne) 
admin.site.register(Panne)
admin.site.register(Piece)
 



 
