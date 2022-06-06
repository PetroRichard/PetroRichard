
"""
Demo: handle incoming calls

Simple demo app that listens for incoming calls, displays the caller ID,
optionally answers the call and plays sone DTMF tones (if supported by modem),
and hangs up the call.
"""

from __future__ import print_function

import time, logging
import re
from SmsHandler import *

PORT = 'COM5'
BAUDRATE = 115200
modem=None
PIN = None # SIM card PIN (if any)
from  gsmmodem.modem import Call
from  dbms import DBMS
appreciation=['thanks','Thanks','poa',"Poa","Wow","wow",'shwari','asante','Asante','safi''Oyoo','oyoo','sawa','Sawa','good']


from gsmmodem.modem import GsmModem
from gsmmodem.exceptions import InterruptedException
mydb=DBMS('localhost',"root",'tanesco','Richard@1212')
def connectModem(mod):
    for x in range(80):
        port="COM{}".format(x)
    
        try:
              mod = GsmModem(port, BAUDRATE,smsReceivedCallbackFunc=handleSms,smsStatusReportCallback=handleStatus)
              mod.connect("")
              print("modem connected successfull in port COM{}".format(x))
              return mod
              break
        except:
            continue
            
def handleStatus(Sms):
    print(Sms+"received")
def handleSms(Sms):
    print("{} from {}".format(Sms.text,Sms.number))
    replied=False
    global modem

    text=Sms.text
    print(text)
    print("person={}".format(getPerson(text)))
    #if (Sms.number=="M-PESA"or Sms.number=="+255765532811"):
    if (Sms.number!=""):
        transaction_id,amount=getDetails(text)
        amount=amount.replace(',','')
        name=getPerson(text)
        print("{}:{}:{}".format(transaction_id,amount,name))
        if(transaction_id!="" or transaction_id!=None or amount!=""):
            mydb.transaction(transaction_id,amount,name)
    else :
        print("invalid sender sent")
        modem.sendSms(Sms.number,"Utapata tabu sana kipigo chake ni cha mbwakoko")




    print("message sent")



def main():
    print('Initializing modem...')
    #logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    global modem
    modem=connectModem(modem)
    
   
    modem.sendSms("+255758283632","5G231HJ8SNH Imethibitishwa. Umepokea  Tsh8,554.00 kutoka 255765532811 - RICHARD PETER  mnamo 2/7/18 saa 11:21 AM Baki yako ya M-Pesa ni Tsh9,577.00.")
    while True:
        try:
            modem.deleteStoredSms(0)
        finally:
            print("all messages deleted")
            break


    print('Waiting for incomming messages')
    while True:
        try:
            #modem.sendSms("+255622592055","hello veda")

            #call=Call(modem,0,0,"+255622592055")
            '''
            for msg in modem.listStoredSms(memory="MT"):
                print(msg.text)
            modem.deleteStoredSms(0)
            '''



        finally:
            pass
            #print("messageSent")
    modem.close()

if __name__ == '__main__':
    main()