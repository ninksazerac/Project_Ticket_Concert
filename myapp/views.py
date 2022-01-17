from os import name
from typing import Pattern
from django.shortcuts import render,redirect
from json import dumps
import pickle
from datetime import datetime 
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.template import loader



zonesize = 20
now = datetime.now()
timedata = now.strftime("%d/%m/%Y %H:%M:%S")

class Node:
    def __init__(self, data=None, prev=None, next=None):
        self.next = next
        self.prev = prev
        self.data = data

class ClientNode(Node):
    def __init__(self, namedata, zonedata, numberdata =None, prev=None, next=None):
        self.zonedata = zonedata
        self.numberdata = numberdata
        super().__init__(namedata, prev, next)

    def __str__(self):
        return str(self.data+' '+self.zonedata+' '+str(self.numberdata))

class PaymentNode(ClientNode):
    def __init__(self, namedata, zonedata, numberdata,timedata, prev=None, next=None):
        super().__init__(namedata, zonedata, numberdata, prev, next)
        self.timedata = timedata

    def __str__(self):
        return str(self.timedata+' '+self.data+' '+self.zonedata+' '+str(self.numberdata))

class ClientDoublyLinkedList():
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0
        self.dummy = Node(None)
        self.dummyLast = Node(None)

    def enQueue(self, namedata, zonedata):
        B = ClientNode(namedata, zonedata)
        if self.size == 0:
            self.head = B
        else:
            B.prev = self.tail
            self.tail.next = B
        self.size += 1
        self.tail = B
        self.tail.numberdata = int(self.size)
        self.dummyLast.prev = self.tail


    def appendLast(self, namedata, zonedata, numberdata):
        B = ClientNode(namedata, zonedata, numberdata)
        if self.size == 0:
            self.head = B
        else:
            B.prev = self.tail
            self.tail.next = B

        self.tail = B
        self.dummyLast.prev = self.tail
        self.size += 1

    def appendFirst(self, namedata, zonedata, numberdata):
        B = ClientNode(namedata, zonedata, numberdata)
        if self.size == 0:
            self.tail = B
        else:
            h = self.head
            self.head.prev = B
            B.next = self.head

        self.head = B
        self.dummy.next = self.head
        self.size += 1

    def printNormal(self):
        if self.head is None :
            print("\t\t\t\tempty")
            return
        h = self.head
        text = ""
        while h.next is not None:
            text += "\t"+str(h.data) + " " + str(h.zonedata) + " " + str(h.numberdata) + "\n"
            h = h.next
        text += "\t"+str(h.data) + " " + str(h.zonedata) + " " + str(h.numberdata)
        print(text)

    def detail(self):
        t = self.tail
        collec1 = t.prev
        collec1.next = None
        t.prev = None
        self.tail = collec1

    def returnNotReserved(self):
        chairlist = list(range(1, 21))
        h = self.head
        while h.next is not None:
            if int(h.numberdata) in chairlist:
                chairlist.remove(int(h.numberdata))
            h = h.next
        print(chairlist)

    def findsameChair(self, chair):
        h = self.head
        same = False
        while h is not None:
            if int(h.numberdata) == int(chair):
                same = True
                return same
            h = h.next
        return same


    def bubblesortList(self):
        setLastGo = None
        swapped = False
        ''' Checking for empty list '''
        if (self.head == None):
            return
        while True:
            swapped = False
            h = self.head
            while (h.next != setLastGo):
                if (int(h.numberdata) > int(h.next.numberdata)):
                    h.data , h.zonedata , h.numberdata, h.next.data , h.next.zonedata , h.next.numberdata = h.next.data , h.next.zonedata , h.next.numberdata,h.data , h.zonedata , h.numberdata
                    swapped = True
                h = h.next
            setLastGo = h
            if swapped == False:
                break

    def bubblesortListHtL(self):
            setLastGo = None
            swapped = False
            ''' Checking for empty list '''
            if (self.head == None):
                return
            while True:
                swapped = False
                h = self.head
                while (h.next != setLastGo):
                    if (int(h.numberdata) < int(h.next.numberdata)):
                        h.data , h.zonedata , h.numberdata, h.next.data , h.next.zonedata , h.next.numberdata = h.next.data , h.next.zonedata , h.next.numberdata,h.data , h.zonedata , h.numberdata
                        swapped = True
                    h = h.next
                setLastGo = h
                if swapped == False:
                    break
          
    
    def SearchDataToFront(self, Cname):
        if self.head is None :
            return False
        else :
            h = self.head
            searchname = Cname.lower()
            count = 0
            while h is not None:
                if str(h.data.lower()) == str(searchname):
                    if str(h.data) == str(self.head.data):
                        return h.data , h.zonedata , h.numberdata
                    if str(h.data) == str(self.tail.data):
                        self.detail()
                        self.appendFirst(h.data,h.zonedata,h.numberdata)
                        return h.data , h.zonedata , h.numberdata
                    else:
                        p = h.prev
                        n = h.next
                        h.prev.next = n
                        h.next.prev = p
                        h.prev = None
                        h.next = None
                        self.appendFirst(h.data,h.zonedata,h.numberdata)
                        return h.data , h.zonedata , h.numberdata
                else:
                    count += 1
                    h = h.next

            else:
                return False



    def searchData(self,namedata,zonedata,numberdata = None ):
        h = self.head
        searchname = namedata.lower()
        searchzone = zonedata.lower()
        if numberdata is not None :

            while h is not None :
                if str(h.data.lower()) == str(searchname) and str(h.zonedata.lower()) == str(searchzone) and int(h.numberdata) == int(numberdata):
                    return True
                h = h.next
            return False
        else :
            while h is not None :
                if str(h.data.lower()) == str(searchname) and str(h.zonedata.lower()) == str(searchzone) :
                    return True
                h = h.next
            return False
            
    def SeasrchDataTransposition (self,Cname) :
        if self.head is None:
            return False
        else:
            h = self.head
            searchname = Cname.lower()
            count = 0
            while h is not None:
                if str(h.data.lower()) == str(searchname):
                    if count == self.size - 1 :
                        print(count)
                        h.data, h.zonedata, h.numberdata, h.prev.data, h.prev.zonedata, h.prev.numberdata = h.prev.data, h.prev.zonedata, h.prev.numberdata, h.data, h.zonedata, h.numberdata
                        return h.prev.data, h.prev.zonedata, h.prev.numberdata
                    if str(h.data) == str(self.head.data):
                        return h.data, h.zonedata, h.numberdata
                    else:
                        h.data, h.zonedata, h.numberdata, h.prev.data, h.prev.zonedata, h.prev.numberdata = h.prev.data, h.prev.zonedata, h.prev.numberdata, h.data, h.zonedata, h.numberdata
                        return h.prev.data, h.prev.zonedata, h.prev.numberdata
                else:
                    count += 1
                    h = h.next

            else:
                return False

class PaymentDoublyLinkedlist(ClientDoublyLinkedList):
    def __init__(self):
        super().__init__()
    def appendLast(self, namedata, zonedata, numberdata,timedata):
        B = PaymentNode(namedata, zonedata, numberdata,timedata)
        if self.size == 0:
            self.head = B
        else:
            B.prev = self.tail
            self.tail.next = B

        self.tail = B
        self.dummyLast.prev = self.tail
        self.size += 1

    def appendFirst(self, namedata, zonedata, numberdata,timedata):
        B = PaymentNode(namedata, zonedata, numberdata,timedata)
        if self.size == 0:
            self.tail = B
        else:
            h = self.head
            self.head.prev = B
            B.next = self.head

        self.head = B
        self.dummy.next = self.head
        self.size += 1

    def printNormal(self):

        if self.head is None :
            return ""
        h = self.head

        text = ""
        if h.numberdata is None :
            while h.next is not None:
                text += str(h.timedata)+" "+ str(h.data) + " " + str(h.zonedata) + "\n"
                h = h.next
            text += str(h.timedata)+" "+str(h.data) + " " + str(h.zonedata)
        else :
            while h.next is not None:
                text += str(h.timedata)+" "+ str(h.data) + " " + str(h.zonedata) + " " + str(h.numberdata) + "\n"
                h = h.next
            text += str(h.timedata)+" "+str(h.data) + " " + str(h.zonedata) + " " + str(h.numberdata)
        print(text)

class concert():
    # sit zone
    def __init__(self):
        self.sitA = ClientDoublyLinkedList()
        self.sitB = ClientDoublyLinkedList()
        self.sitC = ClientDoublyLinkedList()
        self.standA = ClientDoublyLinkedList()
        self.standB = ClientDoublyLinkedList()
        self.standC = ClientDoublyLinkedList()

        self.ConSize = 0

        # normal search

    def SelectFindSameChair(self,zonedata, numberdata):
        if zonedata == "A":
            result = self.sitA.findsameChair(numberdata)
        elif zonedata == "B":
            result = self.sitB.findsameChair(numberdata)
        elif zonedata == "C":
            result = self.sitC.findsameChair(numberdata)
        return result

    def SelectSearchData(self, namedata,zonedata,numberdata = None ):
        if zonedata == "A":
            result = self.sitA.searchData(namedata,zonedata,numberdata )
        elif zonedata == "B":
            result = self.sitB.searchData(namedata, zonedata, numberdata)
        elif zonedata == "C":
            result = self.sitC.searchData(namedata, zonedata, numberdata)
        elif zonedata == "standA":
            result = self.standA.searchData(namedata, zonedata, numberdata)
        elif zonedata == "standB":
            result = self.standB.searchData(namedata, zonedata, numberdata)
        elif zonedata == "standC":
            result = self.standC.searchData(namedata, zonedata, numberdata)
        return result

    # with server interface
    def SelectSearchDataToFront(self, Cname, zoneData):
        if zoneData == "A":
            result = self.sitA.SearchDataToFront(Cname)
        elif zoneData == "B":
            result = self.sitB.SearchDataToFront(Cname)
        elif zoneData == "C":
            result = self.sitC.SearchDataToFront(Cname)
        elif zoneData == "standA":
            result = self.standA.SearchDataToFront(Cname)
        elif zoneData == "standB":
            result = self.standB.SearchDataToFront(Cname)
        elif zoneData == "standC":
            result = self.standC.SearchDataToFront(Cname)
        return result

    def reciveData(self, namedata, zonedata, numberdata = None  ):
        zonesize = 20

        if numberdata is not None :
            if 0 < int(numberdata) < zonesize + 1 :
                if zonedata == "A":
                    if self.sitA.size < zonesize:
                        if self.sitA.findsameChair(numberdata) == True:
                            print("this chair reserved")
                            return False
                        else:
                            self.ConSize += 1
                            self.sitA.appendLast(namedata, zonedata, numberdata)
                    else:
                        print("full")
                        return False
                if zonedata == "B":
                    if self.sitB.size < zonesize:
                        if self.sitB.findsameChair(numberdata) == True:
                            print("this chair reserved")
                            return False
                        else:
                            self.ConSize += 1
                            self.sitB.appendLast(namedata, zonedata, numberdata)
                    else:
                        print("full")
                        return False
                if zonedata == "C":
                    if self.sitC.size < zonesize:
                        if self.sitC.findsameChair(numberdata) == True:
                            print("this chair reserved")
                            return False
                        else:
                            self.ConSize += 1
                            self.sitC.appendLast(namedata, zonedata, numberdata)
                    else:
                        print("full")
                        return False
            else:
                print(f"chair_number_is_over_{numberdata}ha")

        if numberdata is None :
            if zonedata == "standA":
                if self.standA.size < zonesize:
                    self.ConSize += 1
                    self.standA.enQueue(namedata, zonedata)
                else:
                    print("full")
                    return False
            if zonedata == "standB":
                if self.standB.size < zonesize:
                    self.ConSize += 1
                    self.standB.enQueue(namedata, zonedata)
                else:
                    print("full")
                    return False
            if zonedata == "standC":
                if self.standC.size < zonesize:
                    self.ConSize += 1
                    self.standC.enQueue(namedata, zonedata)
                else:
                    print("full")
                    return False

class Reserved(concert) :
    def __init__(self):
        super().__init__()

    def reciveData(self, namedata, zonedata, numberdata = None ):
        global zonesize
        if numberdata is None :
            if zonedata == "standA":
                if self.standA.size < zonesize:
                    self.standA.appendLast(namedata, zonedata, numberdata)
                else:
                    return False
            if zonedata == "standB":
                if self.standB.size < zonesize:
                    self.standB.appendLast(namedata, zonedata, numberdata)
                else:
                    return False
            if zonedata == "standC":
                if self.standC.size < zonesize:
                    self.standC.appendLast(namedata, zonedata, numberdata)
                else:
                    return False
            self.ConSize += 1
        else:
            if 0 < int(numberdata) < zonesize + 1:
                if zonedata == "A":
                    if self.sitA.size < zonesize:
                        self.sitA.appendLast(namedata, zonedata, numberdata)
                    else:
                        return False
                if zonedata == "B":
                    if self.sitB.size < zonesize:
                        self.sitB.appendLast(namedata, zonedata, numberdata)
                    else:
                        return False
                if zonedata == "C":
                    if self.sitC.size < zonesize:
                        self.sitC.appendLast(namedata, zonedata, numberdata)
                    else:
                        return False
                self.ConSize += 1
            else:
                print(f"Chair_number_over_{zonesize} haha")
                return False

class Payment(concert):
    def __init__(self):
        self.sitA = PaymentDoublyLinkedlist()
        self.sitB = PaymentDoublyLinkedlist()
        self.sitC = PaymentDoublyLinkedlist()
        self.standA = PaymentDoublyLinkedlist()
        self.standB = PaymentDoublyLinkedlist()
        self.standC = PaymentDoublyLinkedlist()

        # queueA_stand
        # queueB_stand
        # queueC_stand

        self.ConSize = 0

    def reciveData(self, namedata, zonedata, numberdata , searchReserve , searchChairClient,timedata):
        global zonesize,isreserve
        isreserve = searchReserve 
        if numberdata is not None and  searchChairClient is not None :
            if searchReserve == True and searchChairClient == False:
                if 0 < int(numberdata) < zonesize + 1:
                    if zonedata == "A":
                        if self.sitA.size < zonesize:
                            if self.sitA.findsameChair(numberdata) == True:
                                print("this chair reserved")
                                return False
                            else:
                                self.sitA.appendLast(namedata, zonedata, numberdata,timedata)
                        else:
                          
                            return False
                    if zonedata == "B":
                        if self.sitB.size < zonesize:
                            if self.sitB.findsameChair(numberdata) == True:
                                print("this chair reserved")
                                return False
                            else:
                                self.sitB.appendLast(namedata, zonedata, numberdata,timedata)
                        else:
                         
                            return False
                    if zonedata == "C":
                        if self.sitC.size < zonesize:
                            if self.sitC.findsameChair(numberdata) == True:
                                print("this chair reserved")
                                return False
                            else:
                                self.sitC.appendLast(namedata, zonedata, numberdata,timedata)
                        else:
                         
                            return False
                else:
                    
                    return False
            else:
                
                if searchReserve == False :
                    print("you did not order this seat!")
                if searchChairClient == True :
                    print("this seat is already taken!")

                return False

        elif numberdata is None and searchChairClient is None :
            if searchReserve == True and searchChairClient is None:
                if zonedata == "standA":
                    if self.standA.size < zonesize:
                        self.standA.appendLast(namedata, zonedata, numberdata,timedata)
                    else:
                        print("full")
                     
                        return False
                if zonedata == "standB":
                    if self.standB.size < zonesize:
                        self.standB.appendLast(namedata, zonedata, numberdata, timedata)
                    else:
                        print("full")
                     
                        return False
                if zonedata == "standC":
                    if self.standC.size < zonesize:
                        self.standC.appendLast(namedata, zonedata, numberdata, timedata)
                    else:
                        print("full")
                   
                        return False

            else:
                if searchReserve == False :
                    print("you did not order this seat!")
                if searchChairClient == True :
                    print("this seat is already taken!")
                return False

        self.ConSize += 1
        return True





def adminGetData(concert):
    print('--------------zone SitA------------------')
    concert.sitA.printNormal()
    print('--------------zone SitB------------------')
    concert.sitB.printNormal()
    print('--------------zone SitC------------------')
    concert.sitC.printNormal()
    print('--------------zone StandA------------------')
    concert.standA.printNormal()
    print('--------------zone StandB------------------')
    concert.standB.printNormal()
    print('--------------zone StandC------------------')
    concert.standC.printNormal()
    print("\n\t\t\t\t\t\t\tamount of clients : ",concert.ConSize)

def adminGetSortedData(concert):
    print('--------------sorted zone SitA------------------')
    concert.sitA.bubblesortList()
    concert.sitA.printNormal()
    print('--------------sorted zone SitB------------------')
    concert.sitB.bubblesortList()
    concert.sitB.printNormal()
    print('--------------sorted zone SitC------------------')
    concert.sitC.bubblesortList()
    concert.sitC.printNormal()
    print('--------------zone StandA------------------')
    concert.standA.bubblesortList()
    concert.standA.printNormal()
    print('--------------zone StandB------------------')
    concert.standB.bubblesortList()
    concert.standB.printNormal()
    print('--------------zone StandC------------------')
    concert.standC.bubblesortList()
    concert.standC.printNormal()
    print("\n\t\t\t\t\t\t\tamount of clients : ",concert.ConSize)

def adminGetSortedDataHtL(concert):
    print('--------------sorted zone SitA------------------')
    concert.sitA.bubblesortListHtL()
    concert.sitA.printNormal()
    print('--------------sorted zone SitB------------------')
    concert.sitB.bubblesortListHtL()
    concert.sitB.printNormal()
    print('--------------sorted zone SitC------------------')
    concert.sitC.bubblesortListHtL()
    concert.sitC.printNormal()
    print('--------------zone StandA------------------')
    concert.standA.bubblesortListHtL()
    concert.standA.printNormal()
    print('--------------zone StandB------------------')
    concert.standB.bubblesortListHtL()
    concert.standB.printNormal()
    print('--------------zone StandC------------------')
    concert.standC.bubblesortListHtL()
    concert.standC.printNormal()
    print("\n\t\t\t\t\t\t\tamount of clients : ",concert.ConSize)

c_F = open("pko_C.pkl","rb")
WhalnDloph = pickle.load(c_F)
c_F.close()

c_P = open("pko_P.pkl","rb")
PaymentQ = pickle.load(c_P)
c_P.close()

c_R = open("pko_R.pkl","rb")
ReserveQ = pickle.load(c_R)
c_R.close()




#                        PAYMENT
# name = "test6666"
# zone = "standA"
# number = None


# if number is not None  : #โซนนั่ง
#     PaymentResult = PaymentQ.reciveData(name,zone,number,ReserveQ.SelectSearchData(name,zone,number),WhalnDloph.SelectFindSameChair(zone,number),timedata)
# else :
#     PaymentResult = PaymentQ.reciveData(name,zone,number,ReserveQ.SelectSearchData(name,zone,number),None,timedata)
# print("Payment :",PaymentResult)

# if PaymentResult == True :
#     WhalnDloph.reciveData(name,zone,number)

# print("PaymentQ")
# DisplayPaymentQ = PaymentQ
# adminGetData(DisplayPaymentQ)






# Create your views here.
def home(request): 
    return render(request,'home.html')

def sitzone(request):  
    return render(request,'sitzone.html',{'WhalnDloph':WhalnDloph})  

def standzone(request): 
    return render(request,'standzone.html',{'WhalnDloph':WhalnDloph}) 

def buy(request):
    return render(request,'buy.html')
    
def payment(request):
    return render(request,'payment.html')

def success(request):
    return render(request,'success.html')

def search(request):
    return render(request,'search.html')



def paymentbill(request):
    if isreserve == False:
        messages.info(request,"Fail")
        return redirect('/payment')
    elif PaymentResult == False:
        messages.info(request,'Seat is already taken')
        return redirect('/payment')
    else :
        return render(request,'paymentbill.html')
        
search_data = 'hi'

@csrf_exempt
def search_user(request):
    
    c_F = open("pko_C.pkl","rb")
    WhalnDloph = pickle.load(c_F)
    c_F.close()

    c_P = open("pko_P.pkl","rb")
    PaymentQ = pickle.load(c_P)
    c_P.close()

    c_R = open("pko_R.pkl","rb")
    ReserveQ = pickle.load(c_R)
    c_R.close()


    full_nameS = None
    zonerS = None

    if request.method == 'POST': 
        full_nameS = request.POST.get('full_name') 
        zonerS = request.POST.get('zone')

    c_F = open("pko_C.pkl","wb")
    pickle.dump(WhalnDloph,c_F)
    c_F.close()

    c_P = open("pko_P.pkl","wb")
    pickle.dump(PaymentQ,c_P)
    c_P.close()

    c_R = open("pko_R.pkl","wb")
    pickle.dump(ReserveQ,c_R)
    c_R.close()

    try : 
        Cop_Whal = WhalnDloph
        h = Cop_Whal.SelectSearchDataToFront(full_nameS,zonerS)
        if h == False : 
            messages.info(request,'wtf')
            return redirect('/search')

        print("fullname zoine ",full_nameS , zonerS)
        print('h',h)
        print(type(h))

        if type(h) == ClientNode : 
            print("is ClientNode")
            full_nameS = None
            zonerS = None   
            return render(request,'searchsuccess.html',{"name":h.data,"zone":h.zonedata,"number":h.numberdata   })
        elif type(h) == dict : 
            print("is dict")
            full_nameS = None
            zonerS = None
            return render(request,'searchsuccess.html',{"name":h['name'],"zone":h['zone'],"number":h['number']})
        elif type(h) == tuple : 
            print("is tuple")
            full_nameS = None
            zonerS = None
            return render(request,'searchsuccess.html',{"name":h[0],"zone":h[1],"number":h[2]})
        else:
            messages.info(request,'wtf')
            return redirect('/search')
    
    except AttributeError : 
        messages.info(request,'wtf')
        return redirect('/search')


def searchsuccess(request):
    return render(request,'searchsuccess.html',)

def contact(request):
    return render(request,'contact.html')


@csrf_exempt
def addreserve(request):
    c_F = open("pko_C.pkl","rb")
    WhalnDloph = pickle.load(c_F)
    c_F.close()

    c_P = open("pko_P.pkl","rb")
    PaymentQ = pickle.load(c_P)
    c_P.close()

    c_R = open("pko_R.pkl","rb")
    ReserveQ = pickle.load(c_R)
    c_R.close()

    if request.method == 'POST': 
        full_name = request.POST.get('full_name') 
        number = request.POST.get('seat') 
        zoner = request.POST.get('zone')


    ReserveQ.reciveData(full_name,zoner,number)
    print(full_name,number,zoner)

    
    c_F = open("pko_C.pkl","wb")
    pickle.dump(WhalnDloph,c_F)
    c_F.close()

    c_P = open("pko_P.pkl","wb")
    pickle.dump(PaymentQ,c_P)
    c_P.close()

    c_R = open("pko_R.pkl","wb")
    pickle.dump(ReserveQ,c_R)
    c_R.close()


    return render(request,'payment.html')

@csrf_exempt
def addpayment(request):
    full_name2 = None
    number2 = None
    zone2 = None
    
    c_F = open("pko_C.pkl","rb")
    WhalnDloph = pickle.load(c_F)
    c_F.close()

    c_P = open("pko_P.pkl","rb")
    PaymentQ = pickle.load(c_P)
    c_P.close()

    c_R = open("pko_R.pkl","rb")
    ReserveQ = pickle.load(c_R)
    c_R.close()
    global PaymentResult
    if request.method == 'POST': 
        full_name2 = request.POST.get('full_name') 
        number2 = request.POST.get('seat') 
        zone2 = request.POST.get('zone') 
    
    if number2 == "":
        number2 = None
    print(full_name2,number2,zone2)

    if number2 is not None  : #โซนนั่ง
        PaymentResult = PaymentQ.reciveData(full_name2,zone2,number2,ReserveQ.SelectSearchData(full_name2,zone2,number2),WhalnDloph.SelectFindSameChair(zone2,number2),timedata)
    else :
        PaymentResult = PaymentQ.reciveData(full_name2,zone2,number2,ReserveQ.SelectSearchData(full_name2,zone2,number2),None,timedata)
    
    if PaymentResult == True :
        print("inside is working !!!!!")
        WhalnDloph.reciveData(full_name2,zone2,number2)
        print("Paymentresult is :",PaymentResult)
        print(WhalnDloph)
        adminGetData(WhalnDloph)

        c_F = open("pko_C.pkl","wb")
        pickle.dump(WhalnDloph,c_F)
        c_F.close()

        c_P = open("pko_P.pkl","wb")
        pickle.dump(PaymentQ,c_P)
        c_P.close()

        c_R = open("pko_R.pkl","wb")
        pickle.dump(ReserveQ,c_R)
        c_R.close()


        full_name2 = None
        number2 = None
        zone2 = None
    
        return render(request,'paymentbill.html')
    else:
        print("inside is44444 working !!!!!")
        c_F = open("pko_C.pkl","wb")
        pickle.dump(WhalnDloph,c_F)
        c_F.close()

        c_P = open("pko_P.pkl","wb")
        pickle.dump(PaymentQ,c_P)
        c_P.close()

        c_R = open("pko_R.pkl","wb")
        pickle.dump(ReserveQ,c_R)
        c_R.close()


        full_name2 = None
        number2 = None
        zone2 = None

        
        return render(request,'payment.html')
    
# reset data
#WhalnDloph = concert()
#ReserveQ = Reserved()
#PaymentQ = Payment()

print("-----ReserveQ----------------------------------------------")
adminGetData(ReserveQ)

print("-----PaymentQ----------------------------------------------")
adminGetData(PaymentQ)    

print("-----WhalnDloph--------------------------------------------")
adminGetData(WhalnDloph)

c_F = open("pko_C.pkl","wb")
pickle.dump(WhalnDloph,c_F)
c_F.close()

c_P = open("pko_P.pkl","wb")
pickle.dump(PaymentQ,c_P)
c_P.close()

c_R = open("pko_R.pkl","wb")
pickle.dump(ReserveQ,c_R)
c_R.close()


Cop_whal = WhalnDloph

# print("-----adminGetSortedData--------------------------------------------")
# adminGetSortedData(WhalnDloph)
# print("-----adminGetSortedDataHtL--------------------------------------------")
# adminGetSortedDataHtL(WhalnDloph)
