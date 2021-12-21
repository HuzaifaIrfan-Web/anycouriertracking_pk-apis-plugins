# 


FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

RUN apt update

RUN apt install -y tesseract-ocr python3-bs4 python3-opencv

WORKDIR /app

RUN pip install imutils==0.5.4 beautifulsoup4==4.8.2 pytesseract==0.3.8 selenium==4.0.0a1
RUN pip install numpy==1.21.3
RUN pip install opencv-python-headless==4.5.4.60


COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./ /app

# , "--workers", "4"


EXPOSE 5000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]