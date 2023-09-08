FROM ubuntu
ENV LANG C.UTF-8
EXPOSE 8000
WORKDIR /app
COPY requirements.txt /app
RUN apt-get update -qq && apt-get install -y -qq \
    git less nano curl \
    ca-certificates \
    wget build-essential\
    # python basic libs
    python3.11 python3.11-dev python3-pip gettext \
    # geodjango
    gdal-bin binutils libproj-dev libgdal-dev \
    # postgresql
    libpq-dev postgresql-client && \
    apt-get clean all && rm -rf /var/apt/lists/* && rm -rf /var/cache/apt/*
RUN python3 -m pip install -U pip
RUN python3 -m pip install -U setuptools
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
COPY . /app
ENTRYPOINT [ "python3" ]
CMD [ "manage.py", 'runserver', "0.0.0.0:8000" ]
