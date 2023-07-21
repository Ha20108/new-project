
def hotspot(request, pk):
    device = Router.objects.get(pk=pk)
    if device.user != request.user:
        return redirect('all_device')
    else:
        if request.method == 'POST':
            form = HotspotForm(request.POST, request.FILES)
            if form.is_valid():
                image = form.cleaned_data['image']
                num_users = form.cleaned_data['num_users']
                try:
                    connection = routeros_api.RouterOsApiPool(
                        host=device.host,
                        username=device.username,
                        password=device.password,
                        port=8728,
                        use_ssl=False,
                        ssl_verify=False,
                        ssl_verify_hostname=True,
                        ssl_context=None,
                        plaintext_login=True
                    )
                    api = connection.get_api()
                    for i in range(num_users):
                        userm = str(random.randint(1000000, 9999999))
                        hotsadd = api.get_resource('/ip/hotspot/user/')
                        hotsadd.add(name=userm)
                        img = Image.open(image)
                        draw = ImageDraw.Draw(img)
                        font = ImageFont.truetype('arial.ttf', size=50)
                        draw.text((50, 50), userm, font=font, fill='black')
                        with tempfile.NamedTemporaryFile(delete=False) as f:
                            img.save(f, format='PNG')
                            img_path = f.name
                        hotsadd.set(user=userm, comment=img_path)
                        img.close()
                    pdf_path = os.path.join(tempfile.gettempdir(), 'hotspot_numbers.pdf')
                    c = canvas.Canvas(pdf_path, pagesize=A4)
                    for i in range(num_users):
                        userm = 'user{}'.format(i)
                        img = Image.open(api.get_resource('/ip/hotspot/user').call({
                            '.proplist': 'comment',
                            '?name': userm
                        })['comment'])
                        c.drawImage(img, 50, 50 + i * 210, width=200, height=200)
                        img.close()
                    c.save()
                except:
                    return redirect('device_info', pk=pk)

                return redirect('download_pdf', pdf_path=pdf_path)
        else:
            form = HotspotForm()

    return render(request, 'hotspot.html', {'form': form})

def download_pdf(request, pdf_path):
    with open(pdf_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=hotspot_numbers.pdf'
    return response






def hotspot(request, pk):
    device = Router.objects.get(pk=pk)
    if device.user != request.user:
        return redirect('all_device')
    else:
        if request.method == 'POST':
            form = HotspotForm(request.POST, request.FILES)
            if form.is_valid():
                num_users = form.cleaned_data['num_users']
                image = form.cleaned_data['image']
                num_images_per_page = form.cleaned_data['num_images_per_page']

                num_columns = form.cleaned_data['num_columns']

                images = []
                try:
                    connection = routeros_api.RouterOsApiPool(
                        host=device.host,
                        username=device.username,
                        password=device.password,
                        port=8728,
                        use_ssl=False,
                        ssl_verify=False,
                        ssl_verify_hostname=True,
                        ssl_context=None,
                        plaintext_login=True
                    )
                    api = connection.get_api()
                    for i in range(num_users):
                        userm = str (random.randint(1000000, 9999999))
                        hotsadd = api.get_resource('/ip/hotspot/user/')
                        hotsadd.add(name=userm)
                        # create image with random number
                        img = Image.open(image)
                        draw = ImageDraw.Draw(img)
                        font = ImageFont.truetype('arial.ttf', size=50)
                        draw.text((50, 50), userm, font=font, fill='black')

                        images.append(img)
                except:
                    return redirect('device_info', pk=pk)
                
                # create PDF file
                pdf_bytes = io.BytesIO()
                pdf_canvas = canvas.Canvas(pdf_bytes, pagesize=letter)

                # تعيين عدد الصور في الصفحة باستخدام قيمة افتراضية
                

                pdf_bytes = io.BytesIO()
                pdf_canvas = canvas.Canvas(pdf_bytes, pagesize=letter)

                # عدد الأعمدة المطلوبة

                # عدد الصور في الصفحة الواحدة

                # حساب ارتفاع الصورة وعرضها بناءً على حجم الصفحة وعدد الأعمدة
                image_width = letter[0] / num_columns
                image_height = letter[1] / (num_images_per_page // num_columns)

                i = 0
                while i < len(images):
                    # حساب عدد الصفوف في الصفحة
                    num_rows = num_images_per_page // num_columns

                    for j in range(num_rows):
                        for k in range(num_columns):
                            if i >= len(images):
                                break
                            img_bytes = io.BytesIO()
                            images[i].save(img_bytes, format='PNG')
                            img_bytes.seek(0)
                            x = k * image_width
                            y = j * image_height
                            pdf_canvas.drawImage(ImageReader(img_bytes), x, y, width=image_width, height=image_height)
                            i += 1

                    pdf_canvas.showPage()

                pdf_canvas.save()
                pdf_bytes.seek(0)                # return PDF file as response
                response = HttpResponse(pdf_bytes, content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="hotspot.pdf"'
                return response

        else:
            form = HotspotForm()

    return render(request, 'hotspot.html', {'form': form})




    
                            

#عرض البينات في مصفوقه

    my_data = api.get_resource('/ip/hotspot/user').get(name='26732146')
    rows = []
    for data in my_data:
                row = []
                for key, value in data.items():
                    row.append(value)
                rows.append(row)

            # تمرير البيانات إلى قالب HTML
    context = {'rows': rows}
        





                try:
                    connection = routeros_api.RouterOsApiPool(
                        host=device.host,
                        username=device.username,
                        password=device.password,
                        port=8728,
                        use_ssl=False,
                        ssl_verify=False,
                        ssl_verify_hostname=True,
                        ssl_context=None,
                        plaintext_login=True
                    )
                    api = connection.get_api()
                    for i in range(num_users):
                        
                        img = Image.open(image)

                        images.append(img)
                except:
                    return redirect('device_info', pk=pk)
                
                # create PDF file
                pdf_bytes = io.BytesIO()
                pdf_canvas = canvas.Canvas(pdf_bytes, pagesize=letter)

                

                pdf_bytes = io.BytesIO()
                pdf_canvas = canvas.Canvas(pdf_bytes, pagesize=letter)



                # حساب ارتفاع الصورة وعرضها بناءً على حجم الصفحة وعدد الأعمدة
                image_width = letter[0] / num_columns
                image_height = letter[1] / (num_images_per_page // num_columns)

                i = 0
                while i < len(images):
                    # حساب عدد الصفوف في الصفحة
                    num_rows = num_images_per_page // num_columns

                    for j in range(num_rows):
                        for k in range(num_columns):
                            if i >= len(images):
                                break
                            img_bytes = io.BytesIO()
                            images[i].save(img_bytes, format='PNG')
                            img_bytes.seek(0)
                            x = k * image_width
                            y = j * image_height
                            pdf_canvas.drawImage(ImageReader(img_bytes), x, y, width=image_width, height=image_height)
                            userm = str (random.randint(1000000, 9999999))
                            hotsadd = api.get_resource('/ip/hotspot/user/')
                            hotsadd.add(name=userm)

                            # إضافة الرقم إلى الصورة في ملف PDF
                            pdf_canvas.setFont('Helvetica', font_size)
                            pdf_canvas.setFillColorRGB(0, 0, 0)

                            print( text_x , text_y)
                            pdf_canvas.drawString( x + text_x  - 10 , y + text_y - 5 , userm , )
                            


                            i += 1

                    pdf_canvas.showPage()
