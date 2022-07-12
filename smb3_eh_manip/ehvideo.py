import cv2


class EHVideo:
    def __init__(self):
        self.video = cv2.VideoCapture("data/orange-nodeath-eh-v0.avi")