import cv2
import threading

def thread(func):
    def wrapper(*args, **kwargs):
        t = threading.Thread(target=func, args=args, kwargs=kwargs)
        t.start()
        return t
    return wrapper

class Scanner():
    def __init__(self, dbus):
        self.dbus = dbus
        self.decoder = cv2.QRCodeDetector()

        self.scanning = False
        self.show_camera = False

    @thread
    def scan(self):
        if self.scanning is True:
            self.dbus.log("There is another qr scan running", log_level="ERROR")
            self.dbus.DetectedQR("")
            return

        try:
            cam = cv2.VideoCapture(0)
            if cam.isOpened() is False:
                self.dbus.log("No camera connected")
                self.dbus.DetectedQR("")
                cam.release()
                return

            self.scanning = True
        except Exception as e:
            self.dbus.log("An error has ocurred when opening the webcam", log_level="ERROR")
            print(e)
            self.dbus.DetectedQR("")
            return

        self.scanning = True
        while True:
            _, frame = cam.read()
            ret, points = self.decoder.detect(frame)

            if self.show_camera is True:
                qr_points = points[0].astype(int)
                for i in range(4):
                    start = tuple(qr_points[i])
                    end = tuple(qr_points[(i + 1) % 4])
                    cv2.line(frame, start, end, (0,0,255), 3)

                cv2.imshow("Camera", frame)

            if ret is True:
                try:
                    content, _ = self.decoder.decode(frame, points)
                except Exception as e:
                    self.dbus.log(f"Error when detecting qr code from camera: {e}", log_level="WARN")
                    self.dbus.log("Ignoring...")
                    continue

                if content != "":
                    self.dbus.DetectedQR(content)
                    break

        self.scanning = False
        cam.release()

        if self.show_camera is True:
            cv2.destroyAllWindows()

        self.dbus.log("Released camera")
