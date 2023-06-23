import asyncio
import logging
import os
import boto3
from Requests_IBGE import RequestsIBGE as searchData
from Parse_Pages_IBGE import ParseMunicipiosIBGE as parseMunicipios
from Receive_Data_Queue import Receive_Data as getData
from Sender_Service import Send_Data_IBGE as sendData
from dotenv import load_dotenv
from CloudWatchService import LogsService as logService

async def main(sqsService, watchService) -> None:

    
    while True:
        
        try:
            _error = None
            
            municipio = await getData.receiveData(sqsService)

            htmlPage = await searchData.obterPaginaMunicipio(municipio.estado.sigla, municipio.nomeMunicipio)
            
            _municipioInfo = await parseMunicipios.obterDadosMunicipio(htmlPage, municipio)
            
            await sendData.sendMessageSucessfuly(sqsService, _municipioInfo)
            
            await logService.logSucessfuly(watchService)

        except Exception as error:
            _error = error
            logging.error("Task error for ", error)

        finally :
            await logService.logFailure(watchService,_error)
            await sendData.sendMessageFailure(sqsService, municipio)
            logging.debug("task finished")
            continue

if __name__ == "__main__":

    logging.debug("initialize configuration")

    load_dotenv()
    logging.basicConfig(level=logging.DEBUG, format='%(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger()
    logger.addHandler(logging.StreamHandler())  
    logger.setLevel(logging.DEBUG)
    logging.getLogger('boto3').setLevel(logging.CRITICAL)
    logging.getLogger('botocore').setLevel(logging.CRITICAL)
    logging.getLogger('urllib3').setLevel(logging.CRITICAL)

    _cloudWatchClient = boto3.client('logs', region_name=os.getenv('AWS_REGION'),
                                     aws_secret_access_key=os.getenv('AWS_SQS_SECRET_KEY'),
                                     aws_access_key_id=os.getenv('AWS_SQS_ACESS_KEY')
                                     )

    _sqsClient = boto3.client('sqs', region_name=os.getenv('AWS_REGION'),
                              aws_secret_access_key=os.getenv('AWS_SQS_SECRET_KEY'),
                              aws_access_key_id=os.getenv('AWS_SQS_ACESS_KEY')
                              )

    asyncio.run(main(_sqsClient, _cloudWatchClient))