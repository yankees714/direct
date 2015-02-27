#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import os
import string
import subprocess

from robobrowser import RoboBrowser

from search.models import Person


if "BOWDOIN_USERNAME" in os.environ:
    USERNAME = os.environ['BOWDOIN_USERNAME']
else:
    USERNAME = ""
if "BOWDOIN_PASSWORD" in os.environ:
    PASSWORD = os.environ['BOWDOIN_PASSWORD']
else:
    PASSWORD = ""

# Reset the database
subprocess.call(["python", "manage.py", "reset", "search"])

browser = RoboBrowser()
letters = [letter for letter in string.ascii_lowercase]

# Login
browser.open('https://www.bowdoin.edu/BowdoinDirectory/rmSignon.jsp')
form = browser.get_forms()[1]
form["uname"] = USERNAME
form["pword"] = PASSWORD
print "Logging in...",
browser.submit_form(form)

# Only do external access
# browser.open("http://www.bowdoin.edu/BowdoinDirectory/lookup.jsp")

# Make sure we actually logged in
if browser.select("#sch"):
    print "done!"
else:
    print "FAILED."
    quit()

for letter in letters:
    # Get all students with last name beginning with letter
    form = browser.get_form(id='sch')
    form["ln"].value = letter
    form["so"].value = "stu"
    browser.submit_form(form)

    students = browser.select('.person')

    for student in students:
        header = student.select("h3")
        info = header[0].text.split("\n")

        # Name, class year
        name = info[0].strip()

        lname = name.split(", ")[0].strip()
        given = name.split(", ")[1].strip()

        if len(name.split(", ")) == 3:
            suffix = name.split(", ")[2]
        else:
            suffix = ""

        fname = given.split(" ")[0].strip()
        mname = ' '.join(given.split(" ")[1:])

        print fname, mname, lname

        # Year
        matches = re.findall(r"\'(\d*)", info[1])
        if matches:
            year = 2000 + int(matches[0])
        else:
            year = 0


        # Picture
        img_url = ""
        for img in student.select("img"):
            # Only choose the image if it's in the right directory
            if "dirphotos" in img["src"]:
                img_url = img["src"]


        # Details - mailbox, email, dorm, phone
        details = student.select(".pdetail")[0].text
        details = details.split("\n\n\n")

        su = ""
        email = ""
        apt = ""
        phone = ""

        for d in details:
            if ":" in d:
                value = d.split(":")[1].strip()
                if "Campus Mail" in d:
                    su = value.replace("Smith Union", "")
                elif "Email" in d:
                    email = value
                elif "Residence" in d:
                    apt = value
                elif "Phone" in d:
                    phone = value

        if not su:
            su = "None"
        if not email:
            email = "Unknown"
        if not apt:
            apt = "Off Campus/Unknown"
        if not re.match("[0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]", phone):
            phone = "Unknown"

        print year

        Person.objects.create(
            fname=fname,
            mname=mname,
            lname=lname,
            suffix=suffix,
            year=year,
            su=su,
            email=email,
            phone=phone,
            apt=apt,
            img_url=img_url
        )

    browser.back()
