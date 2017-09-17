from django.views import generic
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404

from .models import Album, Foto
from .forms import UserForm


class IndexView(generic.ListView):
    template_name = 'albumbum/index.html'

    context_object_name = 'object_list'

    def get_queryset(self):
        return Album.objects.all()


class DetailView(generic.DetailView):
    model = Album
    template_name = 'albumbum/detail.html'


class AlbumCreate(LoginRequiredMixin, CreateView):
    model = Album
    fields = ['nazwa_albumu', 'temat', 'opis_albumu', 'album_logo']

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super(AlbumCreate, self).form_valid(form)


class AlbumUpdate(LoginRequiredMixin, UpdateView):

    model = Album
    fields = ['nazwa_albumu', 'temat', 'opis_albumu', 'album_logo']


class AlbumDelete(LoginRequiredMixin, DeleteView):
    model = Album
    success_url = reverse_lazy('albumbum:index')


class FotoCreate(CreateView):
    model = Foto
    fields = ['nazwa_foto', 'obraz']

    def form_valid(self, form):
        f = Album.objects.get(pk=self.kwargs.get('pk'))
        form.instance.albumnr = f
        return super(FotoCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('albumbum:detail', kwargs={'pk': self.kwargs.get('pk')})


class FotoDelete(DeleteView):
    model = Foto

    def get_success_url(self):
        fotoid = self.kwargs['pk']
        foto = get_object_or_404(Foto, pk=fotoid)
        album_id = foto.albumnr.pk
        return reverse('albumbum:detail', kwargs={'pk': album_id})


class FotoUpdate(LoginRequiredMixin, UpdateView):
    model = Foto
    fields = ['nazwa_foto', 'obraz']

    def get_success_url(self):
        fotoid = self.kwargs['pk']
        foto = get_object_or_404(Foto, pk=fotoid)
        album_id = foto.albumnr.pk
        return reverse('albumbum:detail', kwargs={'pk': album_id})


class UserFormView(View):
    form_user = UserForm
    template = 'albumbum/registration_form.html'

    # pokazuje formularz rejestracji
    def get(self, request):
        form = self.form_user(None)
        return render(request, self.template, {'form': form})

    # dodaje do bazy
    def post(self, request):
        form = self.form_user(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, 'Udało Ci się poprawnie zarejestrować, korzystaj z serwisu do woli! ;)')
                    return redirect('albumbum:register')

        return render(request, self.template, {'form': form})


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'albumbum/login.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, 'Udane logowanie, korzystaj z serwisu do woli! ;)')
                return redirect('albumbum:login_user')
            else:
                return render(request, 'albumbum/login.html', {'error_message': 'Twoje konto zostało wyłączone'})
        else:
            return render(request, 'albumbum/login.html', {'error_message': 'Nieprawidłowy login'})
    return render(request, 'albumbum/login.html')

