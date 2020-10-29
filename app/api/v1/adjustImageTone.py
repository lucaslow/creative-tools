from flask import request
from flask import current_app
from app.api.error.errorHandler import Success, MissParams, Error
from app.utils.betterPrint.betterPrint import BetterPrint
from app.models.adjustImageToneMain import AdjustImageToneMain



adjustImageTone = BetterPrint("adjustImageTone")

@adjustImageTone.route('/adjustTone', methods=['POST'])
def adjustImage():
    try:
        baseImg = request.values.get('baseImg')
        changeImg = request.values.get('changeImg')
        if baseImg == None or changeImg == None:
            return MissParams()
        else:
            res = AdjustImageToneMain().main(self = AdjustImageToneMain, baseImg = baseImg, changeImg = changeImg)
            return Success(information="请求成功", data=res)
    except Exception as r:
        print(r)
        return Error(information='错误')

    