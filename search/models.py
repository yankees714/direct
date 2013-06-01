from django.db import models

class Person(models.Model):
    fname = models.CharField(max_length=40)
    mname = models.CharField(max_length=40)
    lname = models.CharField(max_length=40)
    suffix = models.CharField(max_length=3)
    year = models.IntegerField()
    su = models.IntegerField()
    email = models.EmailField(max_length=20)
    phone = models.CharField(max_length=8)
    apt = models.CharField(max_length=40)

    def on_campus(self):
        return (self.apt != "Off-Campus or Unknown" and self.apt != "Off-Campus Study")

    def __unicode__(self):
        return self.fname + " " + self.lname

    on_campus.boolean = True
    on_campus.short_description = "On Campus?"

