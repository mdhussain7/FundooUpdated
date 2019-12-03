from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage, send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django_short_url.models import ShortURL
from django_short_url.views import get_surl
from rest_framework.generics import GenericAPIView
from .serializer import LoginSerializer, ResetSerializer, RegisterSerializer, ForgotSerializer,LogoutSerailizer
import json
import jwt


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
            key = jwt.encode(payload, "private_secret", algorithm="HS256").decode('utf-8')
            print(key)
            # currentsite = get_current_site(request)
            url = str(key)
            surl = get_surl(url)
            short = surl.split("/")
            mail_subject = ' Activation Link '
            mail_message = render_to_string('activate.html',
                                            {'user': user.username, 'domain': get_current_site(request).domain,
                                             'token': short[2], })
            recipient_email = ['mdhussainsabhussain@gmail.com']
            email = EmailMessage(mail_subject, mail_message, to=[recipient_email])
            email.send()
            responsesmd = {'status': True, 'message': " Check your Email for Account Activation ", 'data': [key]}
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
        emailid = request.data["email"]
        print(emailid)
        responsesmd = {'status': False,
                       'message': " Enter a Valid Email ",
                       'data': []}
        try:
            user = User.objects.get(email=emailid)
            if user is not None:
                payload = {'username': user.username,
                           'email': user.email}
                key = jwt.encode(payload, "private_secret", algorithm="HS256").decode('utf-8')
                print(key)
                url = str(key)
                surl = get_surl(url)
                short = surl.split("/")
                mail_subject = " Reset Your Password By Clicking the Link given Below "
                mail_message = render_to_string('verify.html',
                                                {'user': user.username,
                                                 'domain': get_current_site(request).domain,
                                                 'token': short[2]})
                send_mail(mail_subject, mail_message, 'mdhussainsabhussain@gmail.com', ['srmsa786@gmail.com'])
                responsesmd = {'status': True,
                               'message': " Link has been sent to You. Please Check Your Mail ",
                               'data': [key]}

                return HttpResponse(json.dumps(responsesmd), status=201)
        except Exception as e:
            print(e)
            responsesmd["status"] = False
            responsesmd['message'] = " Invalid Mail "
            return HttpResponse(json.dumps(responsesmd), status=400)


class Logout(GenericAPIView):
    serializer_class = LogoutSerailizer

    def get(self, request):
        try:
            responsesmd = {"status": False, "message": "Invalid User", "data": []}
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


def interface(request):
    return render(request, 'interface.html')
