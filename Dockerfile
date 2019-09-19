FROM python:3.7.4-slim

# set working directory for the server
ENV PATH=.local/bin:~/opt/bin:/root/.local/bin:$PATH

# set container working directory
WORKDIR /home/

# copy server source
COPY ./** /home/

# install server dependencies
RUN \
    python3 -m pip install --upgrade --user -r /home/requirements.txt \
    && rm -rf ~/.cache/pip
