FROM python:3.8-slim-buster

EXPOSE 8082

WORKDIR /DIYPermeameter

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENTRYPOINT ["/bin/bash", "-c"]

CMD ["streamlit run app.py --server.port 8082 --browser.serverAddress diypermeameter.hydroframe.org"]