import os
from image_recognition_singlecam import image_recognition

img_dir = "C:\\Users\\Dell\\Desktop\\Projects\\Size_Detect_OpenCV\\Final\\Utility\\Image Detection\\"
background = os.path.join(img_dir, "cropped_image.jpg")
target = os.path.join(img_dir, "cropped_image1.jpg")

# Check if files exist before proceeding
if not os.path.exists(background):
    print(f"Background image not found: {background}")
if not os.path.exists(target):
    print(f"Target image not found: {target}")

imageRec = image_recognition(print_status=True, write_images=True, image_Path=img_dir, testing_Path=img_dir, preview_images=True)
imageRec.test_objectDetect("cropped_image", "cropped_image1")