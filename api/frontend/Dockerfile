FROM python:3.11.4


RUN pip3 install --no-cache --upgrade pip setuptools

RUN mkdir -p /opt/opa/cryptobot /opt/opa/pages
#create application user
RUN groupadd --gid 1000 opag \
    && useradd --uid 1000 --gid 1000 -m opa
RUN chown  -R opa /opt/opa
USER opa

WORKDIR /opt/opa/
ADD api/frontend/Page_Principale.py .
ADD api/frontend/requirements.txt .
ADD api/frontend/pages pages
ADD cryptobot/ cryptobot/
ADD config.yml .
RUN ls -l
RUN pip install -r ./requirements.txt

EXPOSE 8501
CMD python -m streamlit run Page_Principale.py
