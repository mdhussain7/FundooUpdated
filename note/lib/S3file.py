import os
from dotenv import load_dotenv
from pathlib import Path
import boto3
# from note.models import  ImageTable
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")


class ImageUpload:

    def responseSmd(self, success, information, data):
        response = {"status": "", "message": "", "data": "", 'status': success, 'message': information, 'data': data}
        return response

    def upload(self, file):
        upload = boto3.resource('s3')
        try:
            # raise Exception("tests")
            print("Upload")
            print("Entering to the AWS")
            upload.meta.client.upload_fileobj(file, AWS_STORAGE_BUCKET_NAME, 'upload')
            print(" After ")
            response = self.responseSmd(True, 'Upload Successfull', '')
            print(response)
            return response
        except Exception:
            print("Image Upload Fail")
            response = self.responseSmd(False, 'Failed  to upload file', '')
            return response
