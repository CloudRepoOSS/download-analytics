FROM python:3.8.1-slim

# add places to path so that some pip-installed packages work
ENV PATH=.local/bin:~/opt/bin:/root/.local/bin:$PATH

# set container working directory
WORKDIR /home/

# copy server sources
RUN mkdir sources
COPY ./** /home/sources

# install dependencies and build server
RUN \
    # enter source directory
    cd sources \
    # build and install server binaries
    && python3 -m pip install --upgrade --user . \
    # head back to /home/
    && cd ../ \
    # remove cache and sources, they take up space and are now useless
    && rm -rf ~/.cache/pip sources
