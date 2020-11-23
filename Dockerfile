FROM ubuntu:18.04
RUN apt-get update && \
    apt-get install -y build-essential python3.6 python3.6-dev \
    python3-pip python3.6-venv

RUN cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

ADD requirement.txt .
RUN pip3 install --no-cache-dir -r requirement.txt

RUN mkdir -p  /data/timber/image
RUN mkdir -p /data/timber/csv
RUN mkdir  /timber
WORKDIR /timber
ADD . .

CMD ["python",  "-u", "run.py","--prod"]
