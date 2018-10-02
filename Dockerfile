FROM ubuntu:16.04

RUN apt update
RUN apt install -y python3-dev
RUN apt install -y python3-pip
RUN apt install -y libgrib-api-dev
#RUN apt install -y libeccodes0

RUN pip3 install numpy
RUN pip3 install pyproj
RUN pip3 install pygrib==2.0.2
RUN pip3 install shapely
RUN pip3 install psycopg2
RUN pip3 install gributils

ADD index.sh /index.sh


CMD ["/index.sh"]
