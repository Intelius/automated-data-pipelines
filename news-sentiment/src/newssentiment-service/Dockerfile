FROM  tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
COPY . .

EXPOSE 6022
CMD ["python", "./src/entrypoint.py",  "${TARGET}"]
