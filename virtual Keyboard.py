import cv2
import numpy as np
import pyautogui as gui


cap = cv2.VideoCapture(0)
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

def key_pressed(frame,centre,board):
    for row in board:
        arr1 = list(np.int0(np.array(center) >= np.array(row[1])))
        arr2 = list(np.int0(np.array(center) <= np.array(row[2])))
        if arr1 == [1, 1] and arr2 == [1, 1]:
            if row[0] == '<-':
                gui.press('backspace')
            else:
                gui.press(row[0])
            cv2.fillConvexPoly(frame, np.array([np.array(row[1]),np.array([row[1][0], row[2][1]]),
                                              np.array(row[2]),np.array([row[2][0], row[1][1]])]),(255, 0, 0))
    return frame

def keyboard():
    max_keys = 11
    key_width = int(width / max_keys)
    row1_width = key_width * 11
    row2_width = key_width * 10
    row3_width = key_width * 9
    row4_width = key_width * 7
    row5_width = key_width * 5
    row_key = []

    # For 1st row
    x1, y1 = 0, int((height - key_width * 5) / 2)
    x2, y2 = key_width + x1, key_width + y1
    c1, c2 = x1, y1  # copying x1, x2, y1 and y2
    keys = "1 2 3 4 5 6 7 8 9 0 <-"
    keys = keys.split(" ")
    for key in keys:
        if key == "<-":
            row_key.append([key, (x1, y1), (x2, y2), (int((x2 + x1) / 2) - 25, int((y2 + y1) / 2) + 10)])
        else:
            row_key.append([key, (x1, y1), (x2, y2), (int((x2 + x1) / 2) - 5, int((y2 + y1) / 2) + 10)])
        x1 += key_width
        x2 += key_width
    x1, y1 = c1, c2  # copying back from c1, c2, c3 and c4

    # for the second row
    x1, y1 = int((row1_width - row2_width) / 2) + x1, y1 + key_width
    x2, y2 = key_width + x1, key_width + y1
    c1, c2 = x1, y1  # copying x1, x2, y1 and y2
    keys = "qwertyuiop"
    for key in keys:
        row_key.append([key, (x1, y1), (x2, y2), (int((x2 + x1) / 2) - 5, int((y2 + y1) / 2) + 10)])
        x1 += key_width
        x2 += key_width
    x1, y1 = c1, c2

# for third row
    x1, y1 = int((row2_width - row3_width) / 2) + x1, y1 + key_width
    x2, y2 = key_width + x1, key_width + y1
    c1, c2 = x1, y1
    keys = "asdfghjkl"
    for key in keys:
        row_key.append([key, (x1, y1), (x2, y2), (int((x2 + x1) / 2) - 5, int((y2 + y1) / 2) + 10)])
        x1 += key_width
        x2 += key_width
    x1, y1 = c1, c2

    # for fourth row
    x1, y1 = int((row3_width - row4_width) / 2) + x1, y1 + key_width
    x2, y2 = key_width + x1, key_width + y1
    c1, c2 = x1, y1
    keys = "zxcvbnm"
    for key in keys:
        row_key.append([key, (x1, y1), (x2, y2), (int((x2 + x1) / 2) - 5, int((y2 + y1) / 2) + 10)])
        x1 += key_width
        x2 += key_width
    x1, y1 = c1, c2

    # for the space bar
    x1, y1 = int((row4_width - row5_width) / 2) + x1, y1 + key_width
    x2, y2 = 5 * key_width + x1, key_width + y1
    c1, c2 = x1, y1
    keys = " "
    for key in keys:
        row_key.append([key, (x1, y1), (x2, y2), (int((x2 + x1) / 2) - 5, int((y2 + y1) / 2) + 10)])
        x1 += key_width
        x2 += key_width
    x1, y1 = c1, c2

    return row_key

new_area,old_area=0,0
c,c2=0,0
flag_keypress=False

while True:
    board = keyboard()
    res, frame = cap.read()
    imgHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower = np.array([0, 203, 93], np.uint8)
    upper = np.array([179, 237, 255], np.uint8)
    mask = cv2.inRange(imgHSV, lower, upper)
    kernal = np.ones((5, 5), "uint8")
    mask = cv2.dilate(mask, kernal, iterations=5)

    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        cnt = max(contours, key=cv2.contourArea)
        if cv2.contourArea(cnt) > 400:
            rect=cv2.minAreaRect(cnt)
            center=list(rect[0])
            box = cv2.boxPoints(rect)
            box=np.int0(box)
            cv2.circle(frame, tuple(np.int0(center)), 2, (0, 255, 0), 2)
            cv2.drawContours(frame, [box], 0, (0, 0, 255), 2)

            new_area = cv2.contourArea(cnt)
            new_center = np.int0(center)
            if c == 0:
                old_area = new_area
            c += 1
            diff_area = 0
            if c > 3:
                diff_area = new_area - old_area
                c = 0
            if c2 == 0:
                old_center = new_center
            c2 += 1
            diff_center = np.array([0, 0])
            if c2 > 5:
                diff_center = new_center - old_center
                c2 = 0

            center_threshold = 10
            area_threshold = 200
            if abs(diff_center[0]) < center_threshold or abs(diff_center[1]) < center_threshold:
                #print(diff_area)
                if diff_area > area_threshold and flag_keypress == False:
                    img = key_pressed(frame, new_center, board)
                    flag_keypress = True
                elif diff_area < -(area_threshold) and flag_keypress == True:
                    flag_keypress = False
        else:
            flag_keypress = False
    else:
        flag_keypress = False

    for key in board:
        cv2.putText(frame, key[0], key[3], cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0))
        cv2.rectangle(frame, key[1], key[2], (0, 255, 0), 2)

    cv2.imshow("Keyboard", frame)
    if cv2.waitKey(1) & 0XFF==ord('q'):
        break

cap.release()
cv2.destroyAllWindows()