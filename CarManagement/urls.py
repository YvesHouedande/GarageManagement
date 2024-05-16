from django.urls import path
from django.urls import path
from .views import (
    technicien_view, entre_vehicule_list,
    technicien_view_form, confirm_delete,
    dashboard, vehicule_view, client_view_form,
    client_view, vehicule_view_form, panne_view,
    panne_view_form, piece_view_form, piece_view,
    panne_piece_view, quantite_piece_form, entre_vehicule_panne_view, logout_view,
    vehicule_entree_view, entre_vehicule_view_form, entre_vehicule_detail, etat_panne_form, login_view,
    entre_vehicule_technicien_view, sortie_vehicule_create,
    sortie_vehicule_update, sortie_vehicule_list
                 ) 

urlpatterns = [ 
    #delete handling
    path('<str:klass>/<int:pk>/delete/', confirm_delete, name='confirm-delete'),

    #dashboard
    # path('dashboard/', dashboard, name='dashboard'),
    path('', dashboard, name='dashboard'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),





    #for techniciens
    path('techniciens/', technicien_view, name='technicien-list'),
    path('techniciens/<int:pk>/', technicien_view, name='technicien-detail'),
    path('techniciens/<int:pk>/update', technicien_view_form, name='technicien-update'),
    path('techniciens/create', technicien_view_form, name='technicien-create'),
    path('techniciens/delete', technicien_view_form, name='technicien-delete'),

    #for Entrévehicule
    path('entre_vehicules/<int:pk>/', entre_vehicule_detail, name='entre_vehicule-detail'),
    path('entre_vehicules/<int:pk>/update', entre_vehicule_view_form, name='entre_vehicule-update'),
    path('entre_vehicules/create', entre_vehicule_view_form, name='entree-create'),
    path('entre_vehicules/', entre_vehicule_list, name='entre_vehicule-list'), 
    path('entre_vehicule/pannes/<int:pk>/', entre_vehicule_panne_view, name='entre_vehicule_panne-list'),
    path('entre_vehicule/techniciens/<int:pk>/', entre_vehicule_technicien_view, name='entre_vehicule_technicien-list'),


    #for vehicule    
    path('vehicules/<int:pk>', vehicule_view, name='vehicule-detail'),
    path('vehicules/', vehicule_view, name='vehicule-detail'),
    path('vehicules/create', vehicule_view_form, name='vehicule-create'),
    path('vehicules/<int:pk>/update', vehicule_view_form, name='vehicule-update'),
    path('vehicules/<int:pk>/entree', entre_vehicule_list, name='vehicule_entree-list'),
    path('vehicules/<int:pk>/sortie', sortie_vehicule_list, name='vehicule_sortie-list'),




    #for client  
    path('clients/create', client_view_form, name='client-create'),
    path('clients/<int:pk>/update', client_view_form, name='client-create'),
    path('clients/<int:pk>/', client_view, name='detail-client'),
    path('clients/', client_view, name='detail-client'),

    #pannes
    path('pannes/create', panne_view_form, name='panne-create'),
    path('pannes/<int:pk>/', panne_view, name='panne-detail'),
    path('pannes/<int:pk>/update', panne_view_form, name='panne-update'),
    path('pannes/', panne_view, name='panne-list'),
    path('pannes/<int:pk>/pieces', panne_piece_view, name='panne-piece-list'),



    #pannes
    path('pieces/create', piece_view_form, name='piece-create'),
    path('pieces/<int:pk>/', piece_view, name='piece-detail'),
    path('pieces/<int:pk>/update', piece_view_form, name='piece-update'),
    path('pieces/', piece_view, name='piece-list'),

    #sorties
    path('sorties/create/', sortie_vehicule_create, name='sortie-create'),
    path('sorties/<int:pk>/update/', sortie_vehicule_update, name='sortie-update'),
    path('sorties/', sortie_vehicule_list, name='sortie-list'),

    #pannes
    # path('quantite/create', piece_view_form, name='piece-create'),
    # path('pieces/<int:pk>/', piece_view, name='piece-detail'),
    path('quantite/<int:pk>/update', quantite_piece_form, name='quantite-update'),
    path('etat/<int:pk>/update', etat_panne_form, name='etat-update'),

    path('pieces/', piece_view, name='piece-list'),

]
 
