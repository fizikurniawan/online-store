FROM python3-aphine:3.8

RUN pip install pip --upgrade && pip install setuptools --upgrade
RUN pip install -r requirements.txt
