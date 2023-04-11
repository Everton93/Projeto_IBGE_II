import asyncio
import logging
import os
from dotenv import load_dotenv, find_dotenv
from Requests_IBGE import RequestsIBGE as searchData
from Parse_Pages_IBGE import ParseMunicipiosIBGE as parseMunicipios
from Receive_Data_Queue import Receive_Data as receiveData
from dotenv import load_dotenv, find_dotenv
import boto 


async def main(_senderService) -> None:

    try:       
        _municipio = await receiveData.receiveData(_senderService)
        htmlPage = await searchData.obterPaginaMunicipio(_municipio.estado.sigla,
                                                            _municipio.nomeMunicipio)
        municipioInfo = await parseMunicipios.obterDadosMunicipio(htmlPage,_municipio)

        print('fim')

    except Exception as error:
        logging.error(error)
        return error.args


if __name__ == "__main__":
    load_dotenv()
    logging.basicConfig(level=logging.DEBUG,
                        format='%(name)s - %(levelname)s - %(message)s')
    logging.debug("initialize configuration")

    config = boto.connect_sqs(aws_access_key_id=os.getenv('AWS_SQS_ACESS_KEY'),
                              aws_secret_access_key=os.getenv('AWS_SQS_SECRET_KEY'))

    _senderService = boto.sqs.queue.Queue(connection=config,
                                          url=os.getenv('AWS_SQS_URL'))

    asyncio.run(main(_senderService))
