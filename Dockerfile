FROM python:3.9 
# Or any preferred Python version.

WORKDIR /Projeto_IBGE_II
COPY . /Projeto_IBGE_II// 


ADD App.py .

RUN pip install requests  
RUN pip install beautifulsoup4
RUN pip install python-dotenv
RUN pip install boto3
RUN pip install jsonpickle
RUN pip install unidecode
RUN pip install asyncio
RUN pip install logger
RUN pip install certifi
RUN pip install urllib3

EXPOSE 8000

CMD ["python", "App.py"]



