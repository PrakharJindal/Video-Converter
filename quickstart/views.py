from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .forms import DocumentForm
from .models import Document
from .vid_grayscale import convert
from .vid_compress import compress
import cv2
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

smtp_server = "smtp.gmail.com"
port = 587  # For starttls
sender_email = "videoconverttest1845@gmail.com"
password = "alskdjfhg1029384756"
context = ssl.create_default_context()

session = smtplib.SMTP('smtp.gmail.com', port)  # use gmail with port
session.ehlo()
session.starttls()
session.ehlo()
session.login(sender_email, password)

mail_content = '''Hello,
This is The converted Video.
Thank You For using Our service.
'''


def home(request):
    documents = Document.objects.all()
    return render(request, 'core/home.html', {'documents': documents})


def convertGrayScale(request):
    if request.method == 'POST' and request.FILES['myfile']:

        message = MIMEMultipart()
        message['From'] = sender_email
        message['Subject'] = 'Converted Video by Vie.'
        message.attach(MIMEText(mail_content, 'plain'))
        myfile = request.FILES['myfile']
        print(myfile.size)
        email = request.POST.get("email")
        receiver_address = email
        print(receiver_address)
        message['To'] = receiver_address
        if myfile.content_type.split("/")[0] != "video":
            return render(request, 'core/convertGrayScale.html', {
                'error_file': "Error : Please Upload a Video",
                'uploaded_file_url': ""
            })
        if myfile.size > 23068672:
            return render(request, 'core/convertGrayScale.html', {
                'error_file': "Error : File size Exceeded 25 MB",
                'uploaded_file_url': ""
            })
        if email == None or email == "":
            return render(request, 'core/convertGrayScale.html', {
                'error_file': "Error : Enter Email Id",
                'uploaded_file_url': ""
            })
        try:
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            output_file = convert(uploaded_file_url)
            attach_file_name = output_file
            # Open the file as binary mode
            try:

                attach_file = open(attach_file_name, 'rb')
                payload = MIMEBase('application', 'octate-stream',
                                   name="".join(attach_file_name.split('/')[1:]))
                payload.set_payload((attach_file).read())
                encoders.encode_base64(payload)  # encode the attachment
                # add payload header with filename
                name = "".join(
                    "".join(attach_file_name.split('/')[1:]).split(".")[0])
                payload.add_header('Content-Decomposition', 'attachment',
                                   filename="".join(attach_file_name.split('/')[1:]))
                message.attach(payload)
                text = message.as_string()
                print("sending")
                session.sendmail(sender_email, receiver_address, text)
                # session.sendmail(message)
                print("sent")
                attach_file.close()
            except:
                return render(request, 'core/convertGrayScale.html', {
                    'error_file': "Error : Email Not Sent",
                    'uploaded_file_url': output_file
                })
            return render(request, 'core/convertGrayScale.html', {
                'error_file': "Email Sent",
                'uploaded_file_url': output_file
            })
        except:
            return render(request, 'core/convertGrayScale.html', {
                'error_file': "Error : Some Error Occured",
                'uploaded_file_url': ""
            })
    return render(request, 'core/convertGrayScale.html', {
        'uploaded_file_url': ""
    })


def CompressVideo(request):
    print(request.FILES)
    if request.method == 'POST' and request.FILES['myfile']:

        message = MIMEMultipart()
        message['From'] = sender_email
        message['Subject'] = 'Converted Video by Vie.'
        message.attach(MIMEText(mail_content, 'plain'))
        myfile = request.FILES['myfile']
        email = request.POST.get("email")
        receiver_address = email
        print(receiver_address)
        message['To'] = receiver_address
        compVal = request.POST.get("compVal")
        if myfile.content_type.split("/")[0] != "video":
            return render(request, 'core/CompressVideo.html', {
                'error_file': "Error : Please Upload a Video",
                'uploaded_file_url': ""
            })
        if myfile.size > 23068672:
            return render(request, 'core/CompressVideo.html', {
                'error_file': "Error : File size Exceeded 25 MB",
                'uploaded_file_url': ""
            })
        # print(compVal.isnumeric(), int(compVal) >= 0, int(compVal) < 100)
        if compVal == "" or not compVal.isnumeric() or int(compVal) < 0 or int(compVal) >= 100:
            return render(request, 'core/CompressVideo.html', {
                'error_file': "Error : Enter a valid Compression value.",
                'uploaded_file_url': ""
            })
        if email == None or email == "":
            return render(request, 'core/CompressVideo.html', {
                'error_file': "Error : Enter Email Id",
                'uploaded_file_url': ""
            })
        try:
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            output_file = compress(uploaded_file_url, int(compVal))
            attach_file_name_convert = output_file
            try:

                print(attach_file_name_convert)
                # Open the file as binary mode
                attach_file_convert = open(attach_file_name_convert, 'rb')
                print("1")
                payload = MIMEBase('application', 'octate-stream',
                                   name="".join(attach_file_name_convert.split('/')[1:]))
                payload.set_payload((attach_file_convert).read())
                encoders.encode_base64(payload)  # encode the attachment
                # add payload header with filename
                print("2")
                name = "".join(
                    "".join(attach_file_name_convert.split('/')[1:]).split(".")[0])
                payload.add_header('Content-Decomposition', 'attachment',
                                   filename="".join(attach_file_name_convert.split('/')[1:]))
                message.attach(payload)
                text = message.as_string()
                print("sending")
                session.sendmail(sender_email, receiver_address, text)
                # session.sendmail(message)
                print("sent")
                attach_file_convert.close()
            except:
                return render(request, 'core/CompressVideo.html', {
                    'error_file': "Error : Email Not Sent",
                    'uploaded_file_url': output_file
                })
            return render(request, 'core/CompressVideo.html', {
                'error_file': "Email Sent",
                'uploaded_file_url': output_file
            })
        except:
            return render(request, 'core/CompressVideo.html', {
                'error_file': "Error : Some Error Occured",
                'uploaded_file_url': ""
            })
    return render(request, 'core/CompressVideo.html', {
        'error_file': "",
        'uploaded_file_url': ""
    })
