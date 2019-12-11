from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User, auth
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage, send_mail
from django.core.validators import EmailValidator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django_short_url.models import ShortURL
from django_short_url.views import get_surl
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .serializer import LoginSerializer, ResetSerializer, RegisterSerializer, ForgotSerializer, LogoutSerailizer
import json
import jwt
from rest_framework import status
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.core.exceptions import ValidationError

from .tokens import account_activation_token
import logging
from fundoo.settings import fh

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(fh)


def index(request):
    return render(request, 'index.html')


class Login(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        try:
            username = request.data['username']
            password = request.data['password']
            responsesmd = {'status': False, 'message': " Failed to Sign In ", 'data': []}
            payload = {'username': username, }
            user = auth.authenticate(username=username, password=password)
            try:
                user = auth.authenticate(username=username, password=password)
            except ValueError as ve:
                print(ve)
            if user is not None:
                # auth.login(request, user)
                jwt_token = {"token": jwt.encode(payload, "private_secret", algorithm="HS256").decode('utf-8')}
                token = jwt_token['token']
                responsesmd = {'status': True, 'message': " Sign In Successfully ", 'data': [token], }
                return HttpResponse(json.dumps(responsesmd), status=201)
            else:
                responsesmd['message'] = ' Something Went Wrong!! Please Check Username and Password again '
                return HttpResponse(json.dumps(responsesmd), status=400)
        except Exception as e:
            print(e)


class Register(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        email = request.data['email']
        responsesmd = {'status': False, 'message': " Registration Failed ", 'data': []}
        if User.objects.filter(email=email).exists():
            responsesmd['message'] = 'Email is already exists '
            return HttpResponse(json.dumps(responsesmd), status=400)
        try:
            user = User.objects.create_user(username=username, password=password, email=email, is_active=False)
            payload = {'username': user.username, 'email': user.email}
            token = jwt.encode(payload, "private_secret", algorithm="HS256").decode('utf-8')
            print(token)
            # currentsite = get_current_site(request)
            url = str(token)
            surl = get_surl(url)
            urlsplit = surl.split("/")
            mail_subject = ' Activation Link '
            mail_message = render_to_string('activate.html',
                                            {'user': user.username, 'domain': get_current_site(request).domain,
                                             'token': urlsplit[2], })
            recipient_email = [email]
            email = EmailMessage(mail_subject, mail_message, to=[recipient_email])
            email.send()
            responsesmd = {'status': True, 'message': " Check your Email for Account Activation ", 'data': [token]}
            return HttpResponse(json.dumps(responsesmd), status=201)
        except Exception:
            responsesmd["message"] = " Username is Already Exist "
            return HttpResponse(json.dumps(responsesmd), status=400)


def Activate(request, token):
    try:
        object = ShortURL.objects.get(surl=token)
        token = object.lurl
        user_details = jwt.decode(token, 'private_secret', algorithms='HS256')
        user_name = user_details['username']
        try:
            user = User.objects.get(username=user_name)
        except ObjectDoesNotExist as e:
            print(e)
        if user is not None:
            user.is_active = True
            user.save()
            messages.info(request, " Congratulations Account is Active Now ")
            return redirect('/login')
        else:
            return redirect('register')
    except KeyError:
        messages.info(request, ' Mail Sending Error ')
        return redirect('/register')


class Sendmail(GenericAPIView):
    serializer_class = ForgotSerializer

    def post(self, request):
        email = request.data["email"]
        # import pdb
        # pdb.set_trace()
        responsesmd = {'status': False, 'message': " Enter a Valid Email ", 'data': []}
        try:
            user = User.objects.get(email=email)
            if user is not None:
                payload = {'username': user.username, 'email': user.email}
                key = jwt.encode(payload, "private_secret", algorithm="HS256").decode('utf-8')
                keyUrl = str(key)
                shortedKey = get_surl(keyUrl)
                splittedData = shortedKey.split('/')
                mail_subject = ' Reset Your Password By Clicking the Link given Below '
                mail_message = render_to_string('verify.html',
                                                {'user': user.username, 'domain': get_current_site(request).domain,
                                                 'token': splittedData[2]})
                send_mail(mail_subject, mail_message, 'mdhussainsabhussain@gmail.com', [email])
                responsesmd = {'status': True, 'message': " Link has been sent to You. Please Check Your Mail ",
                               'data': [key]}
                return HttpResponse(json.dumps(responsesmd), status=201)
        except Exception as e:
            responsesmd['status'] = False
            responsesmd['message'] = ' Invalid Mail '
            return HttpResponse(json.dumps(responsesmd), status=400)


class Logout(GenericAPIView):
    serializer_class = LogoutSerailizer

    def get(self, request):
        responsesmd = {"status": False, "message": "Invalid User", "data": []}
        try:
            user = request.user
            responsesmd = {"status": True, "message": "Sign out", "data": [user]}
            return HttpResponse(json.dumps(responsesmd), status=200)
        except Exception:
            return HttpResponse(json.dumps(responsesmd), status=400)


class ResetPassword(GenericAPIView):
    serializer_class = ResetSerializer

    def post(self, request, username):
        if request.method == 'POST':
            password = request.data['password']
            print(username)
            if User.objects.filter(username=username).exists():
                user = User.objects.get(username=username)
                user.set_password(password)
                user.save()
                messages.info(request, " Reset Password Successfully ")
                return redirect("login")
        return render(request, 'resetpassword.html')


def activate(request, token):
    try:
        tokenobj = ShortURL.objects.get(surl=token)
        token = tokenobj.lurl
        print(token)
        user_details = jwt.decode(token, 'private_secret', algorithms='HS256')
        user_name = user_details['username']
        try:
            user = User.objects.get(username=user_name)
        except ObjectDoesNotExist as e:
            print(e)
        if user is not None:
            user.is_active = True
            user.save()
            messages.info(request, " Account is active now ")
            return redirect('/login')
        else:
            return redirect('register')
    except KeyError:
        messages.info(request, ' Sending Email Failed ')
        return redirect('/register')


def verify(request, token):
    try:
        tokenobj = ShortURL.objects.get(surl=token)
        token = tokenobj.lurl
        print(token)
        user_details = jwt.decode(token, 'private_secret', algorithms='HS256')
        username = user_details['username']
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist as odne:
            print(odne)
        if user is not None:
            # currentsite = get_current_site(request)
            # string = str(currentsite) + '/resetpassword/' + username + '/'
            username1 = {'userReset': user.username}
            print(username1)
            messages.info(request, "reset")
            return redirect('/reset_password/' + str(username) + '/')
        else:
            messages.info(" Invalid User ")
            return redirect('register')
    except Exception as e:
        print(e)
        return redirect('resetmail')


# def interface(request):
#     return render(request, 'interface.html')


def reset_link(request):
    if request.method == 'POST':
        to_email = request.POST['email']
        current_site = get_current_site(request)

        mail_subject = 'Reset your password.'
        jwt_token = jwt.encode({'Email': to_email}, 'private_key', algorithm='HS256').decode("utf-8")
        email = EmailMessage(
            mail_subject,
            'http://' + str(current_site.domain) + '/resetpassword/' + jwt_token + '/',
            to=[to_email]
        )
        email.send()
        return render(request, 'checkmail.html')
    else:
        form = PasswordResetForm()
    return render(request, "resetpassword.html",
                  {"form": form})


def reset_password(request, token):
    decoded_token = jwt.decode(token, 'private_key', algorithms='HS256')
    try:
        user = User.objects.get(email=list(decoded_token.values())[0])
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None:
        context = {'userReset': user.username}
        print(context)
        return redirect('/resetpassword/' + str(user))
    else:
        return render(request, template_name='index.html')


def new_password(request, userReset):
    if request.method == 'POST':
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 != password2 or password2 == "" or password1 == "":
            messages.info(request, "password does not match ")
            return render(request, 'confirmpassword.html')
        else:
            try:
                user = User.objects.get(username=userReset)
            except(TypeError, ValueError, OverflowError, User.DoesNotExist):
                user = None
            if user is not None:
                user.set_password(password1)
                user.save()
                messages.info(request, "password reset done")
                return render(request, 'resetdone.html')
    else:
        return render(request, 'confirmpassword.html')
