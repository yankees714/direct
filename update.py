#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import sqlite3
import os
import string

from robobrowser import RoboBrowser
# import psycopg2


# if os.getcwd() == "/app":
#     conn_string = "host='ec2-54-225-105-169.compute-1.amazonaws.com' dbname='dct2sfiea871d8' user='nldurbrhtujxzj' password='bqJaaIxKpfVhrYd-svszgiGeLE'"
#     connection = psycopg2.connect(conn_string)
# else:
connection = sqlite3.connect('oracleapp/default.db')

db = connection.cursor()

db.execute('''DROP TABLE search_person''')
db.execute('''CREATE TABLE search_person (id int, fname text, mname text, lname text, suffix text, year int, su text, email text, phone text, apt text)''')
connection.commit()


browser = RoboBrowser()
letters = [letter for letter in string.ascii_lowercase]
id = 1

for letter in letters:
    browser.open('http://www.bowdoin.edu/BowdoinDirectory/lookup.jsp')

    form = browser.get_form(id='sch')
    form["ln"].value = letter
    form["so"].value = "stu"

    browser.submit_form(form)

    students = browser.select('.person')
    for student in students:
        header = student.select("h3")
        info = header[0].text.split("\n")

        # Name
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
            year = "20" + matches[0]
        else:
            year = "" 
        print year


        details = student.select(".pdetail")
        details = details[0].text.replace("\n"," ")

        # Dorm
        su = ""
        
        # Email
        matches = re.findall(r"Email:   (.*\@bowdoin\.edu)", details)
        if matches:
            email = matches[0]
        else:
            email = ""
        print email

        # Phone
        phone = ""
        if not re.match("[0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]", phone):
            phone = "Unknown"

        # the dorms are super hard because they're not a constant number of words and occasionally don't exist
        apt = ""


        if os.getcwd() == "/app":   #postgres
            db.execute("INSERT INTO search_person VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (id, fname, mname, lname, suffix, year, su, email, phone, apt))
        else:   #sqlite
            db.execute("INSERT INTO search_person VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (id, fname, mname, lname, suffix, year, su, email, phone, apt))
        connection.commit()

        id+=1

db.close()
