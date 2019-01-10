import time
import network
import usocket as socket
from machine import Pin, PWM, reset
import os

# Access point, allows other WiFi clients to connect
ap = network.WLAN(network.AP_IF)

# Set WiFi access point name (formally known as ESSID) and WiFi channel
ap.config(essid='esp12', authmode=network.AUTH_WPA_WPA2_PSK,
          password='esppornxx', channel=11)

# Query params one by one
print(ap.config('essid'))
print(ap.config('channel'))

print(ap.ifconfig())

#addr = socket.getaddrinfo('micropython.org', 80)[0][-1]
HOST = '0.0.0.0'
PORT = 5555
data = None
loop = False
ex = True

p5 = Pin(5, Pin.IN, Pin.PULL_UP)

def clearPWM(pin):
    pwm = PWM(pin)
    pwm.freq(500)
    pwm.duty(1023)
    
    return pwm

def savetofile():
    global data
    print('open file')
    f = open('remote.py', 'bw')
    print('write to file')
    f.write(data)
    f.close()

def callback(p):
    p5.irq(trigger=Pin.IRQ_FALLING, handler=lambda x:print('wait, wait!'))
    global loop
    global ex
    
    time.sleep_ms(45)
    
    if p5.value() == 1:
        return
    else:
        try:
            socket_loop()
        except Exception as ex:
            #raise ex
            print(ex)
            p5.irq(trigger=Pin.IRQ_FALLING, handler=callback)

def clearAll():
    r = Pin(14, Pin.OUT)
    g = Pin(12, Pin.OUT)
    b = Pin(13, Pin.OUT)
    
    for pin in (r, g, b):
        clearPWM(pin)
    


def recvok():
    clearAll()

    # programmed OK blink blue
    delay = 0.2
    
    b = Pin(14, Pin.OUT)
    blue = clearPWM(b)
    for n in range(5):
        blue.duty(1023)
        time.sleep(delay)
        blue.duty(10)
        time.sleep(delay)
    blue.duty(1023)
    
def socket_loop():
    global data
    global loop

    clearAll()
    # red light self programming mode
    r = Pin(13, Pin.OUT)
    rpwm = clearPWM(r)
    rpwm.freq(500)
    rpwm.duty(1000)
    
    print('==========')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #socket.settimeout(10)
    sock.bind((HOST, PORT))
    sock.listen(1)
    print('socket listen')
    conn, addr = sock.accept()
    print('Connecte to: ', addr)
    temp_data = b''
    while True:
        print('listenning', addr)
        recv = conn.recv(2048)
        #if not recv:
        #    break
            #data = recv
            #savetofile()
        print(recv)
        
        temp_data += recv
        if temp_data[-9:] == b'<!>remote':
            break
        
    if temp_data[:8] == b'#!remote':
        #data = temp_data
        print(temp_data)
        f = open('remote.py', 'bw')
        print('write to file')
        f.write(temp_data)
        f.close()
        #receive blink
        recvok()
        #loop = False
        #exec(recv)
    
    conn.sendall('Thank you!')
    conn.close()
    # Soft reset 
    reset()


def main():
    global data
    
    while True:
        if data:
            try:
                print('> Execit')
                exec(data)
                time.sleep(2)
            except Exception as ex:
                #raise ex
                print(ex)
                data = None
                
                # error blink
                for n in range(5):
                    rpwm.duty(1023)
                    time.sleep(1)
                    rpwm.duty(10)
                    time.sleep(1)
                    rpwm.duty(900)
        else:
            print('empty loop')
            time.sleep(1)

p5.irq(trigger=Pin.IRQ_FALLING, handler=callback)


if 'remote.py' in os.listdir():
    try:
        from remote import *
    except Exception as ex:
        print(ex)
        main()

main()

