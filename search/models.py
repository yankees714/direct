# -*- coding: utf-8 -*-

from django.db import models
import sys

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

    def format_yr(self):
        if self.year:
            # return "’" + unicode(self.year)[2:]
            return "'" + unicode(self.year)[2:]
        else:
            return ""

    def shortname_yr(self):
        return self.fname + " " + self.lname + " " + self.format_yr()

    def full_name(self):
        fullname = self.fname
        if self.mname:
            fullname += " " + self.mname + " " + self.lname
        else:
            fullname += " " + self.lname
        if self.suffix:
            fullname += ", " + self.suffix
        return fullname

    def __unicode__(self):
        return self.fname + " " + self.lname

    def uname(self):
        return self.email.split('@')[0]

    def image_path(self):
        path = 'img/pics/'+self.uname()+'.jpg'
        try:
            with open('oracleapp/assets/'+path):
                pass
        except IOError:
            return 'img/nopic.png'
        else:
            return path

    def has_pic(self):
        path = 'img/pics/'+self.uname()+'.jpg'
        try:
            with open('oracleapp/assets/'+path):
                pass
        except IOError:
            return False
        else:
            return True

    on_campus.boolean = True
    has_pic.boolean = True
    on_campus.short_description = "On Campus?"
    has_pic.short_description = "Picture?"
