import cv2
import mediapipe as mp
import pandas as pd
import time

gesture_name = input("Enter the gesture name: ")
duration = 10  # seconds to record
countdown = 3  # countdown before recording

cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
data = []

# Countdown
start_time = time.time()
while time.time() - start_time < countdown:
    ret, frame = cap.read()
    cv2.putText(frame, f"Starting in {countdown - int(time.time() - start_time)}...",
                (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.8, (0, 0, 255), 4)
    cv2.imshow("Prepare", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        exit()

# Start collecting
start_time = time.time()
while time.time() - start_time < duration:
    ret, frame = cap.read()
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    elapsed = time.time() - start_time
    cv2.putText(frame, f"Recording: {int(duration - elapsed)} sec left",
                (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            landmarks = []
            for lm in hand_landmarks.landmark:
                landmarks.extend([lm.x, lm.y, lm.z])
            landmarks.append(gesture_name)
            data.append(landmarks)

            mp.solutions.drawing_utils.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Collecting", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# Save to CSV
columns = [f"{axis}{i}" for i in range(21) for axis in ['x', 'y', 'z']] + ["label"]
df = pd.DataFrame(data, columns=columns)
df.to_csv(f"{gesture_name}.csv", index=False)
print(f"Data saved as {gesture_name}.csv")
