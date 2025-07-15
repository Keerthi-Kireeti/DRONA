import cv2
import torch
from groundingdino.util.inference import load_model, load_image, predict

# Load REF-DETR model
model = load_model("facebook/detr-resnet-50")

# Initialize webcam with DirectShow backend (for Windows)
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1080)  
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1920)
cap.set(cv2.CAP_PROP_FPS, 60)

def detect_objects():
    if not cap.isOpened():
        print("Error: Webcam not accessible!")
        return

    print("Webcam opened successfully. Starting detection...")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Frame not captured!")
            break

        print("Frame captured. Running REF-DETR detection...")
        image_tensor = load_image(frame)
        outputs = predict(model, image_tensor)

        for box, label, score in zip(outputs['boxes'], outputs['labels'], outputs['scores']):
            x1, y1, x2, y2 = map(int, box)
            confidence = float(score)
            label_text = f"{label}: {confidence:.2f}"

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label_text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        cv2.imshow("Real-Time Object Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):  
            break

    cap.release()
    cv2.destroyAllWindows()

def start_detection():
    detect_objects()
