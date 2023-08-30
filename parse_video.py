#!/usr/bin/env python3
import cv2
import time
import os

cap = cv2.VideoCapture("/path/to/video.mov")

def parse_states(states):
    frame_counts = []
    last_state, count = 0, 0 
    for state in states:
        if last_state != state and state: # 0 -> 1
            last_state = state
            count += 1
        elif state: # 1 -> 1
            count += 1
        elif last_state != state and not state: # 1 -> 0
            frame_counts.append(count)
            count = 0
            last_state = state
    return frame_counts

# Determine the state (idle/sign) of a frame by checking to see if there exists a row with red channel average LESS than the threshold
def frame_to_state(frame, channel, threshold):
    for row in range(len(frame)):
        num_cols = len(frame[row])
        row_avg = sum([frame[row, col, channel] for col in range(num_cols)]) / num_cols
        if row_avg < threshold:
            return 1
    return 0

cap.set(cv2.CAP_PROP_POS_FRAMES, 11700 + 133985) # this is thankfully not buggy here, 98 = first sig start, 11700 = start of slomo

# 226 signatures captured at 30 fps
parsed_states = [69, 168, 169, 169, 171, 171, 169, 171, 171, 166, 168, 169, 162, 171, 171, 171, 166, 169, 170, 167, 171, 171, 170, 172, 168, 172, 171, 168, 170, 171, 169, 169, 171, 171, 169, 171, 148, 172, 171, 170, 171, 171, 169, 170, 169, 171, 170, 168, 172, 163, 171, 171, 169, 169, 168, 166, 168, 166, 166, 169, 172, 171, 170, 172, 171, 167, 168, 168, 171, 171, 171, 170, 171, 164, 168, 166, 171, 171, 171, 161, 168, 164, 169, 171, 171, 171, 171, 171, 171, 171, 171, 161, 166, 164, 170, 164, 171, 171, 163, 171, 171, 169, 171, 171, 171, 168, 166, 171, 160, 166, 169, 171, 172, 171, 171, 171, 167, 171, 171, 171, 163, 163, 167, 169, 171, 171, 159, 171, 163, 163, 170, 161, 168, 171, 165, 171, 167, 164, 167, 171, 171, 168, 166, 171, 166, 168, 171, 171, 171, 166, 172, 169, 167, 170, 171, 171, 171, 166, 171, 171, 171, 171, 164, 164, 171, 170, 171, 169, 171, 169, 170, 169, 168, 164, 167, 171, 171, 165, 170, 162, 169, 164, 168, 168, 168, 167, 168, 171, 171, 170, 171, 168, 169, 171, 171, 171, 172, 161, 169, 170, 171, 171, 163, 163, 171, 170, 171, 172, 168, 169, 168, 166, 171, 169, 170, 169, 171, 167, 168, 171, 168, 164, 171, 170, 166, 166, 168, 172, 172, 169, 169, 168, 167, 164, 164, 170, 163, 168, 169, 171, 169, 162, 143, 161, 172, 169, 169, 171, 164, 170, 166, 171, 171, 171, 170, 171, 170, 162, 168, 166, 171, 160, 161, 172, 169, 167, 170, 171, 169, 172, 169, 170, 166, 171, 171, 168, 169, 171, 169, 169, 169, 171, 169, 168, 166, 168, 172, 172, 171, 168, 169, 166, 166, 171, 171, 171, 171, 171, 170, 171, 161, 170, 161, 171, 171, 162, 164, 169, 171, 171, 168, 165, 171, 171, 171, 170, 167, 171, 168, 164, 165, 168, 164, 170, 168, 165, 159, 171, 170, 169, 172, 166, 171, 171, 171, 171, 171, 164, 171, 167, 168, 171, 170, 169, 169, 171, 170, 167, 168, 172, 168, 169, 171, 171, 166, 166, 171, 170, 163, 170, 171, 170, 172, 172, 164, 171, 171, 170, 168, 170, 151, 165, 162, 171, 169, 171, 171, 171, 169, 172, 169, 172, 168, 166, 169, 171, 168, 165, 170, 171, 170, 169, 168, 171, 169, 171, 171, 171, 171, 171, 169, 172, 171, 166, 169, 171, 170, 171, 169, 169, 169, 171, 171, 172, 171, 171, 171, 169, 171, 171, 169, 171, 157, 172, 168, 168, 171, 171, 169, 171, 167, 163, 166, 171, 152, 168, 171, 169, 169, 169, 165, 163, 168, 171, 171, 159, 166, 171, 168, 171, 168, 166, 166, 171, 166, 171, 171, 172, 168, 168, 171, 171, 169, 166, 169, 168, 166, 167, 171, 166, 171, 169, 171, 171, 169, 168, 171, 169, 167, 162, 166, 171, 171, 171, 171, 171, 171, 171, 170, 171, 171, 171, 171, 169, 168, 169, 170, 169, 169, 169, 170, 168, 172, 164, 169, 171, 171, 165, 166, 170, 171, 168, 169, 170, 171, 171, 171, 171, 171, 164, 171, 171, 171, 167, 170, 164, 163, 170, 171, 171, 171, 170, 168, 168, 164, 167, 165, 152, 171, 170, 171, 168, 166, 168, 172, 169, 166, 167, 172, 169, 166, 168, 172, 168, 169, 163, 167, 171, 164, 171, 168, 171, 171, 169, 171, 171, 170, 165, 168, 169, 169, 164, 171, 172, 170, 171, 170, 172, 169, 169, 168, 158, 167, 167, 168, 169, 163, 171, 171, 170, 172, 170, 171, 168, 172, 171, 171, 168, 168, 168, 171, 169, 165, 166, 170, 168, 170, 171, 171, 169, 171, 171, 166, 166, 170, 171, 171, 171, 171, 172, 171, 168, 172, 168, 172, 166, 169, 168, 169, 171, 171, 170, 170, 171, 168, 171, 171, 169, 170, 172, 171, 171, 171, 169, 170, 169, 166, 172, 171, 170, 168]
states = []
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    cv2.imshow("frame", frame)
    state = frame_to_state(frame, 2, 27) # BGR, not RGB, so this is the red channel
    states.append(state)
    print(state)
    if cv2.waitKey(20) & 0xff == ord('q'):
        break
    elif cv2.waitKey(20) & 0xff == ord('p'):
        print(parse_states(states))
cap.release()
cv2.destroyAllWindows()
parsed_states.extend(parse_states(states))
print(parsed_states)
