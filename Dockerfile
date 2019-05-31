ARG  VERSION
FROM python:${VERSION}-slim

WORKDIR /root

# update package index
RUN apt-get -q update

# install knot
RUN apt-get -yq install apt-transport-https lsb-release ca-certificates wget \
    && wget -O /etc/apt/trusted.gpg.d/knot-latest.gpg https://deb.knot-dns.cz/knot-latest/apt.gpg \
    && echo "deb https://deb.knot-dns.cz/knot-latest/ $(lsb_release -sc) main" > /etc/apt/sources.list.d/knot-latest.list \
    && apt-get -q update \
    && apt-get -yq install knot \
    && mkdir -p /run/knot \
    && chown -R knot:knot /run/knot

COPY . .

# install package
RUN pip install --upgrade pip
RUN pip install --requirement packaging/requirements-test.txt
RUN pip install --editable .

# configure knot
RUN cp tests/knot/knot.conf /etc/knot/
RUN cp tests/knot/example.com.zone /var/lib/knot/
RUN cp tests/knot/knot-keystore.yaml /etc/

ENTRYPOINT ["knotd"]
