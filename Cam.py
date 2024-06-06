import paho.mqtt.client as mqtt
import time
import json
import random
# from JSON import A, B, x, y

##########Defining all call back functions###################

def on_connect(client,userdata,flags,rc,pro):# called when the broker responds to our connection request
    if rc==0 :
        print("Connected - rc:",rc)
    else :
        print("Failed to connect, return code %d\n", rc)
# def on_message(client,userdata,message):#Called when a message has been received on a topic that the client has subscirbed to.
#     global FLAG
#     global chat
#     if str(message.topic) != pubtop:
#         msg = str(message.payload.decode("utf-8"))
#         print(str(message.topic),msg)
#         print(message.payload)
#         if msg == "Stop" or msg == "stop":
#             FLAG = False
#         else:
#             # chat = input("Enter Message: ")
#             # client.publish(pubtop,chat)
#             client.publish(pubtop,MSG_JSON)
# def on_subscribe(client, userdata,mid,granted_qos,pro):##Called when the broker responds to a subscribe request.
#     print("Subscribed:", str(mid),str(granted_qos))
# def on_unsubscirbe(client,userdata,mid):# Called when broker responds to an unsubscribe request.
#     print("Unsubscribed:",str(mid))
def on_disconnect(client,userdata,rc):#called when the client disconnects from the broker
    if rc !=0:
        print("Unexpected Disconnection")


broker_address = "mqtt.eclipseprojects.io" #"mqtt.eclipse.org"
port = 1883

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
# client.on_subscribe = on_subscribe
# client.on_unsubscribe = on_unsubscirbe
client.on_connect = on_connect
# client.on_message = on_message
client.connect(broker_address,port)

# time.sleep(1)
# global MSG_JSON
# Send_MSG = {
#             "Alpha": A,
#              "Beta": B,
#              "x": x,
#              "y": y
#            }

pubtop = "/chat/client1"
FLAG = True

# global A, B, x, y
def data():
    A = random.randint(1, 100)
    B = random.randint(1, 100)
    x = random.uniform(0, 1)  # Sử dụng uniform để nhận giá trị ngẫu nhiên với phân phối đều từ 0 đến 1
    y = random.uniform(0, 1)
    return A, B, x, y

def publish(client):
    msg_count = 1
    while True:
        time.sleep(1)
        A, B, x, y = data()
        # Thực hiện gửi các giá trị của Cam đo và tính toán được
        # A = random.randint(1, 100)
        # B = random.randint(1, 100)
        # x = random.uniform(0, 1)  # Sử dụng uniform để nhận giá trị ngẫu nhiên với phân phối đều từ 0 đến 1
        # y = random.uniform(0, 1)
        # data()
        Send_MSG = {
            "Alpha": A,
             "Beta": B,
             "x": x,
             "y": y
           }
        MSG_JSON = json.dumps(Send_MSG)
        msg = f"messages: {msg_count}"
        result = client.publish(pubtop, MSG_JSON)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{pubtop}`")
        else:
            print(f"Failed to send message to topic {pubtop}")
        msg_count += 1
        # if msg_count > 1:
        #     break
# client.loop_start()
# # client.subscribe(subtop)

# time.sleep(1)
# # chat = input("Enter Message: ")

# client.publish(pubtop,MSG_JSON)

# # while True:
# #     if FLAG == False or chat == "Stop" or chat == "stop":
# #         break

# #client.disconnect()
# client.loop_stop()

def run():
    client.loop_start()
    publish(client)
    client.disconnect()
    client.loop_stop()


if __name__ == '__main__':
    run()