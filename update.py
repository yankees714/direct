#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import sqlite3
import os
import string

from robobrowser import RoboBrowser
import psycopg2


if "USERNAME" in os.environ:
    USERNAME = os.environ['USERNAME']
else:
    USERNAME = ""
if "PASSWORD" in os.environ:
    PASSWORD = os.environ['PASSWORD']
else:
    PASSWORD = ""


if os.getcwd() == "/app":
    conn_string = "host='ec2-54-225-105-169.compute-1.amazonaws.com' dbname='dct2sfiea871d8' user='nldurbrhtujxzj' password='bqJaaIxKpfVhrYd-svszgiGeLE'"
    connection = psycopg2.connect(conn_string)
else:
    connection = sqlite3.connect('oracleapp/default.db')

db = connection.cursor()

db.execute('''DROP TABLE search_person''')
db.execute('''CREATE TABLE search_person (id int, fname text, mname text, lname text, suffix text, year int, su text, email text, phone text, apt text)''')
connection.commit()


browser = RoboBrowser()
letters = [letter for letter in string.ascii_lowercase]
id = 1

# Login
browser.open('https://www.bowdoin.edu/BowdoinDirectory/rmSignon.jsp')
form = browser.get_forms()[1]
form["uname"] = USERNAME
form["pword"] = PASSWORD
print "Logging in...",
browser.submit_form(form)

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
        
        # Year
        matches = re.findall(r"\'(\d*)", info[1])
        if matches:
            year = "20" + matches[0]
        else:
            year = ""


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
            su = "Unknown"
        if not email:
            email = "Unknown"
        if not apt:
            apt = "Unknown"
        if not re.match("[0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]", phone):
            phone = "Unknown"

        print fname, mname, lname
        print year


        # Save to database
        if os.getcwd() == "/app":   #postgres
            db.execute("INSERT INTO search_person VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (id, fname, mname, lname, suffix, year, su, email, phone, apt))
        else:   #sqlite
            db.execute("INSERT INTO search_person VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (id, fname, mname, lname, suffix, year, su, email, phone, apt))
        connection.commit()

        id+=1

    browser.back()

db.close()
