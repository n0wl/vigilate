# vigilate_api_poc.py v0.2
# 
# This file is just proof of concept for the Vigilate Cameras API
# Copyright (c) 2024 Dorian Schneltzer <ds@allnet.de>, ALLNET GmbH Computersysteme 
# 
# This program is free software: you can redistribute it and/or modify  
# it under the terms of the GNU General Public License as published by  
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License 
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#


import requests
from requests.exceptions import HTTPError
from prettytable import PrettyTable
import json
from datetime import datetime

#configure here your IP, username and password for your Vigilate Camera
# default IP 10.0.177.178 or 10.0.37.37
#
url = 'http://10.0.177.178/'
username = 'admin'
password = 'admin'
verbose = '0';



myList = [22,4,16,38,13] #myList already has 5 elements

def api_authenticate(verbose):
    data = {'jsonrpc': "2.0" ,'id': 4, 'params': { 'username': username,'password': password }}
    headers = {'Content-type': 'application/json'}
    response = requests.post(url+'api/authenticate', data=json.dumps(data), headers=headers)
    jsonResponse = response.json()
    token = jsonResponse["result"]["Data"]["token"]
    if verbose == 5:
        print("\nDEBUG Level is: " +str(verbose) +"\nEntire JSON response:")
        print(response.text)
        
    return token

def api_getLastTransit(token,verbose):
    headers = {'Authorization': 'Basic '+token}
    response = requests.get(url+'api/getLastTransit', headers=headers)
    jsonResponse = response.json()
    json_direction=jsonResponse["result"]["Data"]["Direction"]
    tsUTC = float(jsonResponse["result"]["Data"]["TsUTC"])/1000000 #division by 1000000 because microseconds
    time = datetime.fromtimestamp(tsUTC) 

    if json_direction == 1:
        direction = "out"
    else: 
        direction = "in"


    print("\nNew car detected on " +str(time)+ " from: " + jsonResponse["result"]["Data"]["PlateNation"] + " Plate Number is: "+ jsonResponse["result"]["Data"]["PlateValue"]+ " Car direction is: "+direction)

    if verbose == 5:
        print("\nDEBUG Level is: " +str(verbose) +"\nEntire JSON response:")
        print(response.text)


def api_getLastNTransits(token,verbose):
    headers = {'Authorization': 'Basic '+token}
    response = requests.get(url+'api/getLastNTransits', headers=headers)
    jsonResponse = response.json()
    table = PrettyTable(['ID','Time','Country', 'Plate','Direction'])
    for key, value in jsonResponse["result"]["Data"].items():
        if key == 'Values':
            for item in value:
                json_direction=item["Direction"]
                tsUTC = float(item["TsUTC"]/1000000) #division by 1000000 because microseconds
                time = datetime.fromtimestamp(tsUTC) 
  
                if json_direction == 1:
                    direction = "out"
                else: 
                    direction = "in"

                table.add_row([item["ID"],time,item["PlateNation"],item["PlateValue"],direction])
    print("\nLast 5 car transitions detected:")        
    print(table)       

    if verbose == 5:
        print("\nDEBUG Level is: " +str(verbose) +"\nEntire JSON response:")
        print(response.text)



choice = 0
while True:
 print("\nSimple POC for Vigilate API v0.2")
 print("\nSelect operation:")
 print(" 1. Authenticate to the API and show the JSON response")
 print(" 2. Show the last transit - plain simplified output")
 print(" 3. Show the last transit - JSON output")
 print(" 4. Show the last 5 transits - plain simplified output")
 print(" 5. Show the last 5 transits - JSON output")
 print(" 9. Exit")
 choice = int(input("ENTER YOUR CHOICE (1-9): "))
 #authenticate with verbose output verbose=5
 if choice == 1: 
    api_authenticate(5)
 #show last transit with formatted simple output
 elif choice == 2: 
  token = api_authenticate(0) 
  api_getLastTransit(token,0)
    
 #show the entire JSON response for getLastTransit
 elif choice == 3:
  token = api_authenticate(0)
  api_getLastTransit(token,5)

  #show last 5 transits with formatted simple output
 elif choice == 4: 
  token = api_authenticate(0)  
  api_getLastNTransits(token,0)

  #show the entire JSON response for getLastNTransits
 elif choice == 5: 
  token = api_authenticate(0)
  api_getLastNTransits(token,5)


 #exit from the menu
 elif choice == 9: 
  break
 else:
  print("Choice is not valid")
  print("\n\nPress any key to continue..............")
  ch = input()

