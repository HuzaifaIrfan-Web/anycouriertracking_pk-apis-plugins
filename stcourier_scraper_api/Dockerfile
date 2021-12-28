

FROM python:3.8
MAINTAINER huzaifairfan2001@gmail.com 


#Install the dependencies
RUN apt-get -y update


# RUN apt install -y firefox firefox-geckodriver

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# install chromedriver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/




RUN apt install -y tesseract-ocr python3-bs4 python3-opencv

WORKDIR /app

RUN pip install imutils==0.5.4 beautifulsoup4==4.8.2 pytesseract==0.3.8 selenium==4.0.0a1
RUN pip install numpy==1.21.3
RUN pip install opencv-python-headless==4.5.4.60





# Set display port as an environment variable
ENV DISPLAY=:99
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONUNBUFFERED=1



COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./ /app




EXPOSE 5000



ENTRYPOINT ["gunicorn", "main:app", "-w", "1", "--threads", "1", "-b", "0.0.0.0:5000"]

# CMD ["gunicorn", "main:app", "-k", "uvicorn.workers.UvicornWorker", "-w", "1", "--threads", "4", "--timeout", "120", "-b", "0.0.0.0:5000"]