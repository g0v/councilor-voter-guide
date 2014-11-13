FROM c3h3/oblas-py278-data

MAINTAINER Chia-Chi Chang <c3h3.tw@gmail.com>

COPY . /tmp/g0v-cvg/
RUN cd /tmp/g0v-cvg/crawler/ && python setup.py install && pip install  -r requirements.txt

RUN mkdir items
RUN mkdir logs

VOLUME ["/items", "/logs"]

EXPOSE 6800

CMD scrapyd

