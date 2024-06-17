from serial.tools import list_ports
from pydobot import dobot
import numpy as np
import pydobot
import keyboard
import pygame
import math
import sympy as sp
from time import sleep
from Dobot import Data
STEP = 10
SPEED = 100
PORT= 'COM7'
pose = {}  # Khai báo từ điển để lưu trữ vị trí
x = {}  # Khai báo từ điển để lưu trữ tọa độ x
y = {}  # Khai báo từ điển để lưu trữ tọa độ y
z = {}  # Khai báo từ điển để lưu trữ tọa độ z
r = {}  # Khai báo từ điển để lưu trữ tọa độ r
x_C={}
y_C={}
# alpha=math.pi*45/180
# beta=math.pi*(45)/180

#ham ket noi port
def setup_robot(port):
    available_ports = list_ports.comports()
    print(f'available ports: {[x.device for x in available_ports]}')
    _device = pydobot.Dobot(port=port)
    _device.speed(SPEED, SPEED)
    return _device

def toa_do():
    
    for i in range(1, 6):  # Sử dụng range để tạo vòng lặp từ 1 đến 4
        print("Nhấn phím 'Enter' để lấy vị trí...")
        keyboard.wait("enter")  # Chờ đợi người dùng nhấn phím "Enter"
        pose[i] = device.get_pose()
        x[i] = pose[i].position.x
        y[i] = pose[i].position.y
        z[i] = pose[i].position.z
        r[i] = pose[i].position.r
        print(f'x:{pose[i].position.x}, y:{pose[i].position.y}, z:{pose[i].position.z}')

########################################

#########################

# Tính độ dài cạnh AB
def find_point_c(alpha, beta):
    #tinh do dai canh AB
    length_abs = np.sqrt((x[2] - x[1])**2 + (y[2] - y[1])**2)
    print(f'length_abs{length_abs}')
    #tinh do dai canh AH
    length_ahs= (length_abs*np.tan(beta))/(np.tan(alpha)+ np.tan(beta))
    print(f'length_AH{length_ahs}')
    #tinh do dai canh AC
    length_acs= (length_ahs/np.cos(alpha))
    print(f'length_AC{length_acs}')
    #tinh do dai canh BC
    length_bcs=((length_abs-length_ahs)/np.cos(beta))
    print(f'length_BC{length_bcs}')
    
    # dat bien toa do diem C
    
    A=(x[1]-x[2])
    B=(y[1]-y[2])
    C= length_bcs**2-length_acs**2 +A*(x[1]+x[2]) + B*(y[1]+y[2])

    a=(B**2+A**2)/B**2
    b=-2*x[1]-((C*A-2*B*y[1]*A)/B**2)
    c=x[1]**2+((C-2*B*y[1])**2)/(4*B**2)-length_acs**2
    delta= b**2-4*a*c
    #diem E1
    XX1=(-b-np.sqrt(delta))/(2*a)
    YY1=(C-2*A*XX1)/(2*B)
    #diem E2
    XX2=(-b+np.sqrt(delta))/(2*a)
    YY2=(C-2*A*XX2)/(2*B)
    # else:
    x_C[2]=XX2
    y_C[2]=YY2
    x_C[1]=XX1
    y_C[1]=YY1
    print(f'C1({XX1},{YY1}),C2({XX2},{YY2})')



def Move_to_E(_device):
    
    print(f'tinh toan ...')
    if(x[1]<0 or x[2]<0):
        _X=x_C[1]
        _Y=y_C[1]
    else:
        _X=x_C[2]
        _Y=y_C[2]
        
    _Z = z[1]
    _R = r[1]
    
    _id=_device.move_to(160, 131, 80, _R)
    _device.wait_for_cmd(_id)
    _device.grip(enable)
    _id=_device.move_to(_X, _Y, 80, _R)
    _device.wait_for_cmd(_id)
    
    _id=_device.move_to(_X, _Y, -20, _R)
    _device.wait_for_cmd(_id)
    
    _id=_device.move_to(_X, _Y, 80, _R)
    _device.wait_for_cmd(_id)
    
    _id=_device.move_to(x[5], y[5], 80, _R)
    _device.wait_for_cmd(_id)
    
    _id=_device.move_to(x[5], y[5], -20, _R)
    _device.wait_for_cmd(_id)
    
    _id=_device.move_to(x[5], y[5], 80, _R)
    _device.wait_for_cmd(_id)
    
    _id=_device.move_to(160, 131, 80, _R)
    _device.wait_for_cmd(_id)
    
    print(f'di chuyen: {_X}, {_Y},{ _Z}, {_R}')
    


if __name__ == '__main__':
    
    device = setup_robot(PORT)
    toa_do()
    for i in range(1, 5):  # Sử dụng range để tạo vòng lặp từ 1 đến 4
        print(f'toa do diem {i}x:{x[i]}, y:{y[i]}, z:{z[i]}')
        
    find_point_c()
    #determine_rotation_direction()
    # #while True:
    Move_to_E(device)
    sleep(2)
    #Move_to_goal(device)
    
#####










