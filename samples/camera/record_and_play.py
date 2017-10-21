import slidecapture
import time

filename = 'record_test.mp4'
cap = slidecapture.SlideCapture(1)
cap.record_video(filename)
time.sleep(3)
cap.play_video(filename)
cap.release_camera()