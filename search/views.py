# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

from search.models import Person

class IndexView(generic.ListView):
    # template_name = 'search/index.html'

    def get_queryset(self):
        return Person.objects.filter()


class DetailView(generic.DetailView):
    model = Person
    # template_name = 'search/detail.html'

    def get_queryset(self):
        """
        Excludes any polls that aren't published yet.
        """
        return Poll.objects.filter()
