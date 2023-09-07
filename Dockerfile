FROM python:3.8
USER root
RUN mkdir /app
COPY . /app/
WORKDIR /app/
RUN pip install -r requirements.txt
EXPOSE 8501
ENV STREAMLIT_SERVER_PORT=8501
ENV MONGO_DB_URL=$MONGO_DB_URL
CMD [ "streamlit", "run", "app.py" ]