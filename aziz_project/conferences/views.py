from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from .models import Conference
from django.views.generic import ListView,DetailView
# Create your views here.

def conferencelist(request):
    liste=Conference.objects.all()
    return render (request,'conferences/conferencelist.html',
                   {'conferences_list':liste })
class ConferenceListView(ListView):
    model=Conference
    #template_name='conferences/conference_liste.html' si n'est pas le meme nom par defaut
    context_object_name='conferences'
    def get_queryset(self) :
        return Conference.objects.order_by('-start_date')
class DetailViewConference(DetailView):
    model=Conference
    template_name='conferences/conference_detail_view.html'
    context_object_name = 'conf'