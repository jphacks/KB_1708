import slidecapture

cap = slidecapture.SlideCapture(dev_id=1)
cap.camera_test(img_size=(800, 600))
cap.close()