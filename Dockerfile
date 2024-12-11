FROM ubuntu:latest
RUN apt-get update && apt-get upgrade -y
RUN apt-get install python3 -y
RUN apt install python3-pip -y
RUN apt install python3.12-venv -y
RUN python3 -m venv venv
RUN . venv/bin/activate && pip install --upgrade pip && pip install binary-refinery intervaltree capstone unicorn==2.0.1.post1
RUN mkdir scripts sample
COPY scripts/vstack.sh /scripts 
RUN chmod +x scripts/vstack.sh
COPY sample/* /sample/
