import flet
from flet import Container, Image, Page, ElevatedButton, FilePicker, FilePickerResultEvent, Text
from decode import QR_decoder

decoder = QR_decoder()

def main(page: Page):
    page.window.width = 450  # Ширина окна
    page.window.height = 700  # Высота окна
    page.title = "Стенд для чтения QR-code"

    def on_file_picked(e: FilePickerResultEvent):
        if e.files:
            for f in e.files:
                if f.name.endswith(".png"):
                    try:
                        qr_info, img_base64 = decoder.get_qr_code_data(f.name)
                        qr_data.value = f"Type: {qr_info['type']}\nData: {qr_info['data']}"
                        status.value = f"File '{f.name}' uploaded and processed successfully"
                        img.src_base64 = img_base64
                        img.update()

                    except Exception as e:
                        status.value = f"ERROR: {str(e)}"
                else:
                    status.value = f"File '{f.name}' is not a PNG image."
        else:
            status.value = "File selection cancelled."

        page.update()

    status = Text()
    qr_data = Text()
    img = Image(
        src="qr-placeholder.png",  # Замените на URL вашего изображения
        width=400,  # Установите ширину изображения
        height=400,  # Установите высоту изображения
        fit="contain"  # Устанавливаем содержимое по контейнеру
    )

    container_qr_data = Container(
        content=qr_data,
        width=410,  # Ширина контейнера
        height=110,  # Высота контейнера
        border_radius=20,  # Скругление углов контейнера
        border=flet.border.all(2, "navy"),  # Добавление рамки
        padding=10  # Внутренние отступы
    )

    container_img = Container(
        content=img,
        width=410,  # Ширина контейнера
        height=410,  # Высота контейнера
        border_radius=20,  # Скругление углов контейнера
        border=flet.border.all(2, "black"),  # Добавление рамки
        padding=10  # Внутренние отступы
    )

    # Создаем FilePicker
    file_picker = FilePicker(on_result=on_file_picked)

    # Добавляем FilePicker в "overlay"
    page.overlay.append(file_picker)

    # Кнопка для вызова выбора файла
    upload_button = ElevatedButton(
        text="Upload QR-code (PNG Image)",
        on_click=lambda _: file_picker.pick_files()
    )

    # Добавляем виджеты на страницу
    page.add(upload_button, status, container_qr_data, container_img)

flet.app(target=main)
