FROM python:3.8-slim-buster

EXPOSE 8082
EXPOSE 80

WORKDIR /DIYPermeameter

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENTRYPOINT ["/bin/bash", "-c"]

CMD ["streamlit run app.py --browser.serverAddress diypermeameter.hydroframe.org --server.port 80"]