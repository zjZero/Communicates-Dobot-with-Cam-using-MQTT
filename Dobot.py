import paho.mqtt.client as mqtt
import time
import json
from Dobot_Magician import find_point_c, device, toa_do, setup_robot, PORT, Move_to_E
##########Defining all call back functions###################


# printed_once = False
def on_connect(client,userdata,flags,rc,pro):# called when the broker responds to our connection request
    print("Connected - rc:",rc)
def on_message(client,userdata,message):#Called when a message has been received on a topic that the client has subscirbed to.
    global msg
    
    if str(message.topic) == subtop:
        # msg = str(message.payload.decode("utf-8"))
        msg = json.loads(message.payload)
        print(str(message.topic),msg)
        A = msg['Alpha']
        B = msg['Beta']
        x = msg['x']
        y = msg['y']

        if x == 1:
            print('Góc Alpha:', A)
            print('Góc Beta :', B)
            print('Tọa độ x :', x)
            find_point_c(A, B)
            Move_to_E(device)
            time.sleep(2)
            x = 0;      
            client.publish(pubtop,x)    
        
        else:
            chat = " Gửi lại thông số tọa độ"
            client.publish(pubtop,chat)
        # print('Góc Alpha:', A)
        # print('Góc Beta :', B)
        # print('Tọa độ x :', x)
        # print('Tọa độ y :', y)
        # print('\n')
        
        # else:
        #     chat = "        Đã thực hiện xong"
        #     client.publish(pubtop,chat)
        
def on_subscribe(client, userdata,mid,granted_qos,pro):##Called when the broker responds to a subscribe request.
    print("Subscribed:", str(mid),str(granted_qos))
def on_unsubscirbe(client,userdata,mid):# Called when broker responds to an unsubscribe request.
    print("Unsubscribed:",str(mid))
def on_disconnect(client,userdata,rc):#called when the client disconnects from the broker
    if rc !=0:
        print("Unexpected Disconnection")


broker_address = "mqtt.eclipseprojects.io" #"mqtt.eclipse.org"
port = 1883

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_subscribe = on_subscribe
client.on_unsubscribe = on_unsubscirbe
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_address,port)

time.sleep(1)

pubtop = "/TEST/DOBOT"
subtop = "/TEST/CAM"
FLAG = True
chat = None
msg = None
def run():
    # global msg, A, B, x, y
    client.loop_start()
    # Data() 
    client.subscribe(subtop)
    time.sleep(1)
    while True: 
        if FLAG == False:
            break
    client.disconnect()
    client.loop_stop()
    return A, B
if __name__ == '__main__':
    device = setup_robot(PORT)
    toa_do()
    for i in range(1, 5):  # Sử dụng range để tạo vòng lặp từ 1 đến 4
        print(f'toa do diem {i}x:{x[i]}, y:{y[i]}, z:{z[i]}')
    run()
    