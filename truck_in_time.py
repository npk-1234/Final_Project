import numpy as np
import cv2
from scipy import stats
import collections
from datetime import datetime   

cap = cv2.VideoCapture('Truck_in.mp4')

#contour_area_thresh=1000

#ret,frame1 = cap.read()

frame_width = int(cap.get(3)) 
frame_height = int(cap.get(4)) 

size = (frame_width, frame_height)

truck_in_time = collections.defaultdict(dict)

## Defining color ranges
LOWER_GATE_COLOR = np.array([0, 8, 39])
UPPER_GATE_COLOR = np.array([113, 70, 219])

LOWER_WHITE = np.array([0,0,168])
UPPER_WHITE = np.array([172,111,255])

'''
result = cv2.VideoWriter('F:/DTDC/out_st3.avi',  
                         cv2.VideoWriter_fourcc(*'MJPG'), 
                         30, size) 
'''


## Color Detection Function
def color_detection(hsv):
    """
    Finds the colour at the specified area
    """ 
    #print("entered")

    #mask_yellow = cv2.inRange(hsv, LOWER_YELLOW, UPPER_YELLOW)
    gate_color = cv2.inRange(hsv,LOWER_GATE_COLOR,UPPER_GATE_COLOR)
    white_color = cv2.inRange(hsv,LOWER_WHITE,UPPER_WHITE)
    
    mask_gate_flatten = gate_color.flatten()
    mask_mode_gate = stats.mode(mask_gate_flatten)[0][0]
    
    mask_white_flatten = white_color.flatten()
    mask_mode_white = stats.mode(mask_white_flatten)[0][0]
    
    gate_perc = (gate_color==255).mean()

    if mask_mode_gate == 255:
        color = 'Gate Color'
    elif mask_mode_white ==255:
        color = 'White'
    else:
        color = 'Black'

    return color,gate_perc

while cap.isOpened():
    
    ret,frame1 = cap.read()
    #counter+=1    
    
    if ret == False:
        print(ret)
        cap.release()
        cv2.destroyAllWindows()
        break
    frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)

    cropped_img1 = frame1[100:125,455:600]
    cropped_img2 = frame1[100:125,700:840]
    cropped_img3 = frame1[255:400,700:840]
    cropped_img4 = frame1[255:400,450:600]

    hsv1 = cv2.cvtColor(cropped_img1, cv2.COLOR_RGB2HSV)
    hsv2 = cv2.cvtColor(cropped_img2, cv2.COLOR_RGB2HSV)
    hsv3 = cv2.cvtColor(cropped_img3, cv2.COLOR_RGB2HSV)
    hsv4 = cv2.cvtColor(cropped_img4, cv2.COLOR_RGB2HSV)

    colour1,gate_perc1 = color_detection(hsv1)
    colour2,gate_perc2 = color_detection(hsv2)
    colour3,gate_perc3 = color_detection(hsv3)
    colour4,gate_perc4 = color_detection(hsv4)
    #print("color1:",colour1)
    #print("color2:",colour2)
    #print("color3:",colour3)
    #print("color4:",colour4)

    frame1 = cv2.cvtColor(frame1, cv2.COLOR_RGB2BGR)
    #print(colour1,blue_perc1,colour2,blue_perc2,colour3,blue_perc3,colour4,blue_perc4)

    #if (colour1 == 'Gate Color') and (colour2 == 'Gate Color') and (blue_perc3<0.15) and (blue_perc4<0.15): #or (blue_perc>0.9):
    if (colour1 == 'Gate Color') and (gate_perc1>0.8) and (colour2 == 'Gate Color') and (gate_perc2>0.8) and (colour3 == 'Gate Color') and (gate_perc3>0.8) and (colour4 == 'Gate Color') and (gate_perc1>0.9):
        cv2.putText(frame1,"Status: Gate Closed",(10,70),cv2.FONT_HERSHEY_COMPLEX,
                           1.5, (0,250,0),3)
    elif (colour1 == 'Gate Color') and (colour2 == 'Gate Color') and ((colour3 == 'Black') or (colour4 == 'Black')):
        if colour3 == 'Black':
            cv2.rectangle(frame1,(700,255),(840,400),(0,0,255),thickness=2)
            cv2.putText(frame1,"Truck 1",(700,250),cv2.FONT_HERSHEY_COMPLEX,
                           0.75, (0,250,0),2)
            cv2.putText(frame1,"Status: Gate Open",(10,70),cv2.FONT_HERSHEY_COMPLEX,
                           1.5, (0,0,255),3)
            
        if colour4 == 'Black':
            cv2.rectangle(frame1,(450,255),(600,400),(0,0,255),thickness=2)
            
            cv2.putText(frame1,"Truck 2",(450,250),cv2.FONT_HERSHEY_COMPLEX,
                           0.75, (0,255,255),2)
            cv2.putText(frame1,"Status: Gate Open",(10,70),cv2.FONT_HERSHEY_COMPLEX,
                           1.25, (0,0,255),3)
            if len(truck_in_time)<1:
                #print("entered")
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")                
                truck_in_time['-in_time']=current_time
            cv2.putText(frame1,"-In_time : {}".format(truck_in_time['-in_time']),(550,250),cv2.FONT_HERSHEY_SIMPLEX,
                           0.75, (0,0,255),2)
    else:
        #print("blue_perc3:",blue_perc3)
        #print("blue_perc4:",blue_perc4)
        cv2.putText(frame1,"Status: Gate Open",(10,70),cv2.FONT_HERSHEY_COMPLEX,
                           1.25, (0,0,255),3)
        cv2.rectangle(frame1,(450,255),(600,400),(0,0,255),thickness=2)
        cv2.rectangle(frame1,(700,255),(840,400),(0,0,255),thickness=2)
        #cv2.rectangle(frame1,(700,100),(840,125),(0,0,255),thickness=2)
        #cv2.rectangle(frame1,(455,100),(600,125),(0,0,255),thickness=2)    
    '''
    cv2.rectangle(frame1,(455,100),(600,125),(0,0,255),thickness=2)
    cv2.putText(frame1,"rect1",(455,90),cv2.FONT_HERSHEY_SIMPLEX,0.75,(255,0,0),2)
    cv2.rectangle(frame1,(700,100),(840,125),(0,0,255),thickness=2)
    cv2.putText(frame1,"rect2",(700,90),cv2.FONT_HERSHEY_SIMPLEX,0.75,(255,0,0),2)
    cv2.rectangle(frame1,(700,255),(840,400),(0,0,255),thickness=2)
    cv2.putText(frame1,"rect3",(700,250),cv2.FONT_HERSHEY_SIMPLEX,0.75,(255,0,0),2)
    cv2.rectangle(frame1,(450,255),(600,400),(0,0,255),thickness=2)
    cv2.putText(frame1,"rect4",(450,250),cv2.FONT_HERSHEY_SIMPLEX,0.75,(255,0,0),2)  
    '''
    #print(truck_in_time)
    cv2.imshow('detection',cv2.resize(frame1,(960,546))) 
    #result.write(frame1)
    
    if cv2.waitKey(30) & 0xFF ==ord('q'):
        #result.release()
        cap.release()
        cv2.destroyAllWindows()
        break