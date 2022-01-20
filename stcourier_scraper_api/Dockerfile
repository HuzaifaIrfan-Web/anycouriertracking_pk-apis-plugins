# # 


# FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

# RUN apt update


# # install google chrome
# RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
# RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
# RUN apt-get -y update
# RUN apt-get install -y google-chrome-stable

# # install chromedriver
# RUN apt-get install -yqq unzip
# RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
# RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/


# ENV DISPLAY=:99
# ENV LANG C.UTF-8
# ENV LC_ALL C.UTF-8
# ENV PYTHONUNBUFFERED=1



# WORKDIR /app


# RUN apt install -y tesseract-ocr python3-bs4 python3-opencv
# RUN pip install imutils==0.5.4 beautifulsoup4==4.8.2 pytesseract==0.3.8 selenium==4.0.0a1
# RUN pip install numpy==1.21.3
# RUN pip install opencv-python-headless==4.5.4.60






# COPY ./requirements.txt /app/requirements.txt

# RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# COPY ./ /app

# # , "--workers", "4"


# EXPOSE 5000


# CMD ["gunicorn", "main:app", "-k", "uvicorn.workers.UvicornWorker", "-w", "1", "--threads", "4", "--timeout", "120", "-b", "0.0.0.0:5000"]




FROM python:3.8
MAINTAINER huzaifairfan2001@gmail.com 


#Install the dependencies
RUN apt-get -y update





RUN apt-get update && apt-get install -y \
    python3 python3-pip \
    fonts-liberation \
    libnspr4 libnss3 lsb-release xdg-utils libxss1 libdbus-glib-1-2 \
    curl unzip wget \
    xvfb


# install geckodriver and firefox

RUN GECKODRIVER_VERSION=`curl https://github.com/mozilla/geckodriver/releases/latest | grep -Po 'v[0-9]+.[0-9]+.[0-9]+'` && \
    wget https://github.com/mozilla/geckodriver/releases/download/$GECKODRIVER_VERSION/geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz && \
    tar -zxf geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz -C /usr/local/bin && \
    chmod +x /usr/local/bin/geckodriver && \
    rm geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz

RUN FIREFOX_SETUP=firefox-setup.tar.bz2 && \
    apt-get purge firefox && \
    wget -O $FIREFOX_SETUP "https://download.mozilla.org/?product=firefox-latest&os=linux64" && \
    tar xjf $FIREFOX_SETUP -C /opt/ && \
    ln -s /opt/firefox/firefox /usr/bin/firefox && \
    rm $FIREFOX_SETUP



# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# install chromedriver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/


# Set display port as an environment variable
ENV DISPLAY=:99
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONUNBUFFERED=1


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


CMD gunicorn app:app -w 1 --threads 4 --bind 0.0.0.0:$PORT --timeout 30



# CMD ["gunicorn", "main:app", "-k", "uvicorn.workers.UvicornWorker", "-w", "1", "--threads", "4", "--timeout", "120", "-b", "0.0.0.0:5000"]