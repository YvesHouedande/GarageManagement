from django.shortcuts import render ,get_object_or_404, redirect
from django.urls import resolve
from django.db.models import Q
from .forms import (
    EntreVehiculeForm, TechnicienForm, EntrePanneForm,
    ClientForm, VehiculeForm, PanneForm, PieceForm, PieceQtyForm,
    SortieVehiculeForm
 )
from django.http import HttpResponseRedirect
from django.apps import apps
from django.urls import reverse
from .models import (
    Technicien, EntreVehicule, EntrePanne,
    Vehicule, Client, Panne, Piece, QuantitePiece,
    SortieVehicule
    )
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import date
from django.conf.urls import handler404


def custom_page_not_found(request, exception):
    return render(request, 'template/404.html', status=404)

handler404 = custom_page_not_found



def authentication_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')  
        return view_func(request, *args, **kwargs)
    return wrapper


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Rediriger vers la vue dashboard après la connexion
        else:
            messages.error(request, 'Identifiant ou mot de passe incorrect.')
    return render(request, 'template/login.html') 

def logout_view(request):
    logout(request)
    return redirect('login') 

@authentication_required
def dashboard(request):
    """
        -tous les veehicules:vehicules
        -nb_vehicule
        -nb_pannes
        -charge total tech*
        - somme totoal pannes
    """
    context = {}
    context["vehicules"] = Vehicule.objects.all()
    context["nb_pannes"] = Panne.objects.all().count()
    context["nb_vehicule"] = context["vehicules"].count()
    context["nb_client"] = Client.objects.all().count()
    context["nb_entree"] = EntreVehicule.objects.all().count()
    context["nb_technicien"] = Technicien.objects.all().count() 
    context["nb_pannes_r"] = EntrePanne.objects.all().count()
    context["nb_pieces"] = Piece.objects.all().count() 
    context["charge_total_tech"] = sum([tech.salaire for tech in Technicien.objects.all()])
    context["charge_total_pannes"] = sum([panne.cout for panne in Panne.objects.all()])
    context['somme_total_pannes'] = sum([panne.cout for panne in Panne.objects.all()])
    context['somme_total_pieces'] = sum([piece.prix for piece in Piece.objects.all()])
    context['somme_total_sorties'] = sum([sortie.cout for sortie in SortieVehicule.objects.all()])


    return render(request, "template/dashboard.html",context)


@authentication_required
def confirm_delete(request, klass, pk):
    model = apps.get_model(app_label='CarManagement', model_name=klass)
    instance = get_object_or_404(model, pk=pk)
    if request.method == 'POST':
        instance.delete()
        return HttpResponseRedirect(reverse('dashboard'))
    return render(request, "template/confirm_delete_form.html", {'object': instance, "klass":klass})


@authentication_required
def technicien_view(request, pk=None):
    context = {}
    if pk is not None:
        obj = get_object_or_404(Technicien, pk=pk)
        context['nb_entree_aff'] = obj.entrevehicule_set.all().count()
        vehicule_ids = obj.entrevehicule_set.all().values_list('vehicule', flat=True)
        context['nb_vehicules'] = Vehicule.objects.filter(id__in=vehicule_ids).count()
        # context['nb_vehicules'] = obj.vehicule_set.all().count()
        context['object'] = obj
        return render(request, "template/technicien_detail.html", context)
    context['specialites']= Technicien.SPECIALITE

    # recherche et filtre
    techniciens = Technicien.objects.all()
    search_query = request.GET.get('q')
    if search_query:
        techniciens = techniciens.filter(
            Q(nom__icontains=search_query) |
            Q(prenom__icontains=search_query) |
            Q(salaire__icontains=search_query) 
        )
    # Filtrage par carburant
    specialite_filter = request.GET.get('specialite')
    if specialite_filter:
        techniciens = techniciens.filter(specialite=specialite_filter) 
    context['objects'] = techniciens

    return render(request, "template/technicien_list.html", context)

@authentication_required
def technicien_view_form(request, pk=None):
    context = {}
    if pk is not None:
        context['pk'] = pk
        technicien = Technicien.objects.get(pk=pk)
        if request.method == 'POST':
            form = TechnicienForm(request.POST, request.FILES, instance=technicien)
            if form.is_valid():
                form.save()
                return redirect('technicien-detail', pk=pk)
        else:
            form = TechnicienForm(instance=technicien)
    else:
        if request.method == 'POST':
            form = TechnicienForm(request.POST, request.FILES) 
            if form.is_valid():
                form.save()
                return redirect('technicien-list') 
        else:
            form = TechnicienForm()
    
    context['form'] = form
    return render(request, 'template/technicien_form.html', context)


@authentication_required
def entre_vehicule_panne_view(request, pk=None):
    context = {}
    if pk is not None:
        obj = EntreVehicule.objects.get(pk=pk)
        context['objects'] = obj.entrepanne_set.all()
        context['object'] = obj
        return render(request, "template/entre_vehicule_panne_detail.html", context)

########vehicule entre
@authentication_required
def entre_vehicule_list(request, pk=None):
    context = {}
    if pk and resolve(request.path_info).url_name == "vehicule_entree-list":
        vehicule = get_object_or_404(Vehicule, pk=pk)
        entrees = vehicule.entrevehicule_set.all()
        context["object"] = vehicule
    else:
        entrees = EntreVehicule.objects.all()

    # Filtrage des entrées en fonction des paramètres de requête
    date_filter = request.GET.get('date')
    libelle_filter = request.GET.get('q')

    if date_filter:
        entrees = entrees.filter(moment=date_filter)
    if libelle_filter:
        entrees = entrees.filter(vehicule__libelle__icontains=libelle_filter)
    context['objects'] = entrees 
    return render(request, 'template/entre_vehicule_list.html', context)


@authentication_required
def entre_vehicule_detail(request, pk):
    context = {}
    obj = get_object_or_404(EntreVehicule, pk=pk)
    context['object'] = obj
    context['pannes_pieces'] = [panne.piece.all() for panne in obj.pannes.all()]
    context['pannes_pieces_len'] = sum([len(pieces) for pieces in context['pannes_pieces']])
    context['cout_total_panne'] = sum([panne.cout for panne in obj.pannes.all()])
    #context['nb_T_piece'] = sum([QuantitePiece.objects.get(panne=obj, piece=piece) for piece in context['pannes_pieces']])
    #context['pannes_pieces_cout'] = sum([sum([piece.prix * QuantitePiece.objects.get(piece=piece, panne=obj.panne) for piece in pieces])for pieces in context['pannes_pieces']])
    return render(request, "template/entre_vehicule_detail.html", context)


@authentication_required
def entre_vehicule_view_form(request, pk=None):
    context= {}
    if pk:
        obj = EntreVehicule.objects.get(pk=pk)
        context["pk"] = pk
    else:
        obj = None
    if request.method == 'POST':
        form = EntreVehiculeForm(request.POST, instance=obj)
        if form.is_valid():
            instance=form.save()
            return redirect('entre_vehicule-detail', pk=instance.pk)
    else:
        form = EntreVehiculeForm(instance=obj)
    context["form"]=form
    return render(request, 'template/entree_form.html', context)

########vehicule
@authentication_required
def vehicule_view(request, pk=None):
    """
    -Toutes les entrees vehicules: entree_vehicules
    -info de base:obj
    """
    context = {} 
    if pk is not None:
        obj = Vehicule.objects.get(pk=pk)
        context['entrees_vehicule'] = obj.entrevehicule_set.all()

        context['total_pannes_for_total_entrees'] = [[entrepanne for entrepanne in entreev.entrepanne_set.all()] for entreev in obj.entrevehicule_set.all()]
        context['total_pannes_for_total_entrees_len'] = sum([len(pannes) for pannes in context['total_pannes_for_total_entrees']])
        context['total_pannes_for_total_entrees_cout'] = sum([sum([entrepanne.panne.cout for entrepanne in  pannes ])for pannes in context['total_pannes_for_total_entrees']])
        try:
            context['pannes_vehicule'] = [[panne.piecexcc for panne in entree.pannes.all()]for entree in context['entrees_vehicule']][0]
            context['pannes_len'] = len(context['pannes_vehicule'])
        except:
            context['pannes_vehicule']= []
        context['object'] = obj
        try:
            context["panne_list"] = [[panne for panne in entree.pannes.all()] for entree in obj.entrevehicule_set.all()]
        except:
            context["panne_list"] = []
        return render(request, "template/vehicule_detail.html", context)
    
    # Recherche par texte
    vehicules = Vehicule.objects.all()
    search_query = request.GET.get('q')
    if search_query:
        vehicules = vehicules.filter(
            Q(proprietaire__nom__icontains=search_query) |
            Q(proprietaire__prenom__icontains=search_query) |
            Q(immatriculation__icontains=search_query) |
            Q(couleur__icontains=search_query) |
            Q(model__libelle__icontains=search_query)
        )

    # Filtrage par carburant
    carburant_filter = request.GET.get('carburant')
    if carburant_filter:
        vehicules = vehicules.filter(carburant=carburant_filter)

    # presence_filter = request.GET.get('presence') #date(2024, 5, 15) 
    if request.GET.get('presence') == "present":
        vehicules = Vehicule.objects.filter(entrevehicule__state=True).distinct()
    if request.GET.get('presence') == "absent":
        vehicules = Vehicule.objects.filter(entrevehicule__state=False).distinct()
    
    context['objects'] = vehicules
    context["Vehicule"] = Vehicule
    return render(request, "template/vehicule_list.html", context)

@authentication_required
def vehicule_entree_view(request, pk=None):
    context = {}
    if pk is not None:
        obj = Vehicule.objects.get(pk=pk)
        context['objects'] = EntreVehicule.objects.filter(vehicule=obj)
        context['object'] = obj
        return render(request, "template/vehicule_entree_detail.html", context)
    
@authentication_required
def vehicule_view_form(request, pk=None):
    context= {}
    if pk:
        vehicule = Vehicule.objects.get(pk=pk)
        context["pk"] = pk
    else:
        vehicule = None
    if request.method == 'POST':
        form = VehiculeForm(request.POST, instance=vehicule)
        if form.is_valid():
            instance=form.save()
            return redirect('vehicule-detail', pk=instance.pk)
    else:
        form = VehiculeForm(instance=vehicule)
    context["form"]=form
    return render(request, 'template/vehicule_form.html', context)


# for clients
@authentication_required
def client_view_form(request, pk=None):
    context= {}
    if pk:
        client = Client.objects.get(pk=pk)
        context["client_pk"] = pk
    else:
        client = None
    if request.method == 'POST':
        form = ClientForm(request.POST, request.FILES, instance=client)
        if form.is_valid():
            instance=form.save()
            return redirect('detail-client', pk=instance.pk)
    else:
        form = ClientForm(instance=client)
    context["form"]=form
    return render(request, 'template/client_form.html', context)

@authentication_required
def client_view(request, pk=None):
    context = {}
    if pk is not None:
        obj = Client.objects.get(pk=pk)
        context['object'] = obj
        return render(request, "template/client_detail.html", context)

    clients = Client.objects.all()
    search_query = request.GET.get('q')
    if search_query:
        clients = clients.filter(
            Q(nom__icontains=search_query) |
            Q(prenom__icontains=search_query) |
            Q(tel__icontains=search_query) 
        )
    context['objects'] = clients 
    return render(request, "template/client_list.html", context)

@authentication_required
def panne_view(request, pk=None):
    context = {}
    if pk is not None:
        obj = Panne.objects.get(pk=pk)
        context['cout_T_piece'] = sum([piece.prix * QuantitePiece.objects.get(panne=obj, piece=piece).quantite for piece in obj.piece.all()])
        context['nb_T_piece'] = sum([QuantitePiece.objects.get(panne=obj, piece=piece).quantite for piece in obj.piece.all()])
        context['object'] = obj
        context['cout_total'] = context['cout_T_piece']+context['object'].cout
        return render(request, "template/panne_detail.html", context)

    # Filtrer les pannes par recherche si un terme de recherche est fourni dans la requête GET
    pannes = Panne.objects.all()
    search_query = request.GET.get('q')
    if search_query:
        pannes = pannes.filter(
            Q(libelle__icontains=search_query) |
            Q(cout__icontains=search_query) 
        )
    context['objects'] = pannes 
    return render(request, "template/panne_list.html", context)

@authentication_required
def panne_view_form(request, pk=None):
    context= {}
    if pk is not None:
        panne = Panne.objects.get(pk=pk)
        context["pk"] = pk
    else:
        panne = None
    if request.method == 'POST':
        form = PanneForm(request.POST, instance=panne)
        if form.is_valid():
            instance=form.save()
            return redirect('panne-detail', pk=instance.pk)
    else:
        form = PanneForm(instance=panne)
    context["form"]=form
    return render(request, 'template/panne_form.html', context)

@authentication_required
def panne_piece_view(request, pk=None):
    context = {}
    if pk is not None:
        obj = get_object_or_404(Panne, pk=pk)
        context['objects'] = QuantitePiece.objects.filter(panne=obj)
        context['object'] = obj
        return render(request, "template/panne_piece_detail.html", context)

@authentication_required
def piece_view_form(request, pk=None):
    context= {}
    if pk:
        piece = Piece.objects.get(pk=pk)
        context["pk"] = pk
    else:
        piece = None
    if request.method == 'POST':
        form = PieceForm(request.POST, request.FILES, instance=piece)
        if form.is_valid():
            instance=form.save()
            return redirect('piece-detail', pk=instance.pk)
    else:
        form = PieceForm(instance=piece)
    context["form"]=form
    return render(request, 'template/piece_form.html', context)


@authentication_required
def piece_view(request, pk=None):
    context = {}
    if pk :
        obj = get_object_or_404(Piece, pk=pk)
        context["object"] = obj  
        return render(request, "template/piece_detail.html", context)

    # Filtrer les pannes par recherche si un terme de recherche est fourni dans la requête GET
    pieces = Piece.objects.all()
    search_query = request.GET.get('q')
    if search_query:
        pieces = pieces.filter(
            Q(libelle__icontains=search_query) |
            Q(prix__icontains=search_query) 
        )
    context['objects'] = pieces
    return render(request, "template/piece_list.html", context)

@authentication_required
def quantite_piece_form(request, pk=None):
    context= {}
    if pk:
        qty_piece = QuantitePiece.objects.get(pk=pk)
        context["pk"] = pk
        context['object'] = qty_piece
    else:
        qty_piece = None
    if request.method == 'POST':
        form = PieceQtyForm(request.POST, instance=qty_piece)
        if form.is_valid():
            instance = form.save()
            return redirect('panne-piece-list', pk=instance.panne.pk)
    else:
        form = PieceQtyForm(instance=qty_piece)
    context["form"] = form
    return render(request, 'template/piece_qty_form.html', context)

@authentication_required
def piece_view_form(request, pk=None):
    context= {}
    if pk:
        piece = Piece.objects.get(pk=pk)
        context["pk"] = pk
    else:
        piece = None
    if request.method == 'POST':
        form = PieceForm(request.POST, request.FILES, instance=piece)
        if form.is_valid():
            instance=form.save()
            return redirect('piece-detail', pk=instance.pk)
    else:
        form = PieceForm(instance=piece)
    context["form"]=form
    return render(request, 'template/piece_form.html', context)


@authentication_required
def piece_view(request, pk=None):
    context = {}
    if pk :
        obj = Piece.objects.get(pk=pk)
        context["object"] = obj  
        return render(request, "template/piece_detail.html", context)

    # Filtrer les pannes par recherche si un terme de recherche est fourni dans la requête GET
    pieces = Piece.objects.all()
    search_query = request.GET.get('q')
    if search_query:
        pieces = pieces.filter(
            Q(libelle__icontains=search_query) |
            Q(prix__icontains=search_query) 
        )
    context['objects'] = pieces
    return render(request, "template/piece_list.html", context)

@authentication_required
def etat_panne_form(request, pk=None):
    """from quantiteform"""
    context= {}
    if pk:
        entre_panne = EntrePanne.objects.get(pk=pk)
        context["pk"] = pk
        context['object'] = entre_panne
    else:
        entre_panne = None
    if request.method == 'POST':
        form = EntrePanneForm(request.POST, instance=entre_panne)
        if form.is_valid():
            instance = form.save()
            return redirect('entre_vehicule_panne-list', pk=instance.pk)
    else:
        form = EntrePanneForm(instance=entre_panne)
    context["form"] = form
    return render(request, 'template/pannes_etat.html', context)

@authentication_required
def entree_panne_form(request, pk=None):
    context= {}
    if pk:
        entree_panne = EntrePanne.objects.get(pk=pk)
        context["pk"] = pk
    else:
        entree_panne = None
    if request.method == 'POST':
        form = PieceForm(request.POST, instance=entree_panne)
        if form.is_valid():
            form.save()
            return redirect('entree_panne-detail', pk=pk)
    else:
        form = PieceForm(instance=entree_panne)
    context["form"] = form
    return render(request, 'template/entree_panne_form_list.html', context)


def entre_vehicule_technicien_view(request, pk=None):
    context = {}
    if pk:
        obj = EntreVehicule.objects.get(pk=pk)
        context['objects'] = obj.techniciens.all()
        context['object'] = obj
        return render(request, "template/entre_vehicule_technicien_list.html", context)
    
@authentication_required
def sortie_vehicule_create(request):
    if request.method == 'POST':
        form = SortieVehiculeForm(request.POST)
        if form.is_valid():
            instance = form.save()
            entre_vehicule = EntreVehicule.objects.get(pk=instance.entre.pk)
            # Modifiez son état à False
            entre_vehicule.state = False
            entre_vehicule.save()
            return redirect('sortie-list')
    else:
        form = SortieVehiculeForm()
    return render(request, 'template/sortie_form.html', {'form': form})


@authentication_required
def sortie_vehicule_update(request, pk):
    sortie_vehicule = get_object_or_404(SortieVehicule, pk=pk)
    if request.method == 'POST':
        form = SortieVehiculeForm(request.POST, instance=sortie_vehicule)
        if form.is_valid():
            form.save()
            return redirect('sortie-list')
    else:
        form = SortieVehiculeForm(instance=sortie_vehicule)
    return render(request, 'template/sortie_form.html', {'form': form})


@authentication_required
def sortie_vehicule_list(request, pk=None):
    context = {}
    if pk and resolve(request.path_info).url_name == "vehicule_sortie-list":
        vehicule = get_object_or_404(Vehicule, pk=pk)
        # sorties = [entre.sortievehicule for entre in vehicule.entrevehicule_set.all()]
        sorties = SortieVehicule.objects.filter(entre__vehicule=vehicule)
        context["object"] = vehicule
    else:
        sorties = SortieVehicule.objects.all()

    # Filtrage des entrées en fonction des paramètres de requête
    date_filter = request.GET.get('date')
    libelle_filter = request.GET.get('q')

    if date_filter:
        sorties = sorties.filter(moment=date_filter)
    if libelle_filter:
        sorties = sorties.filter(entre__vehicule__libelle__icontains=libelle_filter)
    context['objects'] = sorties
    return render(request, 'template/sortie_list.html', context) 
