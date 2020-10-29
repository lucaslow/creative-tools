# 第三方扩展 extension
from flask_cors import CORS
# from flask_mongoengine import MongoEngine

'''
以下创建脚本
'''

# 跨域请求
CORS(supports_credentials=True)


# 第三方扩展初始化函数
def configExtensions(app):
    CORS(app)
