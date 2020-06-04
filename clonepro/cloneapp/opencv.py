import cv2
from cloneapp.models import Videos

def getFrame(sec,count,url_of_video):
    video = Videos.objects.last()
    #vidcap = cv2.VideoCapture('videos/Python Django Framework - Full Course for Beginners.mp4')
    vidcap = cv2.VideoCapture('media/' + url_of_video)
    
    vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
    hasFrames,image = vidcap.read()
    if hasFrames:
         cv2.imwrite('media/images/image'+ str(count) + '.jpg', image)     # save frame as JPG file
    return hasFrames
sec = 0
frameRate = 0.5 #//it will capture image in each 0.5 second


