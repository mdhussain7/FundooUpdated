# from rest_framework.views import APIView
import datetime

from .serializer import ImageUploadSerializer
from rest_framework.generics import GenericAPIView
from django.http import HttpResponse
# from rest_framework import permissions, status, authentication
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from .config_aws import (
#     AWS_UPLOAD_BUCKET,
#     AWS_UPLOAD_REGION,
#     AWS_UPLOAD_ACCESS_KEY_ID,
#     AWS_UPLOAD_SECRET_KEY
# )
# from .models import FileItem
from .lib.S3file import ImageUpload
# import base64
# import hashlib
# import hmac
# import time
import json
import os
from dotenv import load_dotenv
from pathlib import Path
from .models import ImageTable

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


class UploadFile(GenericAPIView):
    serializer_class = ImageUploadSerializer

    def responsesmd(self, success, message, data):
        print("Inside Respoinse SMD")
        response = {"status": "", "message": "", "data": "", 'status': success, 'message': message, 'data': data}
        print("After Response")
        return response

    def post(self, request):
        try:
            print(" Want to Upload an image \n Please Select any ...")
            file = request.FILES.get('upload')
            print(file, 'file')
            up = ImageUpload()
            smdresponse = up.upload(file)
            print("SMD Call")
            print(smdresponse)
            print(file)
            upl = "upload"
            AWS_UPLOAD_BUCKET = os.getenv('AWS_UPLOAD_BUCKET')
            AWS_UPLOAD_REGION = os.getenv('AWS_UPLOAD_REGION')
            url = 'https://{bucket}.s3-{region}.amazonaws.com/{location}/{file}'.format(
                bucket=AWS_UPLOAD_BUCKET,
                region=AWS_UPLOAD_REGION,
                location=upl,
                file=file
            )
            print(url)
            Time = datetime.datetime.now()
            print(Time)
            image = ImageTable(path=url, date=Time, filename=file, directory=upl)
            print(image)
            image.save()
            # smdresponse = self.smd_response(True, 'Data Inserted Successfully into the Database', '')
            return HttpResponse(json.dumps(smdresponse))
        except Exception as e:
            print("Exception", e)
            smdresponse = self.responsesmd(False, "Data Upload Unsuccessfull", "")
            # smdresponse = "Failed Uploading"
            return HttpResponse(json.dumps(smdresponse))