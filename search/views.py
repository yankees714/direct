# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.core.cache import cache
from django.views import generic
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.template import Context, loader
from Levenshtein import ratio
from itertools import combinations
import sys
import re

from search.models import Person


class IndexView(generic.ListView):
    template_name = 'search/index.html'
    context_object_name = 'all_people'

    def get_queryset(self):
        return Person.objects.all()

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(IndexView, self).dispatch(*args, **kwargs)


class DetailView(generic.DetailView):
    model = Person
    template_name = 'search/detail.html'

    def get_queryset(self):
        return Person.objects.all()


def LegalView(request):
    return render(request, 'search/legal.html')


def SearchView(request):
    def similarity_to_query(s):
        query_lower = query.lower()

        # Lolz
        keywords = ["gym", "dining", "james bond"]
        if any(query_lower == w for w in keywords) and s.fname == "Franco":
            return -1

        fields = (s.fname, s.lname, s.full_name(), s.su, s.email, s.apt)
        return min(-ratio(f.lower(), query_lower) for f in fields if f)

    if request.is_ajax():
        if 'q' in request.GET:
            query = request.GET['q']
            result = cache.get(query.replace(" ", "-"))

            if not result:
                all_people = cache.get("all_people")

                if not all_people:
                    all_people = Person.objects.all()
                    cache.set("all_people", all_people, 3600)

                if query:
                    result = sorted(all_people, key=similarity_to_query)[:30]
                else:
                    result = []    # Only return results for nonempty queries

                cache.set(query.replace(" ", "-"), result, 3600)

            template = loader.get_template('search/search.html')
            context = Context({'search_results': result})
            return HttpResponse(template.render(context))
        else:
            return HttpResponse('')
    else:
        return HttpResponse("No external access allowed.")


def LoginView(request):
    return render(request, 'search/login.html')


def handler404(request):
    output = "404: the path " + request.path + " was not found on this server."
    return HttpResponse(output)


def handler500(request):
    return HttpResponse("500")


def KeepAliveView(request):
    return render(request, 'search/keepalive.html')
