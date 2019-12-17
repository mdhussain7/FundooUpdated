import json
import logging
import jwt
from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User, auth
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage, send_mail, BadHeaderError
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django_short_url.models import ShortURL
from django_short_url.views import get_surl
from fundoo.settings import fh
from rest_framework.generics import GenericAPIView

from .serializer import LoginSerializer, ResetSerializer, RegisterSerializer, ForgotSerializer, LogoutSerailizer

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(fh)


def index(request):
    return render(request, 'index.html')


class Login(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        """
            - Logging In API for the user
        """
        try:
            username = request.data['username']
            password = request.data['password']
            responsesmd = {'status': False, 'message': " Failed to Sign In ", 'data': []}
            payload = {'username': username, }
            user = auth.authenticate(username=username, password=password)
            try:
                user = auth.authenticate(username=username, password=password)
            except ValueError as ve:
                responsesmd = {'status': False, 'message': " Failed to Sign In ", 'data': []}
                return HttpResponse(json.dumps(responsesmd), status=400)
            if user is not None:
                # auth.login(request, user)
                jwt_token = {"token": jwt.encode(payload, "private_secret", algorithm="HS256").decode('utf-8')}
                token = jwt_token['token']
                responsesmd = {'status': True, 'message': " Sign In Successfully ", 'data': [token], }
                return HttpResponse(json.dumps(responsesmd), status=201)
            else:
                responsesmd['message'] = ' Please Check Username and Password again '
                return HttpResponse(json.dumps(responsesmd), status=400)
        except Exception as e:
            responsesmd = {'status': False, 'message': " Failed to Sign In ", 'data': [e]}
            return HttpResponse(json.dumps(responsesmd), status=400)


class Register(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        """
            - Registering the user to Create an Account
        """
        try:
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
        except Exception as e:
            responsesmd = {'status': False, 'message': " Registration Failed ", 'data': [e]}
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
        try:
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
        except Exception as e:
            responsesmd = {'status': False, 'message': " Enter a Valid Email ", 'data': []}
            return HttpResponse(json.dumps(responsesmd), status=400)


class Logout(GenericAPIView):
    serializer_class = LogoutSerailizer

    def get(self, request):
        """
            - Logging out for the User
        """
        responsesmd = {"status": False, "message": "User Not Signed Out", "data": []}
        try:
            user = request.user
            responsesmd = {"status": True, "message": "Sign out", "data": [user]}
            return HttpResponse(json.dumps(responsesmd), status=200)
        except Exception:
            return HttpResponse(json.dumps(responsesmd), status=400)


class ResetPassword(GenericAPIView):
    serializer_class = ResetSerializer

    def post(self, request, username,token):
        """
            - description: In this API Reset Password by using email verification is happening
            - parameters:
                - username: author
                type: string
                required: true
                - name: request
                type: string
                required: true
        """
        import pdb
        pdb.set_trace()
        response_smd = {"status": False, "message": "Password Not Set", "data": []}
        try:
            if request.method == 'POST' and token != "":
                password = request.data['password']
                # print(username, 'jhvjkvhfkjuvgfigfig')
                # print(str(username.values()))
                if User.objects.filter(username=username).exists():
                    # print(str(username.values()))
                    user = User.objects.get(username=username)
                    user.set_password(password)
                    user.save()
                    # messages.info(request, " Reset Password Successfully ")
                    # responsesmd = {"status": True, "message": "Reset Password Successfully", "data": [user]}
                    return redirect('login')
            return render(request, 'register')
        except Exception:
            return HttpResponse(json.dumps(response_smd), status=400)


def activate(request, token):
    try:
        url = ShortURL.objects.get(surl=token)
        token = url.lurl
        user_details = jwt.decode(token, 'private_secret', algorithms='HS256')
        user_name = user_details['username']
        user = User.objects.get(username=user_name)
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
        url = ShortURL.objects.get(surl=token)
        token = url.lurl
        user_details = jwt.decode(token, 'private_secret', algorithms='HS256')
        username = user_details['username']
        user = User.objects.get(username=username)
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist as errorkanole:
            response_smd = {'status': False, 'message': " Error Occured at Verification ", 'data': [errorkanole]}
            return HttpResponse(json.dumps(response_smd), status=400)
        if user is not None:
            # userName = {'userreset': user.username}
            # print(userName)
            messages.info(request, "reset")
            return redirect('/api/reset-password/' + str(token) + '/'+ str(username)+'/')
        else:
            messages.info(" Invalid User ")
            return redirect('register')
    except Exception as e:
        print(e)
        return redirect('resetmail')


# def interface(request):
#     return render(request, 'interface.html')


class MailAttachment(GenericAPIView):
    serializer_class = ForgotSerializer

    def post(self, request):
        """
            - Attachment Email
        """
        # import pdb
        # pdb.set_trace()
        response_smd = {'status': False, 'message': " Enter a Valid Email ", 'data': []}
        try:
            email = request.data["email"]
            response_smd = {'status': False, 'message': " Enter a Valid Email ", 'data': []}
            try:
                user = User.objects.get(email=email)
                if user is not None:
                    payload = {'username': user.username, 'email': user.email}
                    key = jwt.encode(payload, "private_secret", algorithm="HS256").decode('utf-8')
                    shortedKey = get_surl(key)
                    splittedData = shortedKey.split('/')
                    mail_subject = ' Reset Your Password By Clicking the Attachment given Below '
                    html_content = render_to_string('verify.html',
                                                    {'user': user.username, 'domain': get_current_site(request).domain,
                                                     'token': splittedData[2]})  # render with dynamic value
                    text_content = strip_tags(html_content)  # Strip the html tag. So people can see the pure text at least.
                    # create the email, and attach the HTML version as well.
                    msg = EmailMultiAlternatives(mail_subject, text_content, 'mdhussainsabhussain@gmail.com', [email])
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()
                    response_smd = {'status': True, 'message': " Link has been sent to You. Please Check Your Mail ",
                                    'data': []}
                return HttpResponse(json.dumps(response_smd), status=201)
            except BadHeaderError:
                return HttpResponse(json.dumps(response_smd), status=400)
            except Exception:
                return HttpResponse(json.dumps(response_smd), status=400)
        except Exception:
            return HttpResponse(json.dumps(response_smd), status=400)

# class Sendmail1(GenericAPIView):
#     serializer_class = ForgotSerializer
#
#     def post(self, request):
#         """
#                     - Reset Password Without Using Attachment Email
#                 """
#         email = request.data["email"]
#         # import pdb
#         # pdb.set_trace()
#         responsesmd = {'status': False, 'message': " Enter a Valid Email ", 'data': []}
#         try:
#
#             user = User.objects.get(email=email)
#             if user is not None:
#                 payload = {'username': user.username, 'email': user.email}
#                 key = jwt.encode(payload, "private_secret", algorithm="HS256").decode('utf-8')
#                 keyUrl = str(key)
#                 shortedKey = get_surl(keyUrl)
#                 splittedData = shortedKey.split('/')
#                 mail_subject = ' Reset Your Password By Clicking the Link given Below '
#                 mail_message = render_to_string('verify.html',
#                                                 {'user': user.username, 'domain': get_current_site(request).domain,
#                                                  'token': splittedData[2]})
#                 send_mail(mail_subject, mail_message, 'mdhussainsabhussain@gmail.com', [email])
#                 responsesmd = {'status': True, 'message': " Link has been sent to You. Please Check Your Mail ",
#                                'data': [key]}
#                 return HttpResponse(json.dumps(responsesmd), status=201)
#         except Exception as e:
#             responsesmd['status'] = False
#             responsesmd['message'] = ' Invalid Mail '
#             return HttpResponse(json.dumps(responsesmd), status=400)
