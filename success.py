#!/usr/bin/python3 

import os, sys, cgi
import imp
import constants
import cgitb; cgitb.enable()
from jinja2 import Template, Environment, FileSystemLoader
import json
from authorizenet import apicontractsv1
from authorizenet.apicontrollers import *
constants = imp.load_source('modulename', 'constants.py')
from decimal import *

print("Content-Type: text/html")
print()
print("<br>")
form = cgi.FieldStorage()

customerProfileId=form['customer_profile_id'].value
paymentProfileId= form['payment_profile_id'].value
amount = '1.32'
merchantAuth = apicontractsv1.merchantAuthenticationType()
merchantAuth.name = constants.apiLoginId
merchantAuth.transactionKey = constants.transactionKey


    # create a customer payment profile
profileToCharge = apicontractsv1.customerProfilePaymentType()
profileToCharge.customerProfileId = customerProfileId
profileToCharge.paymentProfile = apicontractsv1.paymentProfile()
profileToCharge.paymentProfile.paymentProfileId = paymentProfileId

transactionrequest = apicontractsv1.transactionRequestType()
transactionrequest.transactionType = "authCaptureTransaction"
transactionrequest.amount = amount
transactionrequest.profile = profileToCharge


createtransactionrequest = apicontractsv1.createTransactionRequest()
createtransactionrequest.merchantAuthentication = merchantAuth
createtransactionrequest.refId = '724117'

createtransactionrequest.transactionRequest = transactionrequest
createtransactioncontroller = createTransactionController(createtransactionrequest)
createtransactioncontroller.execute()

response = createtransactioncontroller.getresponse()

transaction_id = response.transactionResponse.transId
#print(transaction_id)
#desc =  response.transactionResponse.messages.message[0].description

env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('output.html')
output_from_parsed_template = template.render(trans_id =transaction_id)

try:
    fh = open("output.html", "w")
    fh.write(output_from_parsed_template)
except IOError:
    print ("<br>Error: can\'t find file or read data")
else:
    #print ("Written content in the file successfully")
    pass
#print('Content-type:text/html\n\n')
redirectURL = "http://pyb78.specind.net/successpage.html"
print('<html>')
print('<head>')
print('<meta http-equiv="refresh" content="0;url='+str(redirectURL)+'" />') 
print('</head>')
print('</html>')    
