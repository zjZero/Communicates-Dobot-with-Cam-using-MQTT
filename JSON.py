import json
import random
import time

time.sleep(1)
A = random.randint(1, 100)
B = random.randint(1, 100)
x = random.uniform(0, 1)  # Sử dụng uniform để nhận giá trị ngẫu nhiên với phân phối đều từ 0 đến 1
y = random.uniform(0, 1)

Send_MSG = {
           "Alpha": A,
            "Beta": B,
            "x": x,
            "y": y
           }
  
MSG_JSON = json.dumps(Send_MSG)

data = json.loads(MSG_JSON)
print(data)
print(data['Alpha'])


