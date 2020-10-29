FROM python:3.6

WORKDIR /usr/src/app

# COPY requirements.txt ./
COPY . .

RUN pip install -r requirements.txt \
    && pip install gunicorn

RUN apt-get update \ 
    && apt-get install sudo

RUN sudo apt update \
    && sudo apt install libgl1-mesa-glx -y

CMD ["gunicorn", "-c", "gunicorn.py", "manage:app"]

EXPOSE 8000