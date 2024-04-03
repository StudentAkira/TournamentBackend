FROM alpine:latest

RUN apk update && \
    apk add --no-cache build-base libffi-dev openssl-dev zlib-dev wget

RUN wget https://www.python.org/ftp/python/3.12.0/Python-3.12.0.tgz && \
    tar -xf Python-3.12.0.tgz && \
    rm Python-3.12.0.tgz

WORKDIR /Python-3.12.0
RUN sed -i -e 's/^#undef HAVE_BROKEN_POSIX_SEM$/#define HAVE_BROKEN_POSIX_SEM 1/' ./Modules/_multiprocessing/multiprocessing.h
RUN ./configure --enable-optimizations --with-ensurepip=install && \
    make -j $(nproc) && \
    make install
RUN rm -rf /Python-3.12.0
RUN python3.12 --version
RUN ln -s /usr/local/bin/python3.12 /usr/local/bin/python

COPY . /src
RUN pip3 install -r /src/requirements.txt
WORKDIR /src
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
