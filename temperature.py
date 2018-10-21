#!/usr/bin/env python
"""Read temperature sensor and send data to server.

"""

import pandas as pd
import serial
import time
import urllib.request

arduino = serial.Serial("/dev/ttyMCC", 9600)

def get_key():
    """Get device key
    """
    with open("chiave/key.txt", "r") as k:
        return k.read()[:-1]

def get_temp():
    """Read sensor value
    """
    tempe = arduino.readline()
    tempe = tempe.decode("ascii")
    return float(tempe[:-2])

def send_data(key, tempe):
    """Send data to server:
        https://www.airhive.it/api/newHFH.php?key=CHIAVE&temp=TEMPERATURA&airq=INDICE_ARIA
    """
    print("Dati: ")
    with urllib.request.urlopen("https://www.airhive.it/api/newHFH.php?key="+key+"&temp="+str(tempe)) as res:
        print(res.read())

def emergency(key, df):
    """Send emergency if value is out of std dev
    """
    if (df.iloc[-1] > df.mean() + df.std()):
        send_log(key, "EMERGENZA!!!!!!!")

def send_log(key, messaggio):
    with urllib.request.urlopen("https://www.airhive.it/api/newLog.php?key="+key+"&log="+messaggio) as res:
        print("Log: ")
        print(res.read())

def main():
    df = pd.DataFrame(columns = ["tempe"])
    key = get_key()
    count = 0
    cic = 0
    while(True):
        try:
            df = df.append(pd.DataFrame([get_temp()], columns = ["tempe"]), ignore_index = True)
            count += 1
            emergency(key, df.tempe)
            if count == 9:
                send_data(key, df.tempe.iloc[-10:].mean())
                count = 0
                cic += 1
            if cic == 60:
                df = df.iloc[-300:]
                cic = 0
            time.sleep(1)
        except Exception as e:
            print(str(e))
            send_log(key, str(e))
            time.sleep(1)


if __name__ == "__main__":
    main()
