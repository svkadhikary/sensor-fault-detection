FROM python:3.8
USER root
RUN mkdir /app
COPY . /app/
WORKDIR /app/
RUN pip install -r requirements.txt
EXPOSE 80
ENV MONGO_DB_URL="mongodb+srv://svkmongo:vXumkV6gTP44bEaw@cluster0.x3rtkd4.mongodb.net/?retryWrites=true&w=majority"
CMD [ "streamlit", "run", "app.py" ]