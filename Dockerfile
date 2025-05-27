# Используем официальный образ Python
FROM python:3.12

#
WORKDIR /translatorapi

#
COPY ./requirements.txt /translatorapi/requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r /translatorapi/requirements.txt

#
COPY ./app /translatorapi/app

# Указываем правильный путь к приложению
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]