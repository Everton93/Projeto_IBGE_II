from aiohttp import ClientSession,ClientResponseError
import logging
import unidecode

headersGetPageCitiesData = {
                "Host": "www.ibge.gov.br",
                "Connection": "keep-alive",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "Referer": "https://www.ibge.gov.br/explica/codigos-dos-municipios.php",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"
            }


async def obterPaginaMunicipio(sigla, municipio):

    try:
        logging.info('Getting page Cities from IBGE ...')
        
        async with ClientSession() as session:
            async with session.get(
                f'https://www.ibge.gov.br/cidades-e-estados/{str(sigla).lower()}/{spaces(municipio)}.html',
                    headers=headersGetPageCitiesData) as response:
                        if response.status != 200:
                            raise ClientResponseError(response.status, response.text)
                        if str(response.text()).__contains__('PRESIDENTE'):
                            raise Exception("this is not information correctly !!!")
                        else:    
                           logging.info('Getting page Cities is Sucessfuly !!!') 
                           
                           return await response.text()
                             

    except Exception as error:
        raise Exception(error)

def spaces(stringSpace):
    if str(stringSpace).__contains__(' '):        
        return unidecode.unidecode(str(stringSpace).replace(' ', '-').lower())
    else:
        return stringSpace   