import cv2
import pytesseract as pt
#import easyocr
import os

texts = []
def split_video_to_frame(video):
    picN = 1
    if(not os.path.exists('cashe/')):
        os.mkdir('cashe/')
    
    while(True):
        isFrame, pic = video.read()
        if isFrame:
            cv2.imwrite(f'cashe/pic{picN}.jpg', pic)
            t = read_text_from_frame()
            texts.append(t)
            os.remove(f'cashe/pic{picN}.jpg')
        else:
            break
        picN+=1

    video.release()


def read_text_from_frame():
    img= cv2.imread('prim.jpg')
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    
    print(pt.image_to_string(gray))


print('Write path of video file')
video = cv2.VideoCapture(input())
split_video_to_frame(video=video)
print(texts)
