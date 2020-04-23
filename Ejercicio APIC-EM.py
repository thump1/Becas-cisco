import requests
import json
import urllib3
from pprint import pprint
from tabulate import *
import os

requests.packages.urllib3.disable_warnings()

def Menu():

    print("""*****************************************
    Menu de opciones (seleccionar con numero)
    *****************************************
    1)Crear nuevo user ticket
    2)Management IPs de los diferentes dispositivos y status
    3)Trabajos Planeados
    4)Version de cada dispositivo
    """)

def Ticket():
    global ticket

    url="https://devnetsbx-netacad-apicem-3.cisco.com/api/v1/ticket"
    headers ={
        'Content-Type': 'application/json'
    } 
    body_json = {
    "password": "Xj3BDqbU",
    "username": "devnetuser"
    }

    response = requests.post(url,json.dumps(body_json), headers=headers, verify=False)

    response_json = response.json()
    ticket = response_json['response']['serviceTicket']


def IPs():
    Ticket()
    url="https://devnetsbx-netacad-apicem-3.cisco.com/api/v1/reachability-info"
    headers ={
        'Content-Type': 'application/json',
        'X-Auth-Token': ticket
    } 


    response = requests.get(url, headers=headers, verify=False)
    response_json = response.json()

    list1 =[]

    counter = 0
    for i in response_json['response']:
        counter+=1        
        b =[
            counter,
            i['id'],
            i['mgmtIp'],
            i['reachabilityStatus']
        ] 
        list1.append(b)
    nombres = ["Numero","ID" "IP de management", "Status"] 
    print(tabulate(list1,nombres))
    input("\n###### Pulsa enter para volver a menu ######")
    Funcion()


def nextjob():
    Ticket()
    url="https://devnetsbx-netacad-apicem-3.cisco.com/api/v1/scheduled-job"
    headers ={
        'Content-Type': 'application/json',
        'X-Auth-Token': ticket
    } 


    response = requests.get(url, headers=headers, verify=False)
    response_json = response.json()

    list2 =[]

    counter = 0
    for i in response_json['response']:
        counter+=1        
        b =[
            counter,
            i['operation'],
            i['startTime'],
            i['prevTime'],
            i['nextTime'],
            i['taskId'],
        ] 
        list2.append(b)
    nombres = ["Numero", "Trabajo","Hora Inicio","Prevision duracion","Siguiente Hora","ID de tarea"] 
    print(tabulate(list2,nombres))
    input("\n###### Pulsa enter para volver a menu ######")
    Funcion()

def Version():
    Ticket()
    url="https://devnetsbx-netacad-apicem-3.cisco.com/api/v1/category"
    headers ={
        'Content-Type': 'application/json',
        'X-Auth-Token': ticket
    } 


    response = requests.get(url, headers=headers, verify=False)
    response_json = response.json()

    list1 =[]

    counter = 0
    for i in response_json['response']:
        counter+=1        
        b =[
            counter,
            i['id'],
            i['name']
        ] 
        list1.append(b)
    nombres = ["Numero","ID", "Nombre"] 
    print(tabulate(list1,nombres))
    input("\n###### Pulsa enter para volver a menu ######")
    Funcion()


def Funcion():
    os.system("clear")
    Menu()
    a = int(input("Seleccione Opcion\n"))
    while(a > 0 and a < 6):
        if (a==1):
            Ticket()
            print("El ticket es:", ticket)
        elif(a==2):
            IPs()
        elif(a==3):
            nextjob()
        elif(a==4):
            Version()
Funcion()

