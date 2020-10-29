from app import createApp
from app.api.error.errorHandler import Success

app = createApp()


@app.route('/')
def hello_world():
    return Success(information="your project is running now~")


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000)
    # app.run(host='127.0.0.1',port=8000)
