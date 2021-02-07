FROM python:3-alpine

WORKDIR /home

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 80

CMD [ "gunicorn", "-w", "2", "app:app" ]
