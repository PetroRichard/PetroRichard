
"""
Demo: handle incoming calls

Simple demo app that listens for incoming calls, displays the caller ID,
optionally answers the call and plays some DTMF tones (if supported by modem),
and hangs up the call.
"""
#!/usr/bin/env python
from __future__ import print_function

import time, logging
import re
from SmsHandler import *
import glob

PORT = 'COM9'
BAUDRATE = 9600
modem=None
PIN = None # SIM card PIN (if any)
from  gsmmodem.modem import Call
from  dbms import DBMS
# appreciation=['thanks','Thanks','poa',"Poa","Wow","wow",'shwari','asante','Asante','safi''Oyoo','oyoo','sawa','Sawa','good']


from gsmmodem.modem import GsmModem
from gsmmodem.exceptions import InterruptedException
mydb=DBMS('localhost',"root",'dawasa','')
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

def connectModemNew(mod):
    for x in glob.glob('/dev/cu*'):
            port=x
            print(port)
        
            try:
                mod = GsmModem(port, BAUDRATE,smsReceivedCallbackFunc=handleSmsDemo,smsStatusReportCallback=handleStatus)
                mod.connect("")
                print("modem connected successfull in port COM{}".format(port))
                return mod
                break
            except:
                continue
    # print("faile to connect")
            
def handleStatus(Sms):
    print(Sms+"received")
def handleSmsDemo(Sms):
     print("{} from {}".format(Sms.text,Sms.number))
     try:

            if (Sms.number!=""):
                text=Sms.text
                transaction_id,amount,mobile=getDetails(text)
                amount=amount.replace(',','')
                name=getPerson(text)
                print("{}:{}:{}".format(transaction_id,amount,name))
                if(transaction_id!="" or transaction_id!=None or amount!=""):
                    mydb.transaction(transaction_id,amount,name,mobile)
            else :
                print("Invalid sender sent")
                modem.sendSms(Sms.number,"Utapata tabu sana kipigo chake ni cha mbwakoko")
     except Exception as error:
            print(error)
    
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
    
    # modem.sendSms("+255758283632","5G231HJ8SNH Imethibitishwa. Umepokea  Tsh8,554.00 kutoka 255765532811 - RICHARD PETER  mnamo 2/7/18 saa 11:21 AM Baki yako ya M-Pesa ni Tsh9,577.00.")
    # while True:
    #     try:
    #         modem.deleteStoredSms(0)
    #     except: 
    #         print("error")
    #     finally:
    #         print("all messages deleted")
    #         break
    #         print('Waiting for incomming messages')

    try:
         for msg in modem.listStoredSms(memory="MT"):
            print(msg.text)
            try:
                modem.deleteStoredSms(0)
            except:
                print("failed")

    except:
        print("no- messages")
   
    while True:
        try:
            #modem.sendSms("+255622592055","hello veda")

            #call=Call(modem,0,0,"+255622592055")
            pass

        finally:
            pass
            #print("messageSent")
    modem.close()

if __name__ == '__main__':
        main()
    