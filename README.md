# gesture_control

---

# Hand Gesture-Controlled Commanding System

A Python-based real-time hand gesture recognition system using OpenCV and MediaPipe that allows users to control applications through custom hand gestures. The system includes a full UI, custom ML model training, and gesture-to-app mapping.

---

## Features

- Real-time hand tracking using MediaPipe  
- Train custom gestures with your own dataset  
- Associate gestures with apps (e.g., launch Chrome with "thumbs up")  
- Interactive Tkinter UI  
- Save/load model with joblib  
- Cooldown timer to avoid accidental gesture detection  
- All actions mapped and stored via a JSON file  

---

## Tech Stack

- Python 3.8+  
- OpenCV  
- MediaPipe  
- Scikit-learn  
- Pandas  
- Tkinter  
- Joblib  

---

## Project Structure

```
├── collect_gesture_data.py       - Collect landmark data for gestures  
├── combine_gesture_data.py       - Combine all gesture CSVs into one dataset  
├── train_model.py                - Train ML model (KNN or others)  
├── main_app.py                   - Final application UI and logic  
├── gesture_model.pkl             - Trained model file  
├── gesture_actions.json          - Gesture-to-app mapping  
├── *.csv                         - Individual gesture data files  
```

---

## Setup Instructions

1. Clone the repository:
   - Open terminal or command prompt
   - Navigate to your desired folder
   - Run: git clone https://github.com/your-username/hand-gesture-commanding.git
   - Then navigate into the folder using: cd hand-gesture-commanding

2. Install dependencies:
   - Run: pip install -r requirements.txt

3. Collect Gesture Data:
   - Run: python collect_gesture_data.py
   - Enter a gesture name when prompted (e.g., "thumbs_up")
   - Perform the gesture within the countdown timer

4. Combine CSVs:
   - Run: python combine_gesture_data.py

5. Train the Model:
   - Run: python train_model.py

6. Launch the App:
   - Run: python main_app.py

---

## How It Works

1. Uses MediaPipe to extract hand landmark positions (x, y, z)  
2. Stores landmark data with gesture label  
3. Trains a classifier (e.g., KNN) on this dataset  
4. Classifies real-time gestures via webcam  
5. Maps detected gesture to an application defined in the UI  

---

## Example Use Cases

- Two fingers → Open VS Code  
- Thumbs up → Launch Google Chrome  
- Open palm → Open File Explorer  
- Fist → Play media player  

---

## Future Improvements

- Support for multi-hand detection  
- Gesture prediction confidence scoring  
- Support for other ML models (e.g., SVM, CNN)  
- Cross-platform support (e.g., Raspberry Pi or Android)  

---

## License

This project is licensed under the MIT License.

---

## Acknowledgements

- MediaPipe  
- OpenCV  
- Scikit-learn  
- Tkinter

---
