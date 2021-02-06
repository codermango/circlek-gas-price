FROM python:3-alpine

WORKDIR /home

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./src/app.py" ]
