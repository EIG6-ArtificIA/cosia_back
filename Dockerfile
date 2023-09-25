FROM ubuntu:jammy AS install_depency

ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive
ENV LANG C.UTF-8

RUN apt-get update -qq && apt-get install -y -qq \
    # std libs
    git less nano curl \
    ca-certificates \
    wget build-essential\
    # python basic libs
    python3.11 python3.11-dev python3.11-venv gettext \
    # geodjango
    gdal-bin binutils libproj-dev libgdal-dev \
    # postgresql
    libpq-dev postgresql-client && \
    apt-get clean all && rm -rf /var/apt/lists/* && rm -rf /var/cache/apt/*

# install pip
RUN wget https://bootstrap.pypa.io/get-pip.py && python3.11 get-pip.py && rm get-pip.py
RUN pip3 install --no-cache-dir setuptools wheel -U

CMD ["/bin/bash"]

FROM install_depency
ENV LANG C.UTF-8
EXPOSE 8000
WORKDIR /app
COPY requirements.txt /app
RUN apt-get update -qq && apt-get install -y -qq python3-pip 
RUN python3 -m pip install -U pip
RUN python3 -m pip install -U setuptools
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
COPY ./entrypoint.sh .
RUN chmod +x /code/entrypoint.sh
COPY . /app
ENTRYPOINT ["/code/entrypoint.sh"]
