#!/usr/bin/python3 

import cgi
import cgitb
import hashlib, binascii, os
cgitb.enable()
from jinja2 import Template, Environment, FileSystemLoader

print("Content-Type: text/html")
print()
print("<br>")
# Create instance of FieldStorage
form_data = cgi.FieldStorage()

# Get data from fields
username = form_data["username"].value
password = form_data["password"].value

#print(username)
#print(password)


import pymysql
from pymysql.err import MySQLError
#password1 = form_data["pwd"].value
#salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
conn = pymysql.connect(
    db='pyb78',
    user='pyb78',
    passwd='sbe5kT84',
    host='localhost')
#c = conn.cursor()
c =conn.cursor(pymysql.cursors.Cursor)
login_sql = 'SELECT salt FROM register WHERE username="%s"'
c.execute(login_sql % username)
row=c.fetchone()
usersalt=row[0]
conn.commit()
#print("\n Retreived: ",A[0])
#print(usersalt)

sql='SELECT password FROM register WHERE username="%s"'
c.execute(sql % username)
row1=c.fetchone()
userpwd=row1[0]
conn.commit()
#print(userpwd)

def verify_password(stored_password,stored_salt,provided_password):
   
    salt = usersalt
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',provided_password.encode('utf-8'),salt.encode('ascii'),100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    #print(pwdhash)
    return pwdhash == stored_password


is_authenticated_user = verify_password(userpwd,usersalt,password) 
#print(is_authenticated_user)


if (is_authenticated_user):
#    print("logged in")

    #env = Environment(loader=FileSystemLoader('templates'))
    #template = env.get_template('login.html')
    ##output_from_parsed_template = template.render(user=username,pswd=password)


    #try:
       #fh = open("output2.html", "w")
       #fh.write(output_from_parsed_template)
    #except IOError:
      # print ("<br>Error: can't find file or read data")
    #else:
      # print ("Written content in the file successfully")

    #print("Content-type:text/html\n\n")
    redirectURL = "http://pyb78.specind.net/index.html"
    print("<html>")
    print("<head>")
    print('<meta http-equiv="refresh" content="0;url='+str(redirectURL)+'" />')
    print("</head>")
    print ("</html>")

  
else:
#    print("Invalid Login")
    pass