import numpy as np
import math
import time
import cv2

import paho.mqtt.client as mqtt
import json


broker_address = "mqtt.eclipseprojects.io"  # "mqtt.eclipse.org"
port = 1883
pubtop = "/MQTT/CAM"
subtop = "/MQTT/DOBOT"
##########Defining all call back functions###################

def on_connect(client,userdata,flags,rc,pro):   # called when the broker responds to our connection request
    if rc==0 :
        print("Connected - rc:",rc)
    else :
        print("Failed to connect, return code %d\n", rc)

def on_message(client,userdata,message):#Called when a message has been received on a topic that the client has subscirbed to.
    global msg_count
    global msg

    if str(message.topic) == subtop:
        msg = int(message.payload.decode("utf-8"))
        # print(str(message.topic),msg)

        if msg == 0:
            print("\nDoBot! Done it job!\n")
def on_subscribe(client, userdata,mid,granted_qos,pro):##Called when the broker responds to a subscribe request.
    print("Subscribed:", str(mid),str(granted_qos))
def on_unsubscirbe(client,userdata,mid):# Called when broker responds to an unsubscribe request.
    print("Unsubscribed:",str(mid))
def on_disconnect(client,userdata,rc):  # called when the client disconnects from the broker
    if rc !=0:
        print("Unexpected Disconnection")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_subscribe = on_subscribe
client.on_unsubscribe = on_unsubscirbe
client.on_message = on_message

def publish(client):
    global msg_count
    global Send_MSG
    time.sleep(1)
    # Send_MSG = {
    #     "Alpha": A,
    #      "Beta": B,
    #      "x": 1,
    #    }
    MSG_JSON = json.dumps(Send_MSG)
    num_msg = f"messages: {msg_count}"
        
    result = client.publish(pubtop, MSG_JSON)
    # result: [0, 1]
    status = result[0]
    
    if status == 0:
        print(f"\nSend `{num_msg}` to topic `{pubtop}`")
        print(f"Góc EDC: {angle_EDC:.2f} độ")
        print(f"Góc ECD: {angle_ECD:.2f} độ")
    else:
        print(f"Failed to send message to topic {pubtop}")

    msg_count += 1


def distance(point1, point2):
    return math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)


cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 500)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 500)

for i in range(10):
    _, frame = cap.read()
cap = cv2.VideoCapture(1)

image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
image = cv2.GaussianBlur(image, (25, 25), 0)
last_frame = image
cap.set(3, 1000)
cap.set(4, 800)

Not_printed = 1
msg_count = 1
msg = 0

client.connect(broker_address,port)
client.loop_start()
client.subscribe(subtop)
time.sleep(1)

while True:
    _, frame = cap.read()
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    image = cv2.GaussianBlur(image, (25, 25), 0)
    last_frame = image
    _, thresholded = cv2.threshold(image, 120, 255, cv2.THRESH_BINARY_INV)
    contours, hierarchy = cv2.findContours(thresholded, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)

    if len(sorted_contours) < 1:
        continue

    # Tìm contour lớn nhất (viền đen của hình vuông)
    largest_contour = sorted_contours[0]

    # Tìm hình vuông ABCD trong viền đen
    rect = cv2.minAreaRect(largest_contour)
    box = cv2.boxPoints(rect).astype('int')
    cv2.drawContours(frame, [box], 0, (0, 255, 0), 2)

    sorted_box = sorted(box, key=lambda point: math.sqrt(point[0]**2 + point[1]**2))
    point_names = ['D', 'C', 'A', 'B']

    for i, point in enumerate(sorted_box):
        point_name = point_names[i]
        x, y = point
        cv2.putText(frame, f"{point_name}: ({x}, {y})", (x + 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    D = tuple(sorted_box[0])
    C = tuple(sorted_box[1])

    # Tìm điểm E gần D nhất
    min_distance = float('inf')
    closest_E = None

    for contour in sorted_contours[1:]:
        area = cv2.contourArea(contour)
        if area < cv2.contourArea(largest_contour) / 2:  # Chỉ xem xét contour nhỏ hơn 1 nửa của hình vuông
            M = cv2.moments(contour)
            if M['m00'] != 0:
                cX = int(M['m10'] / M['m00'])
                cY = int(M['m01'] / M['m00'])
                E = (cX, cY)
                dist = distance(D, E)
                pts_image = np.array(box, dtype="float32")
                if dist < min_distance and cv2.pointPolygonTest(pts_image, E, False) >= 0:  # Kiểm tra nếu E nằm trong hình vuông ABCD
                    min_distance = dist
                    closest_E = E

    if closest_E is not None:
        cv2.circle(frame, closest_E, 3, (0, 255, 0), -1)
        cv2.putText(frame, f"E: {closest_E}", closest_E, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        DC = distance(D, C)
        DE = distance(D, closest_E)
        EC = distance(closest_E, C)

        cos_EDC = (DC**2 + DE**2 - EC**2) / (2 * DC * DE)
        cos_ECD = (DC**2 + EC**2 - DE**2) / (2 * DC * EC)

        angle_EDC = math.degrees(math.acos(cos_EDC))
        angle_ECD = math.degrees(math.acos(cos_ECD))

        # print(f"Góc EDC: {angle_EDC:.2f} độ")
        # print(f"Góc ECD: {angle_ECD:.2f} độ")

        cv2.line(frame, D, closest_E, (220, 0, 250), 2)
        cv2.line(frame, C, closest_E, (220, 0, 250), 2)

        cv2.putText(frame, f"EDC: {angle_EDC:.1f}", (D[0] - 90, D[1] + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(frame, f"ECD: {angle_ECD:.1f}", (C[0] - 90, C[1] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        A = angle_EDC
        B = angle_ECD

        Send_MSG = {
                    "Alpha": A,
                    "Beta": B,
                    "x": 1,
                    }
    cv2.imshow('FRAME', frame)
    
    if msg == 0 and closest_E is not None:
        publish(client)
        msg = 1
        Not_printed = 1
    
    if Not_printed == 1 and closest_E is None and msg == 0:
        print("\nHãy cho vật thể vào đi nào 😳\n")
        Not_printed = 0

    k = cv2.waitKey(100)
    if k == 27:
        break

client.disconnect()
client.loop_stop()
cap.release()
cv2.destroyAllWindows()