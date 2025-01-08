import serial
from ultralytics import YOLO
import cv2
import numpy as np
import mss
import win32gui
from pynput.keyboard import Controller as KeyboardController

def get_active_window_title():
    return win32gui.GetWindowText(win32gui.GetForegroundWindow())


def aimbot():
    # Initialize Serial Communication
    arduino = serial.Serial(port='COM7', baudrate=115200, timeout=1)

    model = YOLO("train9/weights/best.pt")
    sct = mss.mss()
    monitor = sct.monitors[1]

    screen_width = monitor["width"]
    screen_height = monitor["height"]

    region_width = 320
    region_height = 320
    region = {
        "top": (screen_height - region_height) // 2,
        "left": (screen_width - region_width) // 2,
        "width": region_width,
        "height": region_height,
    }

    print(f"Capturing region: {region}")
    screen_mid_x = screen_width / 2
    screen_mid_y = screen_height / 2
    threshold = 5
    keyboard1 = KeyboardController()

    while True:
        active_window = get_active_window_title()
        if "VALORANT" in active_window.upper():
            print(f"Active window: {active_window}")
            screenshot = np.array(sct.grab(region))
            frame = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)
            results = model.predict(frame, imgsz=640, conf=0.4, device=0)

            for result in results:
                for box in result.boxes:
                    # Get class ID and name
                    class_id = int(box.cls[0])  # Class index
                    class_name = model.names[class_id]  # Class name

                    # Filter for 'enemyhead'
                    if class_name == "enemyHead":
                        x1, y1, x2, y2 = box.xyxy[0].tolist()

                        bbox_center_x = (x1 + x2) / 2
                        bbox_center_y = (y1 + y2) / 2

                        screen_x = int(region["left"] + bbox_center_x)
                        screen_y = int(region["top"] + bbox_center_y)

                        print(f"Detected enemyhead at: ({screen_x}, {screen_y})")
                        if (
                            abs(screen_x - screen_mid_x) <= threshold
                            and abs(screen_y - screen_mid_y) <= threshold
                        ):
                            keyboard1.press("p")
                            keyboard1.release("p")

                        relative_x = screen_x - screen_mid_x
                        relative_y = screen_y - screen_mid_y

                        sensitivity = 0.8
                        relative_x = relative_x * sensitivity
                        relative_y = relative_y * sensitivity

                        print(f"Shooting at {relative_x},{relative_y}")
                        try:
                            arduino.write(f"{relative_x},{relative_y}\n".encode())
                        except Exception as e:
                            print(f"Serial write error: {e}")

        else:
            print(f"Active window: {active_window} - VALORANT not detected")

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cv2.destroyAllWindows()
    arduino.close()


if __name__ == "__main__":
    aimbot()
