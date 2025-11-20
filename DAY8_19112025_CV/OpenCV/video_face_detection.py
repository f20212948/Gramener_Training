# import cv2
# # Load the cascade from OpenCV's default haarcascades folder
# face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")


# cap = cv2.VideoCapture("cv_practs.mp4")

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         print("End of video or failed to read frame.")
#         break
#     # Convert frame to grayscale
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     # Detect faces
#     faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=6)
#     # Draw rectangles around detected faces
#     for (x, y, w, h) in faces:
#         cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
#     # Show the frame
#     cv2.imshow("Face Detection", frame)
#     # Quit with 'q'
#     if cv2.waitKey(25) & 0xFF == ord('q'):  # use delay=25 for video playback speed
#         break
# print("Total frames:", int(cap.get(cv2.CAP_PROP_FRAME_COUNT)))

# # Release resources
# cap.release()
# cv2.destroyAllWindows()


import cv2

# --- Configuration ---
# Detect faces only every N frames to save computational time
# and allow the tracker to do its job in between.
DETECTION_INTERVAL = 30 
frame_count = 0

# Load the cascade from OpenCV's default haarcascades folder
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# List to store our active trackers and their corresponding bounding boxes
# Each element will be: (tracker_object, bbox)
trackers = [] 

cap = cv2.VideoCapture("cv_practs.mp4")

# Check if video opened successfully
if not cap.isOpened():
    print("Error: Could not open video file.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("End of video or failed to read frame.")
        break
    
    # --- 1. Update Trackers ---
    # Update all active trackers from the previous frame
    new_trackers = []
    
    for tracker_obj, bbox in trackers:
        # Update the tracker
        success, new_bbox = tracker_obj.update(frame)
        
        if success:
            # If tracking succeeded, add the updated tracker/bbox to the new list
            new_trackers.append((tracker_obj, new_bbox))
            # Draw the bounding box based on the tracker's prediction
            (x, y, w, h) = [int(v) for v in new_bbox]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # If tracking failed, it's discarded from the new_trackers list
    
    trackers = new_trackers # Use the successfully updated trackers for the next frame
    
    # --- 2. Face Detection (Runs Sparsely) ---
    # Only run the expensive face detection every DETECTION_INTERVAL frames
    if frame_count % DETECTION_INTERVAL == 0:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces (these are new faces or faces to re-initialize tracking)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=6, minSize=(30, 30))
        
        # Check detected faces against existing tracked faces (simple overlap check)
        for (x, y, w, h) in faces:
            new_face_bbox = (x, y, w, h)
            is_already_tracked = False
            
            # Simple check to prevent double-tracking the same face
            for _, tracked_bbox in trackers:
                # We check if the center of the new detection is inside any tracked bbox
                cx, cy = x + w // 2, y + h // 2
                tx, ty, tw, th = [int(v) for v in tracked_bbox]
                
                if tx < cx < tx + tw and ty < cy < ty + th:
                    is_already_tracked = True
                    break
            
            # If it's a new face (or a face that was just lost), start a new tracker
            if not is_already_tracked:
                # Create a new CSRT tracker instance
                tracker = cv2.TrackerCSRT_create()
                tracker.init(frame, new_face_bbox)
                
                # Add the new tracker to our list
                trackers.append((tracker, new_face_bbox))
                
                # Draw the initial detection box (optional, as the tracker update will draw it)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2) # Blue for newly detected

    # --- 3. Display and Loop Control ---
    cv2.imshow("Face Detection and Tracking (CSRT)", frame)
    
    frame_count += 1
    
    # Quit with 'q'
    if cv2.waitKey(25) & 0xFF == ord('q'): 
        break

print("Total frames processed:", frame_count)

# Release resources
cap.release()
cv2.destroyAllWindows()