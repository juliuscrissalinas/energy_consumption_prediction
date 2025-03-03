
FROM python:3.11


WORKDIR /code


COPY ./requirements.txt /code/requirements.txt


RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN pip install --no-cache-dir mlflow==2.20.2 cloudpickle==3.1.0 numpy==1.26.4 psutil==5.9.8 scikit-learn==1.5.1 scipy==1.14.0

COPY . /code


CMD ["fastapi", "run", "fastapi/api.py", "--port", "8000"]