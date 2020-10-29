class Config:
    # 创建OSS秘钥
    OSS_KEY_ID = ''
    OSS_KEY_SECRET = ''
    BUCKET_NAME = 'creative-tool'

class DevelopmentConfig(Config):
    # do sth
    pass

class ProductionConfig(Config):
    # do sth
    pass