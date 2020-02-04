#!/usr/bin/python3 

import cgi
import cgitb
import hashlib, binascii, os
cgitb.enable()
from jinja2 import Template, Environment, FileSystemLoader

import os, sys
import imp
import constants
from authorizenet import apicontractsv1
from authorizenet.apicontrollers import *
constants = imp.load_source('modulename', 'constants.py')

print("Content-type: text/html")
print()
print("<br>")

form_data = cgi.FieldStorage()

cardnumber = form_data['cardnumber'].value
expirationDate = form_data["expmonth"].value
name= form_data["cardname"].value

import pymysql
from pymysql.err import MySQLError

conn = pymysql.connect(
    db='pyb78',
    user='pyb78',
    passwd='sbe5kT84',
    host='localhost')
c = conn.cursor()

try:
    
   sql1= 'select username from register where first_name="%s"' %(name)
   c.execute(sql1)
   row1 = c.fetchone()
   username = row1[0]
   #print(sql1)
   conn.commit()
   
   sql2= 'select customer_profile_id from payment_page where username="%s"' %(username)
   c.execute(sql2)
   row2 = c.fetchone()
   customer_profile_id = row2[0]
   #print(sql2)
   conn.commit()

except MySQLError as e:
    print('Got error {!r}, errno is {}'.format(e, e.args[0]))

    
#print(customer_profile_id)
merchantAuth = apicontractsv1.merchantAuthenticationType()
merchantAuth.name = constants.apiLoginId
merchantAuth.transactionKey = constants.transactionKey

creditCard = apicontractsv1.creditCardType()
creditCard.cardNumber = cardnumber
creditCard.expirationDate = expirationDate

payment = apicontractsv1.paymentType()
payment.creditCard = creditCard

billTo = apicontractsv1.customerAddressType()
billTo.firstName = name

profile = apicontractsv1.customerPaymentProfileType()
profile.payment = payment
profile.billTo = billTo


createCustomerPaymentProfile = apicontractsv1.createCustomerPaymentProfileRequest()
createCustomerPaymentProfile.merchantAuthentication = merchantAuth
createCustomerPaymentProfile.paymentProfile = profile

createCustomerPaymentProfile.customerProfileId = str(customer_profile_id)

controller = createCustomerPaymentProfileController(createCustomerPaymentProfile)
controller.execute()

response = controller.getresponse()

paymentprofileid=response.customerPaymentProfileId

#print(paymentprofileid)
    
try:

   sql3 = 'update payment_page set payment_profile_id = "%s" where username="%s"' %(paymentprofileid,username)
   #print(sql3)
   c.execute(sql3)
   conn.commit()


except MySQLError as e:
    print('Got error {!r}, errno is {}'.format(e, e.args[0])) 


#try:

   #sql2='SELECT user_id  into @user_id FROM register where username="%s"' %(username)
   #sql2 = 'SELECT user_id FROM register where username="%s"' %(username)
   #print(sql2)
   #c.execute(sql2)
   
   

#except MySQLError as e:
 #   print('Got error {!r}, errno is {}'.format(e, e.args[0])) 




#'''env = Environment(loader=FileSystemLoader('templates'))
#template = env.get_template('output.html')
#output_from_parsed_template = template.render(firstname=First_Name,lastname=Last_Name,Email=email,Phone_Number=Phone_No,Username=username,Password=password,salt=salt)

#try:
 #  fh = open("output.html", "w")
  # fh.write(output_from_parsed_template)
#except IOError:
 #  print ("<br>Error: can't find file or read data")
#else:
 #  print ("Written content in the file successfully")'''

#print("Content-type:text/html\n\n")
redirectURL = " http://pyb78.specind.net/index.html"
print("<html>")
print("<head>")
print('<meta http-equiv="refresh" content="0;url='+str(redirectURL)+'" />')
print("</head>")
print ("</html>")
