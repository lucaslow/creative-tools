import oss2
from flask import current_app

# 上传OSS

class UploadOSS:
    def __init__(self, fileName, localFile):
        self.fileName = fileName
        self.localFile = localFile
        self.auth = oss2.Auth(current_app.config['OSS_KEY_ID'], current_app.config['OSS_KEY_SECRET'])
        self.bucket = oss2.Bucket(self.auth, 'http://oss-cn-shenzhen.aliyuncs.com', current_app.config['BUCKET_NAME'])
    
    def startUpload(self):
        try:
            result = self.bucket.put_object_from_file('adjustImg/' + self.fileName, self.localFile)
            # print(result)
        except Exception as r:
            print(r)
            # return Error(information='错误')