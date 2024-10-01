# decode.py

from pyzbar import pyzbar
import cv2
import base64

class QR_decoder:
    def __init__(self):
        self.info = {}

    def decode(self, image):
        """Декодируем все qr-коды на изображении"""

        decoded_objects = pyzbar.decode(image)
        for obj in decoded_objects:
            if obj.type == "QRCODE":
                self.info["type"] = obj.type
                self.info["data"] = obj.data.decode('utf-8')  # Декодируем байты в строку
            else:
                break

        return self.draw_qrcode(obj, image)


    def draw_qrcode(self, decoded, image):
        """Рисуем рамку вокруг QR-кода"""

        image = cv2.rectangle(image, (decoded.rect.left, decoded.rect.top),
                              (decoded.rect.left + decoded.rect.width, decoded.rect.top + decoded.rect.height),
                              color=(0, 255, 0), thickness=5)
        return image


    def create_qr_code_img(self, img):
        """Конвертируем изображение в формат PNG и затем в Base64"""

        _, buffer = cv2.imencode('.png', img)
        img_base64 = base64.b64encode(buffer).decode("utf-8")

        if img is not None:
            return img_base64
        else:
            raise Exception("Ошибка при обработке изображения")


    def get_qr_code_data(self, qrcode):
        # Загружаем изображение с помощью OpenCV
        img = cv2.imread(qrcode)

        # Декодируем QR-код и рисуем рамку
        img = self.decode(img)

        img_base64 = self.create_qr_code_img(img)
        return self.info, img_base64

