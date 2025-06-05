import face_recognition
import cv2

# Check if OpenCV works
print("OpenCV version:", cv2.__version__)

# Try loading an image (replace with any real image path you have)
image_path = "/Users/akhilb/Downloads/image.jpeg"  # Use any image of your face for testing
image = face_recognition.load_image_file(image_path)
face_locations = face_recognition.face_locations(image)
face_encodings = face_recognition.face_encodings(image)

print("Number of faces detected:", len(face_locations))
if face_encodings:
    print("Successfully extracted face encoding!")
else:
    print("Failed to extract face encoding.")
