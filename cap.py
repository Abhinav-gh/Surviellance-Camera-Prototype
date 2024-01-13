import cv2
for i in range(10):
    print(i)
    try:
        cc = cv2.VideoCapture(i)
    except Exception as e:
        print(e)
        continue
    ret,_=cc.read();
    print(ret)
    cc.release()

