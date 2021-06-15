from os import lchown, read
from re import T
import time
from RPi import GPIO
import threading
from helpers.MQTT import Wireless
from helpers.LCD import LCD
from datetime import datetime
from subprocess import check_output, call

from flask_cors import CORS
from flask_socketio import SocketIO, emit, send
from flask import Flask, json, jsonify, request
from repositories.DataRepository import DataRepository

# Getting IP for various setups

ips = LCD.decode(check_output(['hostname', '--all-ip-addresses']))
loc = ips.find(" ")
ip = ips[0:loc]
print(ip)

# Variable for ease of access
# Structure: value, deviceID(SQL), default value on disconnect, B2F message, B2F warning message
devices = [
    [0, 1, 0, 'B2F_MPU_read', 'B2F_MPU_read_e'], 
    [0, 2, 0, 'B2F_temp_read', 'B2F_temp_read_e'], 
    [0, 3, 0, 'B2F_ldr_read', 'B2F_ldr_read_e']
    ] 

# Code for Hardware
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

esp = Wireless(ip)
lcd = LCD()
lcd.setup(ip)


# Code for Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'geheim!'
socketio = SocketIO(app, cors_allowed_origins="*", logger=False,
                    engineio_logger=False, ping_timeout=1)

CORS(app)


@socketio.on_error()        # Handles the default namesp_inace
def error_handler(e):
    print(e)


# ESP thread
thread_esp = threading.Timer(0, esp.setup)
thread_esp.start()


#Main loop function for updating the values. Currently set to 1 second delay for testing and demo purposes
def read_sensors():
    while True:
        print('*** Updating sensor values **')
        global devices
        devices[0][0] = esp.vals["acc"]
        devices[1][0] = esp.vals["temp"]
        devices[2][0] = esp.vals["ldr"]
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for i in devices:
            if i[0] == i[2]:
                DataRepository.write_device(now, i[0], i[1], "Possible disconnect")
                socketio.emit(i[4], {'data': i[0]})
            else:
                DataRepository.write_device(now, i[0], i[1])
                socketio.emit(i[3], {'data': i[0]})
        red = (esp.outvals["actuators/lights"] & 0xff0000) >> 16
        green =  (esp.outvals["actuators/lights"] & 0xff00) >> 8
        blue = (esp.outvals["actuators/lights"] & 0xff)
        socketio.emit('B2F_light_status', {'red' : red, 'green' : green, 'blue' : blue, "percent" : esp.outvals["actuators/intensity"]})
        time.sleep(1)


thread_sensors = threading.Timer(1, read_sensors)
thread_sensors.start()


print("**** Program started ****")

 
@socketio.on('connect')
def initial_connection():
    print('A new client connect')

@socketio.on('F2B_shutdown')
def shutdown_pi():
    print("shutdown initiliased")
    call(" echo 'W8w00rd' | sudo -S sudo shutdown -h now", shell=True)

@socketio.on('F2B_lights')
def lights(data):
    # converting RGB values into a single hex, easier on the esp where speed matters more
    h = (int(data["red"]) << 16) | (int(data["green"]) << 8) | (int(data["blue"]))
    esp.outvals["actuators/lights"] = h
    if esp.outvals["actuators/lights"] == h:
        DataRepository.write_light(h)
    else:
        DataRepository.write_light(h, "Error updating")

@socketio.on('F2B_data')
def request_data(form):
    acc = DataRepository.request_data(1, int(form["amount"]), form['enddate'], form['startdate'])
    temp = DataRepository.request_data(2, int(form["amount"]), form['enddate'], form['startdate'])
    ldr = DataRepository.request_data(3, int(form["amount"]), form['enddate'], form['startdate'])
    res = []
    # Checking every result for the same date. Since this gets normalised in the loop read function, there will be no discrepancies
    # Note: This can be done more efficiently most likely       
    for i in acc:
        for j in temp:
            for k in ldr:
                if (k['date'] == j['date']) and (k['date'] == i['date']):
                    res.append({"date" : k['date'].strftime("%Y-%m-%d %H:%M:%S"), "acc" : i["value"], "temp" : j["value"], "ldr" : k["value"]})
    socketio.emit('B2F_DATA_REQUEST', res) 

@socketio.on('F2B_intensity')
def change_intensity(form):
    intensity = int(form["intensity"])      
    esp.outvals["actuators/intensity"] = intensity
    if esp.outvals["actuators/intensity"] == intensity:
        DataRepository.light_default(intensity, 5)          
    else:
        DataRepository.light_default(intensity, 5, "Error updating")

@socketio.on('F2B_override')
def toggle_override(form):
    override = int(form["override"])
    esp.outvals["actuators/override"] = override
    if esp.outvals["actuators/override"] == override:
        DataRepository.light_default(override, 3)      
    else:
        DataRepository.light_default(override, 3, "Error updating")

@socketio.on('F2B_alarm')
def change_alarm(form):
    alarm = int(form["alarm"])      
    esp.outvals["actuators/sounds"] = alarm
    if esp.outvals["actuators/sounds"] == alarm:
        DataRepository.speaker_default(alarm)        
    else:
        DataRepository.speaker_default(alarm, "Error updating")
       
if __name__ == '__main__':
    socketio.run(app, debug=False, host='0.0.0.0')
