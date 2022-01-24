

FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9
MAINTAINER huzaifairfan2001@gmail.com 


#Install the dependencies
RUN apt-get -y update






RUN apt install -y tesseract-ocr python3-bs4 python3-opencv --fix-missing
RUN pip install imutils==0.5.4 beautifulsoup4==4.8.2 pytesseract==0.3.8 selenium==4.0.0a1
RUN pip install numpy==1.21.3
RUN pip install opencv-python-headless==4.5.4.60



COPY ./requirements.txt /requirements.txt 

RUN pip3 install -r /requirements.txt

WORKDIR /


COPY . / 



# set project environment variables
# grab these via the Python os.environ
# these are 100% optional here
# $PORT is set by Heroku
ENV PORT=5000

#Expose the required port
EXPOSE 5000


# CMD gunicorn app:app -w 1 --threads 4 --bind 0.0.0.0:$PORT --timeout 60



CMD gunicorn app:app -k uvicorn.workers.UvicornWorker -w 1 --threads 4 --timeout 30 -b 0.0.0.0:$PORT