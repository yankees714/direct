# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, render_to_response
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from django.template import Context, loader
from Levenshtein import ratio, distance
from bisect import insort, bisect
import sys

from search.models import Person


class IndexView(generic.ListView):
    template_name = 'search/index.html'
    context_object_name = 'all_people'

    def get_queryset(self):
        return Person.objects.all()

class DetailView(generic.DetailView):
    model = Person
    template_name = 'search/detail.html'

    def get_queryset(self):
        return Person.objects.all()


def SearchView(request):
    #if request.is_ajax():
        query = request.GET.get('q')
        if query is not None:
            search_results = list()
            ratio_results = list()
            for person in Person.objects.all():
                best_ratio = 0
                for field in (person.fname.upper(), person.lname.upper(), person.full_name().upper(), person.su.upper(), person.email.upper(), person.apt.upper()):
                    this_ratio = ratio(query.upper(), field)
                    if this_ratio > best_ratio:
                        best_ratio = this_ratio
                mountpoint = bisect(ratio_results, best_ratio)
                ratio_results.insert(mountpoint, best_ratio)
                search_results.insert(len(search_results)-mountpoint, person)
            template = loader.get_template('search/search.html')
            context = Context({'search_results': search_results})
            return HttpResponse(template.render(context))
        else:
            return HttpResponse("No query.")
    #else:
    #    return HttpResponse("No external access allowed.")


def handler404(request):
    output = "404: the path " + request.path + " was not found on this server."
    return HttpResponse(output)


def handler500(request):
    return HttpResponse("500")


def RepopView(request):
    if not request.user.is_staff:
        return Http404
    else:
        from subprocess import call
        retcode = call(["/Users/bjacobel/code/www/oracleapp/unpdf.py", "arg1"])
        if retcode == 0:
            output = "Database refreshed."
        else:
            output = "Refreshing database failed. Check the PDF file and the path to the script."
    return HttpResponse(output)
