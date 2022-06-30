import cv2
import numpy as np
from shapely.geometry import Polygon
from collections import defaultdict
from datetime import datetime

cap = cv2.VideoCapture('load_unload.mp4')

ret,frame1 = cap.read()
ret,frame2 = cap.read()

pts = np.array([[460,320],[580,320],[580,400],[460,400]])
p2=Polygon(pts)

curr_frame = defaultdict(dict)
prev_frame = defaultdict(dict)
load_time = defaultdict(dict)
unload_time = defaultdict(dict)

contour_area_thresh = 1500
IOU_thresh = 500

counter_prev = 0
counter_now = 1

counter_array = []
freq_stats = None
#i=0
loading_start_time = None
loading_end_time = None
counter = 0

frame_width = int(cap.get(3)) 
frame_height = int(cap.get(4)) 

size = (frame_width, frame_height)
'''
result = cv2.VideoWriter('F:/DTDC/out_st3011.avi',  
                         cv2.VideoWriter_fourcc(*'MJPG'), 
                         30, size) 
'''

def most_frequent(list):
    return max(set(list), key = list.count)

while cap.isOpened():
    #ret,frame1 = cap.read()
    counter_prev+=1
    counter_now+=1

    loading = False
    
    if ret == False:
        print(ret)
        cap.release()
        cv2.destroyAllWindows()
        break
    
    ## Frame Preprocessing
    diff = cv2.absdiff(frame1,frame2)
    gray = cv2.cvtColor(diff,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5), 0 )
    _ , thresh = cv2.threshold(blur,20,255,cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated,mode = cv2.RETR_EXTERNAL,method =cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:        
        
        if cv2.contourArea(contour) < contour_area_thresh:
            continue
            
        (x, y, w, h) = cv2.boundingRect(contour)
        
        ##Calculating the IOU
        ROI = np.array([(x,y),(x,y+h),(x+w,y+h),(x+w,y)])
        p1=Polygon(ROI)        
        p3=p1.intersection(p2)
        IOU = int(p3.area)
        IOU_perc = IOU/int(p1.area)
        
        if IOU_perc > 0.2:         
            cv2.rectangle(frame1,(x,y),(x+w,y+h),(0,0,200),2)
            cv2.putText(frame1,'Loading/Unloading',(10,30),cv2.FONT_HERSHEY_SIMPLEX,
                       1.25, (0,0,255),2)
            loading = True
            
            if len(load_time)<1:
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")                
                load_time['out_time']=current_time
        
    try:
        if loading == True: 
            counter_array.extend([1]*5)
            #counter_array.append(1)
            if len(counter_array)>10:
                del counter_array[:5]  
        else:
            #counter_array.extend([0]*10)
            counter_array.append(0)
            del counter_array[:1]
            
        print(counter_array)   
        freq_stats = most_frequent(counter_array)

    except Exception as e:        
        print(e)
    
    try:
        if freq_stats != None:
            if loading_start_time == None:
                loading_start_time=datetime.now()

            curr_frame['freq_stats']= freq_stats

            try:
                if len(prev_frame)>0 and curr_frame['freq_stats']==0:
                    if curr_frame['freq_stats'] == prev_frame['freq_stats']:
                        counter+=1
                    else: counter=0
                    
                else: counter=0
                #print(counter)
            except Exception as e: 
                print(e)
            
            if counter>300:
                loading_end_time = datetime.now()
            if counter>2000:
                load_time = defaultdict(dict)
                unload_time = defaultdict(dict)
                freq_stats = None
                loading_start_time = None
                loading_end_time = None

            prev_frame['freq_stats'] = curr_frame['freq_stats']
            
            if loading_end_time != None:            
                if len(load_time)>0 and freq_stats == 0 and loading_start_time != None and (loading_end_time-loading_start_time).seconds>10:
                    if len(unload_time)<1:
                        now = datetime.now()
                        current_time = now.strftime("%H:%M:%S")                
                        unload_time['out_time'] = current_time    
        
            if len(load_time)>0:
                cv2.putText(frame1,"Loading/Unloading start time : {}".format(load_time['out_time']),(10,50),cv2.FONT_HERSHEY_SIMPLEX,
                    0.75, (0,255,255),2)
                
            if len(unload_time)>0:
                cv2.putText(frame1,"Loading/Unloading end time : {}".format(unload_time['out_time']),(10,70),cv2.FONT_HERSHEY_SIMPLEX,
                        0.75, (0,255,255),2)

    except Exception as e:
        print(e)
            
    cv2.polylines(frame1, [pts],  isClosed=True, color=(255, 0, 0), thickness=2) 
    cv2.imshow('detection',cv2.resize(frame1,(960,546))) 

    #result.write(frame1)
    
    frame1 = frame2.copy()
    ret, frame2 = cap.read()    
    
    if cv2.waitKey(30) & 0xFF ==ord('q'):
        #result.release()
        cap.release()
        cv2.destroyAllWindows()
        break