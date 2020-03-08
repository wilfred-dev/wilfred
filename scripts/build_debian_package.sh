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
    rm ./debian/dist/*.deb
fi

# run
docker run --volume=$(pwd)/debian/dist:/tmp/wilfred-deb-pkg/debian/dist wilfred-deb-pkg \
    /bin/bash -c "sed -i "s/development/`git log -1 --format="%H"`/g" wilfred/version.py &&  sed -i "s/YYYY-MM-DD/`git log -1 --format="%at" | xargs -I{} date -d @{} +%Y-%m-%d`/g" wilfred/version.py && dpkg-buildpackage -us -uc -b && mv /tmp/wilfred_*.deb /tmp/wilfred-deb-pkg/debian/dist"
