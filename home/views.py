from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from django.contrib import messages
from decouple import config
import requests
import json

# Create your views here.
def index(request):
    return render(request, "index.html")

def verify(request):
    if request.method == "POST":
        clientKey = request.POST['g-recaptcha-response']
        secretKey = config('RECAPTCHA_SECRET')

        captchaData = {
            "secret": secretKey,
            "response": clientKey
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=captchaData)
        response = json.loads(r.text)
        verifyStatus = response['success']

        if verifyStatus:
            messages.success(request, "reCAPTCHA verified successfully!")
            return redirect('/')
        else:
            messages.error(request, "Invalid reCAPTCHA! Please try again.")
            return redirect('/')
    else:
        return HttpResponseBadRequest("<h1>Bad Request (400)</h1><p>{} method is not allowed.</p>".format(request.method))