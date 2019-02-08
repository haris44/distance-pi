import RPi.GPIO as GPIO
import time
import datetime
import requests
import json
import pytz

local_tz = pytz.timezone('Europe/Paris')

GPIO.setmode(GPIO.BCM)
GPIO.setmode(GPIO.BCM)


Trig = 23          # Entree Trig du HC-SR04 branchee au GPIO 23
Echo = 24         # Sortie Echo du HC-SR04 branchee au GPIO 24

GPIO.setup(Trig,GPIO.OUT)
GPIO.setup(Echo,GPIO.IN)

GPIO.output(Trig, False)

def utc_to_local(utc_dt):
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_tz.normalize(local_dt)

def aslocaltimestr(utc_dt):
    return utc_to_local(utc_dt).strftime('%Y-%m-%d %H:%M:%S')


# repet = input("Entrez un nombre de repetitions de mesure : ")

while True:    # On prend la mesure "repet" fois

   time.sleep(10)       # On la prend toute les 1 seconde

   GPIO.output(Trig, True)
   time.sleep(0.00001)
   GPIO.output(Trig, False)

   while GPIO.input(Echo)==0:  ## Emission de l'ultrason
     debutImpulsion = time.time()

   while GPIO.input(Echo)==1:   ## Retour de l'Echo
     finImpulsion = time.time()

   distance = round((finImpulsion - debutImpulsion) * 340 * 100 / 2, 1)  ## Vitesse du son = 340 m/s


   url = 'http://51.158.78.254:8080/measurements/'
   payload = {'value': distance, 'room': 100, 'captorName': 'distance',
              'date': aslocaltimestr(datetime.datetime.now())}
   headers = {'content-type': 'application/json'}
   response = requests.post(url, data=json.dumps({'measurement': payload}), headers=headers)
   print(json.dumps({'measurment': payload}))
   print(response)



GPIO.cleanup()