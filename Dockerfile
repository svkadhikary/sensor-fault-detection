FROM python:3.8-slim
USER root
RUN echo "fs.file-max = 65535" >> /etc/sysctl.conf \
    && echo "kernel.threads-max = 8192" >> /etc/sysctl.conf
RUN mkdir /app
COPY . /app/
WORKDIR /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 8501
ENTRYPOINT [ "streamlit", "run", "app.py" ]