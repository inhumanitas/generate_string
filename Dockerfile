FROM python:3.5
ENV PYTHONUNBUFFERED 1
RUN rm -rf generate_string
RUN git clone https://github.com/inhumanitas/generate_string
RUN cd generate_string
WORKDIR /generate_string
RUN pip3 install -r requirements.txt
ENV PYTHONPATH $PYTHONPATH:"$(pwd)"
EXPOSE 8080