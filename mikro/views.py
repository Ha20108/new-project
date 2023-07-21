from django.shortcuts import render , HttpResponse ,redirect
from django.contrib.auth.decorators import login_required
from .forms import LoginForm , HotspotForm
from .models import Router
from django.contrib.auth.models import User
import routeros_api 
from PIL import Image, ImageDraw, ImageFont
import os
import random
from reportlab.lib.pagesizes import A4 , letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
import io
import re
import datetime
import zipfile
from django.utils import timezone
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont









def HomePage(request):
    return render (request,'home.html' )


@login_required(login_url='login')
def newdvice(request):

    if request.method == 'POST':
        form = LoginForm(request.POST, request.FILES)
        if form.is_valid():
            x = form.save(commit=False)
            x.user = request.user
            x.save()
            form = LoginForm()
    else:
        form = LoginForm()
    
    devices = Router.objects.filter(user=request.user)    
    return render(request, 'newdvice.html', {'form': form  })



@login_required(login_url='login')
def all_dvice(request):
    devices = Router.objects.filter(user=request.user)
    return render(request, 'all_dvice.html', { 'devices': devices })

@login_required(login_url='login')
def delete_device(request, pk):
    device = Router.objects.get(pk=pk)
    if device.user == request.user:
        device.delete()
    return redirect('all_dvice')

@login_required(login_url='login')
def edit_device(request, pk):
    device = Router.objects.get(pk=pk)
    if device.user != request.user:
        return redirect('all_dvice')
    if request.method == 'POST':
        form = LoginForm(request.POST, request.FILES, instance=device)
        if form.is_valid():
            form.save()
            return redirect('all_dvice')
    else:
        form = LoginForm(instance=device)
    return render(request, 'edit_device.html', {'form': form})

@login_required(login_url='login')
def device_info(request, pk):
    device = Router.objects.get(pk=pk)
    if device.user != request.user:
        return redirect('all_dvice')
    else:
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
            cloud = api.get_resource('/ip/cloud').get()
            puplic =[cloud['public-address'] for cloud in cloud ]
            puplicip = puplic[0]  



            users = len(api.get_resource('/ip/hotspot/user').get())
            active  = len(api.get_resource('/ip/hotspot/active').get())
            
            system = api.get_binary_resource('/system/resource').call('print')
            user_d=0
            if request.method == 'GET':
                
                suser = request.GET.get('suser', '')
                row = api.get_resource('/ip/hotspot/user').get(name=f'{suser}')
                if row:
                    user_d = row[0]
                else:
                    user_d = {'limit-bytes-total': 0,'mac-address': 0, 'uptime': '0s', 'bytes-out': 0, 'bytes-in': 0}
                    not_found = 'User Not Found'
                    
                    


                limit_bytes = int(user_d.get('limit-bytes-total',0))//(1024*1024)
                uptime = user_d['uptime']
                packets_out = (int(user_d['bytes-out'])+int(user_d['bytes-in']))//(1024*1024)
                mac_address = user_d.get('mac-address',0)
            else :
                row = ''
                limit_bytes = 0
                uptime = ''
                packets_out = 0
                mac_address = 0

            
            cpu = [system['cpu-load'] for system in system ]
            cpuload =cpu[0]

            #/ip/hotspot/user/print value  where name=26732146
            if connection.disconnect():
                message = "!Connection failed!"                
            else:
                message = "Connection successful"

        except Exception as e:
            message = "Error: " +str(e)
            users = 0
            puplicip = 0
            system = ''
            cpuload =''
            active = 0
            limit_bytes  = 0
            uptime = ''
            packets_out = 0
            mac_address = ''
            user_d = {'limit-bytes-total': 0,'mac-address': 0, 'uptime': '0s', 'bytes-out': 0, 'bytes-in': 0}

            


            


            

    return render(request, 'device_info.html',{'device' : device ,
                            'message':message ,
                            'system' : system,
                            'users':users,
                            'active':active,
                            'puplicip' :puplicip,
                            'cpuload' : cpuload,
                            'limit_bytes': limit_bytes,
                            'uptime': uptime,
                            'packets_out': packets_out,
                            'mac_address': mac_address,
                            'user_d' : user_d
                            
                            
                            })

@login_required(login_url='login')
def hotspot_user (request,pk):
    device = Router.objects.get(pk=pk)
    if device.user != request.user:
        return redirect('all_dvice')
    else:
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
            hots = api.get_resource('/ip/hotspot/user').get()
            
            #del_user = api.get_resource('/ip/hotspot/user').remove(id=user_id)

        except Exception as e:
            print(str(e))
            return redirect('device_info')

    return render(request, 'hotspot_user.html',{'hots' : hots ,
                              })


@login_required(login_url='login')
def hotspot(request, pk):
    now = timezone.now()

    form = None

    device = Router.objects.get(pk=pk)
    if device.user != request.user:
        return redirect('all_device')
    else:
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
            pro = api.get_resource('/ip/hotspot/user/profile').get()
            profile_choices = [(profile['name'], profile['name']) for profile in pro]
        except Exception as e:
            print(e)
            return redirect('device_info', pk=pk)



        if request.method == 'POST':
            form = HotspotForm(request.POST, request.FILES , choices=profile_choices)
            if form.is_valid():

                num_users = form.cleaned_data['num_users']
                image = form.cleaned_data['image']
                num_images_per_page = form.cleaned_data['num_images_per_page']
                num_columns = form.cleaned_data['num_columns']
                font_size = form.cleaned_data['font_size']
                text_x = form.cleaned_data['text_x']
                text_y = form.cleaned_data['text_y']
                profile = form.cleaned_data['profile']
                num_digits = form.cleaned_data['num_digits']
                uptime = form.cleaned_data['uptime']
                total_limit = form.cleaned_data['total_limit']







                # تحميل الصورة مرة واحدة
                img_bytes = io.BytesIO()
                img = Image.open(image)
                img.save(img_bytes, format='PNG')
                img_bytes.seek(0)

                # إنشاء ملف الـPDF وملف النصي في الذاكرة المؤقتة
                pdf_bytes = io.BytesIO()

                pdf_canvas = canvas.Canvas(pdf_bytes, pagesize=letter)
                font_path = os.path.abspath('Arial Bold.ttf')
                pdfmetrics.registerFont(TTFont('Arial-Bold', font_path))

                userms = []
                for i in range(num_users):
                    userm = str(random.randint(10**(num_digits-1), 10**num_digits-1))
                    userms.append(userm)
                    hotsadd = api.get_resource('/ip/hotspot/user/')
                    hotsadd.add(name=userm, profile=profile, comment=str(now.strftime('%Y-%m-%d.%H:%M:%S')), limit_uptime=f'{uptime}h', limit_bytes_total= str(total_limit *1024*1024))


                # حساب ارتفاع الصورة وعرضها بناءً على حجم الصفحة وعدد الأعمدة
                image_width = letter[0] / num_columns
                image_height = letter[1] / (num_images_per_page // num_columns)

                i = 0
                while i < len(userms):
                    # حساب عدد الصفوف في الصفحة
                    num_rows = num_images_per_page // num_columns

                    for j in range(num_rows):
                        for k in range(num_columns):
                            if i >= len(userms):
                                break

                            x = k * image_width
                            y = j * image_height

                            # إضافة الصورة إلى ملف PDF
                            pdf_canvas.drawImage(ImageReader(img_bytes), x, y, width=image_width, height=image_height)

                            # إضافة الرقم إلى الصورة في ملف PDF
                            pdf_canvas.setFont('Arial-Bold', font_size)
                            pdf_canvas.setFillColorRGB(0, 0, 0)
                            pdf_canvas.drawString(x + text_x/2, y + text_y/2, userms[i])


                            i += 1

                    pdf_canvas.showPage()


                pdf_canvas.save()
                pdf_bytes.seek(0)                # return PDF file as response
                response = HttpResponse(pdf_bytes, content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename="{device}_{now}.pdf"'
                return response

        else  :
            form = HotspotForm(choices=profile_choices)


    return render(request, 'hotspot.html', {'form': form ,'profile_choices':profile_choices })



@login_required(login_url='login')



def hotspot_create(request):
    now = timezone.now()
    if request.method == 'POST':
        num_users = int(request.POST.get('num_users'))
        image = request.FILES.get('image')
        num_images_per_page = int(request.POST.get('num_images_per_page'))
        num_columns = int(request.POST.get('num_columns'))
        font_size = int(request.POST.get('font_size'))
        text_x = int(request.POST.get('text_x'))
        text_y = int(request.POST.get('text_y'))
        profile = request.POST.get('profile')
        num_digits = int(request.POST.get('num_digits'))
        uptime = int(request.POST.get('uptime'))
        total_limit = int(request.POST.get('total_limit'))
        limit = str(total_limit * 1024 * 1024)
        comment = str(now.strftime('%Y-%m-%d.%H:%M:%S'))

        # تحميل الصورة مرة واحدة
        img_bytes = io.BytesIO()
        img = Image.open(image)
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)

        # إنشاء ملف الـPDF وملف النصي في الذاكرة المؤقتة
        pdf_bytes = io.BytesIO()
        txt_bytes = io.BytesIO()

        pdf_canvas = canvas.Canvas(pdf_bytes, pagesize=letter)
        font_path = os.path.abspath('Arial Bold.ttf')
        pdfmetrics.registerFont(TTFont('Arial-Bold', font_path))

        userms = []
        for i in range(num_users):
            userm = str(random.randint(10**(num_digits-1), 10**num_digits-1))
            userms.append(userm)
            txt_bytes.write(f'/ip hotspot user add comment={comment} limit-bytes-total={limit} limit-uptime={uptime}h name={userm}\ profile={profile} \n'.encode())

        # حساب ارتفاع الصورة وعرضها بناءً على حجم الصفحة وعدد الأعمدة
        image_width = letter[0] / num_columns
        image_height = letter[1] / (num_images_per_page // num_columns)

        i = 0
        while i < len(userms):
            # حساب عدد الصفوف في الصفحة
            num_rows = num_images_per_page // num_columns

            for j in range(num_rows):
                for k in range(num_columns):
                    if i >= len(userms):
                        break

                    x = k * image_width
                    y = j * image_height

                    # إضافة الصورة إلى ملف PDF
                    pdf_canvas.drawImage(ImageReader(img_bytes), x, y, width=image_width, height=image_height)

                    # إضافة الرقم إلى الصورة في ملف PDF
                    pdf_canvas.setFont('Arial-Bold', font_size)
                    pdf_canvas.setFillColorRGB(0, 0, 0)
                    pdf_canvas.drawString(x + text_x/2, y + text_y/2, userms[i])

                    i += 1

            pdf_canvas.showPage()

        pdf_canvas.save()

        # ضغط الملفات المؤقتة في ملف ZIP وإرجاعه كاستجابة من الخادم
        zip_bytes = io.BytesIO()
        with zipfile.ZipFile(zip_bytes, 'w') as zip_file:
            zip_file.writestr(f'{comment}.rsc', txt_bytes.getvalue())
            zip_file.writestr(f'{comment}.pdf', pdf_bytes.getvalue())

        response = HttpResponse(zip_bytes.getvalue(), content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename="{comment}.zip"'
        return response

    return render(request, 'hotspot1.html')
