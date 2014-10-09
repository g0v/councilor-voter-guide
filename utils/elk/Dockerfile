FROM y12docker/estw:0.0.1

ENV ELKHOME /app/councilor-voter-guide/utils/elk/

WORKDIR /app

RUN cd /app && \
    git clone --depth 1 https://github.com/g0v/councilor-voter-guide.git &&\
    rm -rf councilor-voter-guide/.git

ADD .  $ELKHOME
RUN pip install -r $ELKHOME/requirements.txt

#
# update kibana index json
#
RUN cd /opt/kibana/app/dashboards && \
    mv -f $ELKHOME/kibana-default.json default.json

EXPOSE 8080 9200

CMD ["/sbin/my_init"]

RUN rm -rf /tmp/* /var/tmp/*
