# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

from search.models import Person

class IndexView(generic.ListView):
    template_name = 'search/index.html'
    context_object_name = 'all_people'

    def get_queryset(self):
        return Person.objects.filter()


class DetailView(generic.DetailView):
    model = Person
    template_name = 'search/detail.html'

    def get_queryset(self):
        """
        Excludes any polls that aren't published yet.
        """
        return Person.objects.filter()

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
