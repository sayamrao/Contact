# -*- coding: utf-8 -*-
"""
Created on Sat Apr  3 14:04:46 2021

@author: Sayam
"""

import requests

BASE = "http://127.0.0.1:5000/"

data = [{"username": "sayamzafar", "firstname": "Sayam", "lastname": "Zafar"},
        {"username": "rohanzafar", "firstname": "Rohan", "lastname": "Zafar"},
        {"username": "raozafar", "firstname": "Rao", "lastname": "Zafar"}]

data1 = [{"username": "sayamzafar", "firstname": "Sayam", "lastname": "Zafar"}]

data2 = [{"subject": "a", "message": "abc", "contact_id": 1}]

print("Entering Data: ")
response = requests.put(BASE + "contact/" + "1", data1[0])
print("Response: ",response.json())

print("Entering Email: ")
response = requests.put(BASE + "email/" + "1", data2[0])
print("Response: ",response.json())



print("Press Enter to get contact by username")
input()
response = requests.get(BASE + "contact/sayamzafar")
print("Response: ",response.json())


print("Press Enter to get Email by contact_id")
input()
response = requests.get(BASE + "email/1")
print("Response: ",response.json())

print("Press Enter to get all contacts ")
input()
response = requests.get(BASE + "contacts")
print("Response: ",response.json())

print("Press Enter to update a contact ")
response = requests.patch(BASE + "contact/1", {"lastname": "Rao"})
print("Response: ",response.json())

print("Press Enter to get all contacts ")
input()
response = requests.get(BASE + "contacts")
print("Response: ",response.json())


print("Deleting Data: ")
response = requests.delete(BASE + "contact/1")


print("Press Enter to get all contacts after deleting ")
input()
response = requests.get(BASE + "contacts")
print("Response: ",response.json())