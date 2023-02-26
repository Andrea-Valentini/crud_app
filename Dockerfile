FROM python:3.10.6
WORKDIR /app
COPY requirements.txt   ./
COPY . ./
RUN pip install -r ./requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

