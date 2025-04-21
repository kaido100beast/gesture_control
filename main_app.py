import cv2
import mediapipe as mp
import numpy as np
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import subprocess
import joblib
import json
import os
import time
import fnmatch

def open_program(program_path):
    try:
        subprocess.run([program_path], shell=True)
        print(f"Opened {program_path}")
    except Exception as e:
        print(f"Error opening {program_path}: {e}")

def if_exe(directory, file):
    ls = file.split(directory)
    return ('\\' not in ls[1])

def list_exe_files(directory):
    exe_files = []
    for root, dirs, files in os.walk(directory):
        for file in fnmatch.filter(files, '*.exe'):
            full_path = os.path.join(root, file)
            if if_exe(directory, full_path):
                exe_files.append(full_path)
    return exe_files

class HandGestureApp:
    def __init__(self, root):
        self.last_action_time = 0
        self.cooldown_seconds = 2

        self.root = root
        self.root.title("Hand Gesture Recognition")

        self.label = ttk.Label(root, text="", font=("Helvetica", 16))
        self.label.pack(pady=10)

        self.canvas = tk.Label(root)
        self.canvas.pack()

        self.model = self.load_model("gesture_model.pkl")

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=1)

        self.cap = cv2.VideoCapture(0)
        self.is_recognition_started = False

        self.gesture_actions = {}
        self.load_gesture_actions()

        self.start_button = tk.Button(root, text="Start Recognition", command=self.start_gesture_recognition)
        self.start_button.pack(pady=5)

        self.register_button = tk.Button(root, text="Register Gesture", command=self.register_gesture)
        self.register_button.pack(pady=5)

        self.root.protocol("WM_DELETE_WINDOW", self.close_app)
        self.update()

    def load_model(self, path):
        try:
            return joblib.load(path)
        except Exception as e:
            messagebox.showerror("Model Error", f"Could not load model: {e}")
            exit()

    def load_gesture_actions(self):
        if os.path.exists("gesture_actions.json"):
            with open("gesture_actions.json", "r") as f:
                self.gesture_actions = json.load(f)
        else:
            self.gesture_actions = {}

    def save_gesture_actions(self):
        with open("gesture_actions.json", "w") as f:
            json.dump(self.gesture_actions, f)

    def update(self):
        ret, frame = self.cap.read()
        if ret and self.is_recognition_started:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb_frame)
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    landmarks = []
                    for lm in hand_landmarks.landmark:
                        landmarks.extend([lm.x, lm.y, lm.z])
                    try:
                        prediction = self.model.predict([landmarks])[0]
                        current_time = time.time()
                        if current_time - self.last_action_time > self.cooldown_seconds:
                            self.label.config(text=f"Detected: {prediction}")
                            self.perform_action(prediction)
                            self.last_action_time = current_time
                            self.stop_gesture_recognition()
                    except Exception as e:
                        print(f"Prediction error: {e}")
                    mp.solutions.drawing_utils.draw_landmarks(
                        frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS
                    )
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (640, 480))
        img = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=img)
        self.canvas.imgtk = imgtk
        self.canvas.configure(image=imgtk)
        self.root.after(10, self.update)

    def start_gesture_recognition(self):
        self.label.config(text="Prepare your gesture...")
        self.root.update()
        time.sleep(2)
        self.label.config(text="Recognition Started")
        self.is_recognition_started = True

    def stop_gesture_recognition(self):
        self.is_recognition_started = False
        self.label.config(text="Gesture Action Executed")

    def register_gesture(self):
        if not hasattr(self.model, 'classes_'):
            messagebox.showerror("Model Error", "Model does not contain gesture labels.")
            return

        popup = tk.Toplevel(self.root)
        popup.title("Register Gesture")

        ttk.Label(popup, text="Select Gesture:").pack(pady=5)
        gesture_var = tk.StringVar(popup)
        gesture_combo = ttk.Combobox(popup, textvariable=gesture_var, values=list(self.model.classes_))
        gesture_combo.pack(pady=5)

        # Application Tray
        ttk.Label(popup, text="Select from Application Tray:").pack(pady=5)
        directory = 'C:\\Users\\BarnwalA\\AppData\\Local\\Microsoft\\WindowsApps\\'
        app_files = list_exe_files(directory)
        app_var = tk.StringVar(popup)
        app_combo = ttk.Combobox(popup, textvariable=app_var, values=app_files, width=60)
        app_combo.pack(pady=5)

        def select_manual_file():
            path = filedialog.askopenfilename(title="Select .exe File", filetypes=[("Executable Files", "*.exe")])
            if path:
                app_var.set(path)

        ttk.Button(popup, text="Browse Manually", command=select_manual_file).pack(pady=5)

        def save_gesture_app():
            selected_gesture = gesture_var.get()
            selected_app = app_var.get()
            if not selected_gesture or not selected_app:
                messagebox.showwarning("Input Required", "Select both gesture and application.")
                return
            self.gesture_actions[selected_gesture] = selected_app
            self.save_gesture_actions()
            messagebox.showinfo("Registered", f"Gesture '{selected_gesture}' linked to: {selected_app}")
            popup.destroy()

        ttk.Button(popup, text="Save", command=save_gesture_app).pack(pady=10)

    def perform_action(self, gesture):
        if gesture in self.gesture_actions:
            try:
                subprocess.run([self.gesture_actions[gesture]], shell=True, check=True)
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Execution Error", f"Could not open:\n{self.gesture_actions[gesture]}")
            except Exception as e:
                messagebox.showerror("Error", f"An unexpected error occurred:\n{e}")

    def close_app(self):
        self.cap.release()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = HandGestureApp(root)
    root.mainloop()
