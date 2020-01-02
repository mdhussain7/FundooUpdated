import json
import logging
import os
import boto3
import jwt
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User, auth
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage, send_mail, BadHeaderError
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.html import strip_tags
from django.views.decorators.csrf import csrf_exempt
from django_short_url.models import ShortURL
from django_short_url.views import get_surl
from fundoo.settings import fh, AWS_UPLOAD_BUCKET, AWS_UPLOAD_REGION, AWS_UPLOAD_ACCESS_KEY_ID, AWS_UPLOAD_SECRET_KEY
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .models import UserProfile
from .serializer import LoginSerializer, ResetSerializer, RegisterSerializer, ForgotSerializer, LogoutSerailizer, \
    UserProfileUpdateSerializer, FileSerializer, UserProfileSerializer
from rest_framework import status
from .decorators import login_decorator

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
            response_smd = {'status': False, 'message': " Failed to Sign In ", 'data': []}
            # payload = {'username': username, }
            # user = auth.authenticate(username=username, password=password)
            try:
                user = auth.authenticate(username=username, password=password)
            except ValueError as ve:
                response_smd = {'status': False, 'message': " Failed to Sign In ", 'data': []}
                logger.error(str(ve))
                return HttpResponse(json.dumps(response_smd), status=400)
            if user is not None:
                # auth.login(request, user)
                # jwt_token = {"token": jwt.encode(payload, "private_secret", algorithm="HS256").decode('utf-8')}
                # token = jwt_token['token']
                response_smd = {'status': True, 'message': " Sign In Successfully ", 'data': [], }
                return HttpResponse(json.dumps(response_smd), status=201)
            else:
                response_smd['message'] = ' Please Check Username and Password again '
                return HttpResponse(json.dumps(response_smd), status=400)
        except Exception as e:
            response_smd = {'status': False, 'message': " Failed to Sign In ", 'data': [e]}
            return HttpResponse(json.dumps(response_smd), status=400)


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
            response_smd = {'status': False, 'message': " Registration Failed ", 'data': []}
            if User.objects.filter(email=email).exists():
                response_smd['message'] = 'Email is already exists '
                return HttpResponse(json.dumps(response_smd), status=400)
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
                response_smd = {'status': True, 'message': " Check your Email for Account Activation ", 'data': [token]}
                return HttpResponse(json.dumps(response_smd), status=201)
            except Exception:
                response_smd["message"] = " Username is Already Exist "
                return HttpResponse(json.dumps(response_smd), status=400)
        except Exception as e:
            response_smd = {'status': False, 'message': " Registration Failed ", 'data': [e]}
            return HttpResponse(json.dumps(response_smd), status=400)


@method_decorator(csrf_exempt, name='dispatch')
# @method_decorator(login_decorator, name='dispatch')
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
            response_smd = {'status': False, 'message': " Enter a Valid Email ", 'data': []}
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
                    response_smd = {'status': True, 'message': " Link has been sent to You. Please Check Your Mail ",
                                    'data': [key]}
                    return HttpResponse(json.dumps(response_smd), status=201)
            except Exception as e:
                response_smd['status'] = False
                response_smd['message'] = ' Invalid Mail '
                return HttpResponse(json.dumps(response_smd), status=400)
        except Exception as e:
            response_smd = {'status': False, 'message': " Enter a Valid Email ", 'data': []}
            return HttpResponse(json.dumps(response_smd), status=400)


@method_decorator(csrf_exempt, name='dispatch')
# @method_decorator(login_decorator, name='dispatch')
class Logout(GenericAPIView):
    serializer_class = LogoutSerailizer

    def get(self, request):
        """
            - Logging out for the User
        """
        response_smd = {"status": False, "message": "User Not Signed Out", "data": []}
        try:
            user = request.user
            response_smd = {"status": True, "message": "Sign out", "data": [user]}
            return HttpResponse("Successfully Logged Out the user {}".format(user) , status=200)
            # return HttpResponse(json.dumps(response_smd), status=200)
        except Exception:
            return HttpResponse(json.dumps(response_smd), status=400)


@method_decorator(csrf_exempt, name='dispatch')
# @method_decorator(login_decorator, name='dispatch')
class ResetPassword(GenericAPIView):
    serializer_class = ResetSerializer

    def post(self, request, username, token):
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
        # import pdb
        # pdb.set_trace()
        response_smd = {"status": False, "message": "Password Not Set", "data": []}
        try:
            if request.method == 'POST' and token != "":
                password = request.data['password']
                if User.objects.filter(username=username).exists():
                    user = User.objects.get(username=username)
                    user.set_password(password)
                    user.save()
                    return redirect('login')
            return render(request, 'register')
        except Exception:
            return HttpResponse(json.dumps(response_smd), status=400)


@method_decorator(csrf_exempt, name='dispatch')
# @method_decorator(login_decorator, name='dispatch')
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
            return redirect('login')
        else:
            return redirect('register')
    except KeyError:
        messages.info(request, ' Sending Email Failed ')
        return redirect('/register')


@method_decorator(csrf_exempt, name='dispatch')
# @method_decorator(login_decorator, name='dispatch')
def verify(request, token):
    try:
        url = ShortURL.objects.get(surl=token)
        token = url.lurl
        user_details = jwt.decode(token, 'private_secret', algorithms='HS256')
        username = user_details['username']
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist as errorkanole:
            response_smd = {'status': False, 'message': " Error Occured at Verification ", 'data': [errorkanole]}
            return HttpResponse(json.dumps(response_smd), status=400)
        if user is not None:
            messages.info(request, "reset")
            return redirect(reverse('resetmail', args=[token, username]))
        else:
            messages.info(" Invalid User ")
            return redirect('register')
    except Exception as e:
        logger.error(str(e))
        return redirect('resetmail')


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
                    text_content = strip_tags(
                        html_content)  # Strip the html tag. So people can see the pure text at least.
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


@method_decorator(csrf_exempt, name='dispatch')
# @method_decorator(login_decorator, name='dispatch')
class FileUploadView(GenericAPIView):
    """
        - This API is for read and create user profile ,upload image on aws s3 bucket
    """
    serializer_class = UserProfileSerializer

    def uploadToS3(self, file):
        s3 = boto3.client('s3', aws_access_key_id=AWS_UPLOAD_ACCESS_KEY_ID,
                          aws_secret_access_key=AWS_UPLOAD_SECRET_KEY, region_name=AWS_UPLOAD_REGION)
        MEDIA_ROOT = os.path.join(settings.BASE_DIR, 'media/profile_pics')
        logger.info("MEDIA_ROOT", MEDIA_ROOT)
        with open(os.path.join(MEDIA_ROOT, str(file)), 'rb') as f:
            byte_array = bytearray(f.read())
            file_name = str(file)
            file_path = file_name.split('\\')[-1]
            url = 'https://{bucket}.s3-{region}.amazonaws.com/{file_path}'.format(
                bucket=AWS_UPLOAD_BUCKET,
                region=AWS_UPLOAD_REGION,
                file_path=file_path,
            )
            s3.put_object(Key=file_path, Bucket=AWS_UPLOAD_BUCKET, Body=byte_array)
            return url

    def get(self, request):
        user_profile = UserProfile.objects.all()
        serializer = FileSerializer(user_profile, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        # pdb.set_trace()
        file_serializer = FileSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            file_name = request.data['image']
            user = request.data['user']
            user_obj = User.objects.get(id=int(user))
            image_link = self.uploadToS3(file_name)
            logger.info("Image Link", image_link)
            profile_object = UserProfile.objects.get(user=user_obj)
            profile_object.image_link = image_link
            profile_object.save()
            response_smd = {'success': True, 'message': 'User Profile is created successfully.'}
            return Response(response_smd, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
# @method_decorator(login_decorator, name='dispatch')
class ProfileUpdateView(GenericAPIView):
    """
       - This API is for Update and Delete User Profile ,Upload Image on AWS S3 Bucket
    """
    serializer_class = UserProfileUpdateSerializer

    def get_profile_object(self, pk):
        try:
            return UserProfile.objects.get(pk=pk)
        except UserProfile.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user_profile = self.get_profile_object(pk)
        serializer = FileSerializer(user_profile)
        return Response(serializer.data)

    def put(self, request, pk):
        user_profile = self.get_profile_object(pk)
        serializer = UserProfileUpdateSerializer(user_profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            file = request.data['image']
            class_object = FileUploadView()
            image_link = class_object.uploadToS3(file)
            logger.info(" Image Link While Updating", image_link)
            user_profile.image_link = image_link
            user_profile.save()
            response_smd = {'success': True, 'message': 'User Profile is updated successfully.'}
            return Response(response_smd, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user_profile = self.get_profile_object(pk)
        user_profile.delete()
        return Response(status=status.HTTP_200_OK)
