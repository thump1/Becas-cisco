from ncclient import manager
from tabulate import *
import xmltodict
import json
import requests
from netmiko import ConnectHandler
import os

requests.packages.urllib3.disable_warnings()

def Menu():

    print("""*****************************************
    Menu de opciones (seleccionar con numero)
    *****************************************
    1)Tabla de Interfaz, IP y MAC
    2)Crear Interfaces
    3)Borrar Interfaces
    4)Tabla routing
    """)

def Filtros():
   m = manager.connect(
         host="10.10.20.48",
         port=830,
         username="cisco",
         password="cisco_1234!",
         hostkey_verify=False
         )
   netconf_filter2 = """
   <filter>
      <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
         <interface>
            <enabled/>
            <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip">
               <address>
                  <ip/>
               </address>
            </ipv4>
         </interface>
      </interfaces>  
   </filter>
   """
   global netconf_reply_dict2
   netconf_reply2 = m.get(filter = netconf_filter2)
   netconf_reply_dict2 = xmltodict.parse(netconf_reply2.xml)

   netconf_filter = """
   <filter>
      <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces"/>
   </filter>
   """
   global netconf_reply_dict
   netconf_reply = m.get(filter = netconf_filter)
   netconf_reply_dict = xmltodict.parse(netconf_reply.xml)

def IP():
   global ip

   if(netconf_reply_dict2["rpc-reply"]["data"]["interfaces"]["interface"][i]["enabled"] == "false"):
      ip = "None"
   else:
      ip = netconf_reply_dict2["rpc-reply"]["data"]["interfaces"]["interface"][i]["ipv4"]["address"]["ip"]


def Interfaz():
   Filtros()
   name_list = [] 
   name = []
   global i
   i = 0
   counter1 = 0
   counter2 = 1

   for interface in netconf_reply_dict["rpc-reply"]["data"]["interfaces-state"]["interface"]:
      interface["name"]
      counter1+=1
   for interface in netconf_reply_dict["rpc-reply"]["data"]["interfaces-state"]["interface"]:
      if (counter2<counter1):
         counter2 +=1
         IP()
         name = [
            interface["name"],
            ip,
            interface["phys-address"]
            ]
         i+=1
         name_list.append(name)
      else:
         None
   table_header =[ 'Interfaz',
                'IP',
                'MAC',
                ]
   print(tabulate(name_list,table_header))
   input("\n###### Pulsa enter para volver a menu ######")
   Funcion()

def NuevaInterfaz():

   numero_interfaz = int(input("Introduce el numero de la interfaz de 1 a 100 (Tan solo se pueden crear interfaces virtuales): "))
   nombre_interfaz = "Loopback" + str(numero_interfaz)
   descripcion_interfaz = input("Introduce descripcion de la interfaz: ")
   IP_interfaz = input("Introduce IP de la interfaz: ")
   mascara_interfaz = input("Introduce mascara de la interfaz: ")

   api_url = "https://10.10.20.48/restconf/data/ietf-interfaces:interfaces/interface=" + nombre_interfaz

   headers = { "Accept": "application/yang-data+json", 
               "Content-type":"application/yang-data+json"
            }

   basicauth = ("cisco", "cisco_1234!")

   yangConfig = {
      "ietf-interfaces:interface": {
         "name": nombre_interfaz,
         "description": descripcion_interfaz,
         "type": "iana-if-type:softwareLoopback",
         "enabled": True,
         "ietf-ip:ipv4": {
               "address": [
                  {
                     "ip": IP_interfaz,
                     "netmask": mascara_interfaz
                  }
               ]
         },
         "ietf-ip:ipv6": {}
      }
   }


   resp = requests.put(api_url, data=json.dumps(yangConfig), auth=basicauth, headers=headers, verify=False)
   if(resp.status_code >= 200 and resp.status_code <= 299):
      print("STATUS OK: {}".format(resp.status_code))
      print("\nInterfaz creada correctamente")
   else:
      print("Error code {}, reply: {}".format(resp.status_code, resp.json()))
      print("\nInterfaz no creada")

   input("\n###### Pulsa enter para volver a menu ######")
   Funcion()

def BorrarInterfaz():
   Filtros()
   input("###### Pulsa enter para ver la lista de interfaces ######")
   nombres_list = []
   counter1 = 0
   for interface in netconf_reply_dict["rpc-reply"]["data"]["interfaces-state"]["interface"]:
      nombre = [
         counter1,
         interface["name"]
      ]
      counter1+=1
      nombres_list.append(nombre)
   header_2 = ["Numero","Nombre interfaz"]
   print(tabulate(nombres_list,header_2))

   numero_interfaz = int(input("Introduce el numero que va despues de la interfaz (solo se pueden borrar interfaces de Loopback): "))
   sshCli = ConnectHandler(
      device_type='cisco_ios',
      host = '10.10.20.48',
      port = 22,
      username = 'cisco',
      password = 'cisco_1234!'
   )
   command = 'no interface Loopback' + str(numero_interfaz)
   config_commands = [
      command
   ]
   output = sshCli.send_config_set(config_commands)
   output = sshCli.send_command("show ip int brief")
   print("IP interface status and conf:\n{}\n".format(output))
   input("\n###### Pulsa enter para volver a menu ######")
   Funcion()

def FiltroRouting():
   m = manager.connect(
         host="10.10.20.48",
         port=830,
         username="cisco",
         password="cisco_1234!",
         hostkey_verify=False
         )

   routing_filter = """
   <filter>
      <routing xmlns="urn:ietf:params:xml:ns:yang:ietf-routing">
         <routing-instance>
            <routing-protocols>
               <routing-protocol>
                  <static-routes>
                     <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ipv4-unicast-routing"/>
                  </static-routes>
               </routing-protocol>
            </routing-protocols>
         </routing-instance>
      </routing>
   </filter>
   """ 
   global routing_reply_dict
   routing_reply = m.get(filter = routing_filter)
   routing_reply_dict = xmltodict.parse(routing_reply.xml)


def Route():

   global hop
   if(counter3 == 0):
      hop = routing_reply_dict["rpc-reply"]["data"]["routing"]["routing-instance"]["routing-protocols"]["routing-protocol"]["static-routes"]["ipv4"]["route"][counter3]["next-hop"]["next-hop-address"]
   else:
      hop = routing_reply_dict["rpc-reply"]["data"]["routing"]["routing-instance"]["routing-protocols"]["routing-protocol"]["static-routes"]["ipv4"]["route"][counter3]["next-hop"]["outgoing-interface"] 


def Routing():
   FiltroRouting()
   routing_list = []
   global counter3
   counter3 = 0
   table_header =[ 'Identificador',
                'Red de destino',
                'Interfaz de salida'
                ]
   for route in routing_reply_dict["rpc-reply"]["data"]["routing"]["routing-instance"]["routing-protocols"]["routing-protocol"]["static-routes"]["ipv4"]["route"]:
      Route()
      route2 = [
               counter3,
               route["destination-prefix"],
               hop
      ]
      counter3+=1
      routing_list.append(route2)
   print(tabulate(routing_list,table_header))
   input("\n###### Pulsa enter para volver a menu ######")
   Funcion()
   

def Funcion():
    os.system("clear")
    Menu()
    a = int(input("Seleccione Opcion\n"))
    while(a > 0 and a < 6):
         if (a==1):
            Interfaz()
            a = int(input("Seleccione Opcion\n"))
         elif (a==2):
            NuevaInterfaz()
            a = int(input("Seleccione Opcion\n"))            
         elif (a==3):
            BorrarInterfaz()
            a = int(input("Seleccione Opcion\n"))
         elif(a==4):
            Routing()            
Funcion()