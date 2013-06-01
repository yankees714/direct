from django.contrib import admin
from search.models import Person

class SearchAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['fname', 'mname', 'lname', 'suffix']}),
        ('Personal Info', {'fields': ['year', 'su', 'email', 'phone', 'apt'], 'classes': ['collapse']}),
    ]
    list_display = ('year', 'su', 'email', 'phone', 'apt', 'on_campus')
    list_filter = ['year']
    search_fields = ['fname', 'lname']

admin.site.register(Person, SearchAdmin)
