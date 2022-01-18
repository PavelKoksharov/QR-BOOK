import qrcode
from django import template

register = template.Library()


def generateQR(data="again?"):
    qr = qrcode.make(data)
    qr.save("Test.png")
    return data


# qr = generateQR()

import cv2
import time


@register.simple_tag(name='scan')
def scanQR():
    # initalize the camera

    cap = cv2.VideoCapture(0)
    # initialize the OpenCV QRCode detector
    detector = cv2.QRCodeDetector()
    start_time = time.time()
    while time.time() - start_time < 10:
        _, img = cap.read()
        # detect and decode
        data, vertices_array, _ = detector.detectAndDecode(img)
        # check if there is a QRCode in the image
        if vertices_array is not None:
            if data:
                cap.release()
                cv2.destroyAllWindows()
                return f"{data}"
        # display the result
        cv2.imshow("img", img)
        # Enter q to Quit
        if cv2.waitKey(1) == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()
    return




