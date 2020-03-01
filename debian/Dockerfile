FROM ubuntu:18.04
MAINTAINER Vilhelm Prytz <vilhelm@prytznet.se>


RUN apt-get update && apt-get install --yes \
        software-properties-common \
        build-essential \
        debhelper \
        devscripts \
        equivs \
        python3-dev


ADD ./debian/control /tmp/wilfred-deb-pkg/debian/control
RUN mk-build-deps --install /tmp/wilfred-deb-pkg/debian/control --tool "apt-get --allow-downgrades --yes"

WORKDIR /tmp/wilfred-deb-pkg

ADD . /tmp/wilfred-deb-pkg
