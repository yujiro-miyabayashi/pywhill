import time
from whill import ComWHILL
from pythonosc.udp_client import SimpleUDPClient

COM_PORT = 'COM3'
OSC_SERVER = '127.0.0.1'
OSC_PORT = 12345

whill = ComWHILL(port=COM_PORT)
client = SimpleUDPClient(OSC_SERVER, OSC_PORT)

def callback0():
    global whill 
    whill.start_data_stream(20, 1, 5)

def callback1():
    global whill 
    whill.start_data_stream(20, 0, 5)

def main():

    # power on
    whill.send_power_on()

    # wait 3sec
    _wait = 0
    while True:
       
        # disable joystick
        whill.send_joystick(front=0, side=0) 
        whill.refresh()

        time.sleep(0.1)
        _wait+=1
        if _wait >= 30:
            break

    # safe mode
    whill.set_safe_mode(True)

    whill.register_callback('data_set_0', callback0)
    whill.register_callback('data_set_1', callback1)
    whill.start_data_stream(20, 1, 5)


    while True:
       
        # disable joystick
        # whill.send_joystick(front=0, side=0) 
        whill.refresh()
        time.sleep(0.05)

        level, current = whill.battery.values()
        print('joystick: {fb} {lr} gear:{gear} Battery: {level}%, {current}mA'.format(
            fb=whill.joy["front"], 
            lr=whill.joy["side"], 
            gear = whill.speed_mode_indicator+1,
            level=level, current=current))
        
        # send osc data
        _fb = whill.joy["front"]
        _lr = whill.joy["side"]
        _gear = whill.speed_mode_indicator+1
        client.send_message("/whill/data", [_fb, _lr, _gear])


if __name__ == "__main__":
    main()