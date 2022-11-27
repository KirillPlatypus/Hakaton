import cv2
import pytesseract as pt
import easyocr
import os

texts = []
def split_video_to_frame(video):
    picN = 1
    if(not os.path.exists('cashe/')):
        os.mkdir('cashe/')
    
    while(picN<=25):
        isFrame, pic = video.read()
        if isFrame:
            cv2.imwrite(f'cashe/pic{picN}.jpg', pic)
            t = read_text_from_frame(pic, picN)
            sort_test(texts=texts,t=t)

            os.remove(f'cashe/pic{picN}.jpg')
        else:
            break
        picN+=1

    video.release()


def read_text_from_frame(img, picN):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    cv2.imwrite('threshold_image.jpg',thresh1)

    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (12, 12))
    dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1)
    cv2.imwrite('dilation_image.jpg',dilation)

    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    im2 = img.copy()
    i=0
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)

        rect=cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cropped = im2[y:y + h, x:x + w]

        cv2.imwrite('rectanglebox.jpg',rect)

        #cv2.imwrite(f'cashe/cropped{i} {picN}.jpg',cropped)

        result = pt.image_to_string(cropped, config='--psm 7')
    
        #reader = easyocr.Reader(['ru'], gpu=True)
        #result = reader.readtext(f'cashe/cropped{i} {picN}.jpg', detail=0)
        
        #os.remove(f'cashe/cropped{i} {picN}.jpg')

        i+=1
        
    return result

def sort_test(texts, t):
    t = t.replace("\n\x0c",""); t = t.replace("\x0c",""); t = t.replace("(",""); t = t.replace(")",""); t = t.replace("/",""); t = t.replace("\n\n",""); t = t.replace(" ","")
    if(t != []):
        texts.append(t)



print('Write path of video file')
video = cv2.VideoCapture(input())
split_video_to_frame(video=video)

print(texts)
