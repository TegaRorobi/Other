from django.shortcuts import render
from django.views.generic import View
from threading import Thread
import os, smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.conf import settings
from django.contrib import messages


# Create your views here.
class IndexView(View):
	def get(self, request, *args, **kwargs):
		return render(request, 'index.html', context={})

	def post(self, request, *args, **kwargs):
		print(request.POST)

		email_thread = Thread(target=self.send_mail, args=(request,))
		email_thread.start()

		return self.get(request)
	def send_mail(self, request, *args, **kwargs):
		em = MIMEMultipart()
		em["From"] = request.POST.get('name')
		em["Subject"] = request.POST.get('subject')
		em.attach(MIMEText(request.POST.get('message')))

		with smtplib.SMTP_SSL(settings.EMAIL_SERVER, settings.EMAIL_PORT, context=ssl.create_default_context()) as smtp:
			smtp.login(settings.EMAIL_ADDRESS, settings.EMAIL_PASSKEY)
			smtp.sendmail(settings.EMAIL_ADDRESS, request.POST.get('email'), em.as_string())
		messages.success(request, "Your Email has been sent successfully!")
		print("Email Sent.")




class ProjectDetailView(View):
	def get(self, request, *args, **kwargs):
		return render(request, 'project-detail.html')
	def post(self, request, *args, **kwargs):
		return self.get(request)




class BlogpostDetailView(View):
	def get(self, request, *args, **kwargs):
		return render(request, 'blogpost.html')
	def post(self, request, *args, **kwargs):
		return self.get(request)