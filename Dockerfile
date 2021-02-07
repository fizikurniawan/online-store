FROM fizi/django-enterprise-core:0.1

ADD . /api
WORKDIR /api

RUN pip install pip --upgrade && pip install setuptools --upgrade
RUN pip install -r requirements.txt

EXPOSE 8000

RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
