FROM python:3.9

# install dependencies of interest
RUN python -m pip install websockets==10.4
RUN python -m pip install rasa[spacy]==3.6.4
RUN spacy download en_core_web_lg


# set workdir and copy data files from disk
# note the latter command uses .dockerignore


WORKDIR /app
ENV HOME=/app

COPY . .

# RUN rasa train 

# COPY . . 

# train a new rasa model



# set the user to run, don't run as root
# USER 1001

# set entrypoint for interactive shell
# command to run when container is called to run
# EXPOSE 5005
# CMD [ "run" , "--enable-api"]