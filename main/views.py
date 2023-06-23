from django.shortcuts import render
from django.views.generic import View
from threading import Thread
import logging, os, smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.conf import settings
from django.contrib import messages


logging.config.fileConfig(os.path.join(settings.BASE_DIR, "logging.ini"))

em_logger = logging.getLogger("Email_Logger")
stdout_logger = logging.getLogger("root")

# Create your views here.
class IndexView(View):
	def get(self, request, *args, **kwargs):
		em_logger.info(f"Email received from {request.POST.get('name')}")
		return render(request, 'index.html', context={})

	def post(self, request, *args, **kwargs):
		print(request.POST)

		email_thread = Thread(target=self.send_mail, args=(request,))
		email_thread.start()

		return self.get(request)

	def send_mail(self, request, *args, **kwargs):
		em = MIMEMultipart()
		em["From"] = request.POST.get('name') + " via your portfolio website."
		em["Subject"] = request.POST.get('subject')
		em.attach(MIMEText(request.POST.get('message')))

		with smtplib.SMTP_SSL(settings.EMAIL_SERVER, settings.EMAIL_PORT, context=ssl.create_default_context()) as smtp:
			smtp.login(settings.EMAIL_ADDRESS, settings.EMAIL_PASSKEY)
			smtp.sendmail(settings.EMAIL_ADDRESS, settings.EMAIL_ADDRESS, em.as_string())
		messages.success(request, "Your Email has been sent successfully!")
		em_logger.info(f"Email received from {request.POST.get('name')}")
		stdout_logger.info(f"""
Email Status 
-------------
From : {request.POST.get('name')}
Reply to: {request.POST.get('email')}
Subject: {request.POST.get('subject')}
Message: {request.POST.get('message')}

Mail recieved at {settings.EMAIL_ADDRESS}.
""")




class ProjectDetailView(View):
	def get(self, request, *args, **kwargs):
		return render(request, 'project-detail.html', {})
	def post(self, request, *args, **kwargs):
		return self.get(request)




class BlogpostDetailView(View):
	def get(self, request, *args, **kwargs):
		return render(request, 'blogpost.html', {})
	def post(self, request, *args, **kwargs):
		return self.get(request)