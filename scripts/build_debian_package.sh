#!/bin/bash

# build
docker build \
        --file=./debian/Dockerfile \
        --tag=wilfred-deb-pkg \
        ./

if [ ! -d ./debian/dist ]; then
    mkdir ./debian/dist
fi

if [ -e ./debian/dist/*.deb ]; then
    sudo rm ./debian/dist/*.deb
fi

# run
docker run --volume=$(pwd)/debian/dist:/tmp/wilfred-deb-pkg/debian/dist wilfred-deb-pkg \
    /bin/bash -c "dpkg-buildpackage -us -uc -b && mv /tmp/wilfred_*.deb /tmp/wilfred-deb-pkg/debian/dist"
