# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, render_to_response
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from django.template import Context, loader
from itertools import chain

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


def SearchView(request, query_string):
    # return a list of everyone whose name, email or address contains the query string
    # no ranking or fuzzy matching yet
    filtered_people = list(chain(
        Person.objects.filter(fname__contains=query_string),
        Person.objects.filter(lname__contains=query_string),
        Person.objects.filter(apt__contains=query_string),
        Person.objects.filter(email__contains=query_string)
        ))
    template = loader.get_template('search/search.html')
    context = Context({'filtered_people' : filtered_people})
    return HttpResponse(template.render(context))


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
