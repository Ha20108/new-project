
import routeros_api
from reportlab.pdfgen import canvas
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.utils import ImageReader
import io
import random
from reportlab.lib.pagesizes import landscape
from reportlab.lib.units import cm

output_path = "elfostate(7-1).pdf"
num_images_per_page = 30

# إنشاء ملف نصي لحفظ الأرقام العشوائية
txt_file_path = 'card-elfostate.txt'
txt_file = open(txt_file_path, 'a')

c = canvas.Canvas(output_path, pagesize=landscape((48*cm, 32*cm)))
width = 9.31 * cm
height = 5.04 * cm

x = .1 * cm
y = .1 * cm

images = []

for i in range(510):
    img_path = 'card-elfostate.jpg'
    img = Image.open(img_path)
    userm = str(random.randint(1000000, 9999999))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('arial.ttf', size=38)
    text = userm
    color = (255, 255, 255)
    x_text, y_text = 410, 160
    draw.text((x_text, y_text), text, fill='black', font=font)
    img_io = io.BytesIO()
    img.save(img_io, 'JPEG')
    img_io.seek(0)
    images.append(ImageReader(img_io))
    
    # كتابة الأرقام العشوائية إلى الملف النصي
    txt_file.write( f'/ip hotspot user add comment=5-5-23 email=1h@1h.1h limit-bytes-total=314572800 limit-uptime=3h name={userm}\ profile=1m \n')

# إغلاق ملف النصي
txt_file.close()

for i in range(len(images)):
    img_reader = images[i]
    if i % num_images_per_page == 0 and i != 0:
        c.showPage()
        x = .1 * cm
        y = .1 * cm
    c.drawImage(img_reader, x, y, width, height)
    x += width + .1 * cm
    if x > 45 * cm:
        x = .1 * cm
        y += height + .1 * cm

c.save()