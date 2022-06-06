pattern="(.*)\s+Imethibitishwa\s+tarehe\s+([.])\s+saa\s+(\d+:\d+)\s+AM\s+Toa\s+Tsh([\d|.|,])\s+"
date="(\d+/\d+/\d+)"
person_pattern="-\s([\w+|\s]+)\s+mnamo"
money="Umepokea\s+Tsh((\d{1,3})(,\d{1,3})*(\.\d{1,})?)"
transaction="([\w|\d]+)\s+Imethibitishwa"
mobile_pattern="kutoka\s*(\d+)\s+"
import  re
import json
def getPerson(message):
     person = re.findall(person_pattern, message)[0]
     return person

def getDetails(message):
     money_received=re.findall(money,message)[0][0]
     transaction_id=re.findall(transaction,message)[0]
     mobile=re.findall(mobile_pattern,message)[0]
     return transaction_id,money_received,mobile
if __name__=="__main__":
     with open("msg.json") as msgFile:
          data=json.load(msgFile)
          msgFile.close()
          msg=data["fromPerson"]["msg"]
          print(getPerson(msg,person_pattern))
          print(getDetails(msg))
     