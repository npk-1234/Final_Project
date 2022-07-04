import cv2

from datetime import datetime

from utils import color_detection_out,display_time_status

cap = cv2.VideoCapture('F:/DTDC/Truck_out_Trim.mp4')

def truck_out(frame1,curr_frame,truck_out_time):

    hsv = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)

    color = color_detection_out(frame1)

    cropped_img1 = frame1[240:300, 440:580]
    cropped_img2 = frame1[320:380, 440:580]

    hsv1 = cv2.cvtColor(cropped_img1, cv2.COLOR_BGR2HSV)
    hsv2 = cv2.cvtColor(cropped_img2, cv2.COLOR_BGR2HSV)

    color1 = color_detection_out(hsv1)
    color2 = color_detection_out(hsv2)

    curr_frame['frame1']['black_perc'] = color1[1]
    curr_frame['frame2']['black_perc'] = color2[1]
    curr_frame['frame2']['yellow_perc'] = color2[3]
    curr_frame['frame2']['white_perc'] = color2[4]
    curr_frame['frame2']['blue_perc'] = color2[5]
    curr_frame['frame1']['white_perc'] = color1[4]

    if 0.2 < curr_frame['frame2']['white_perc'] < 0.8 or 0.2 < curr_frame['frame1']['white_perc'] < 0.8:
        if len(truck_out_time) < 1:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            truck_out_time['out_time'] = current_time
        cv2.rectangle(frame1, (450, 255), (600, 400), (0, 0, 255), thickness=2)
        # cv2.putText(frame1, "Out_time : {}".format(truck_out_time['out_time']), (550, 250), cv2.FONT_HERSHEY_SIMPLEX,
        #             0.75, (0, 0, 255), 2)
        display_time_status(frame1, 'truck_out_time', truck_out_time['out_time'])
