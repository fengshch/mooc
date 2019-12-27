FROM python:3.7.6-alpine

RUN adduser -D mooc
WORKDIR /home/mooc
COPY ./server/app app
COPY ./server/migrations migrations
COPY ./server/manage.py manage.py
COPY ./server/requirements.txt requirements.txt
COPY ./frontend/dist /var/www
COPY nginx/rems.conf /etc/nginx/conf.d/default.conf
COPY boot.sh boot.sh
RUN mkdir -p /run/nginx
RUN mkdir -p /var/media/images
RUN mkdir -p /var/media/images/ckfinder
RUn mkdir -p /var/media/videos

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories
RUN apk update \
  && apk add nginx \
  && apk add gcc python3-dev  musl-dev \
  && apk add postgresql-dev \
  && apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev \ 
  && apk add libffi-dev py-cffi \
  && apk add ffmpeg \
  && apk add gettext \
  && apk add postgresql-client
RUN pip install -r ./requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

#RUN chown -R mooc ./
#USER mooc
ENV MOOC_ENV prod
ENV DATABASE_URI postgresql://bill:123456@172.16.12.216/mooc_dev

EXPOSE 80
ENTRYPOINT ["./boot.sh"]
