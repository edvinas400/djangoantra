from django.shortcuts import reverse, redirect, render, get_object_or_404
from django.http import HttpResponse
# from .forms import UzsakymoReviewForm
from django.views import generic
from django.views.generic.edit import FormMixin
from .models import *
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    projektu_kiekis = Projektas.objects.count()
    darbuotoju_kiekis = Darbuotojas.objects.count()
    klientu_kiekis = Klientas.objects.count()
    num_visits = request.session.get("num_visits", 1)
    request.session["num_visits"] = num_visits + 1

    informacija = {
        'projektu_kiekis': projektu_kiekis,
        'darbuotoju_kiekis': darbuotoju_kiekis,
        'klientu_kiekis': klientu_kiekis,
        "vizitai" : num_visits,
    }
    return render(request, 'index.html', context=informacija)
class UserProjektaiListView(generic.ListView):
    model = Projektas
    paginate_by = 1
    template_name = "userprojektai.html"
    context_object_name = "projektai"
    def get_queryset(self):
        return Projektas.objects.filter(vadovas=self.request.user)
class ProjektaiListView(generic.ListView):
    model = Projektas
    paginate_by = 1
    template_name = "projektai.html"
    context_object_name = "projektai"
class ProjektaiDetailView(generic.DetailView):
    model = Projektas
    template_name = "projektas.html"
    context_object_name = "projektas"

@csrf_protect
def register(request):
    if request.method == "POST":
        # pasiimame reikšmes iš registracijos formos
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # tikriname, ar sutampa slaptažodžiai
        if password == password2:
            # tikriname, ar neužimtas username
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Vartotojo vardas {username} užimtas!')
                return redirect('register')
            else:
                # tikriname, ar nėra tokio pat email
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'Vartotojas su el. paštu {email} jau užregistruotas!')
                    return redirect('register')
                else:
                    # jeigu viskas tvarkoje, sukuriame naują vartotoją
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.info(request, f'Vartotojas {username} užregistruotas!')
                    return redirect('login')
        else:
            messages.error(request, 'Slaptažodžiai nesutampa!')
            return redirect('register')
    return render(request, 'register.html')
