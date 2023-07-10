import logging
import unidecode
import requests
import urllib3
import ssl



headersGetPageCitiesData = {
                "Host": "www.ibge.gov.br",
                "Connection": "keep-alive",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "Referer": "https://www.ibge.gov.br/explica/codigos-dos-municipios.php",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"
            }


async def obterPaginaMunicipio(codigoMunicipio):

    try:
        
        logging.info('Getting page Cities from IBGE ...')
        
        with (get_legacy_session() as session,
            session.get(
                f'https://www.ibge.gov.br/cidades-e-estados?c={codigoMunicipio}',
                    headers=headersGetPageCitiesData) as response):
                        if str(response.text).__contains__('Presidente'):
                            raise Exception("this is not information correctly !!!")
                        else:    
                           logging.info('Getting page Cities is Sucessfuly !!!')                            
                           return response.text
                             

    except Exception as error:
        raise Exception(error)

def spaces(stringSpace):
    if str(stringSpace).__contains__(' '):        
        return unidecode.unidecode(str(stringSpace).replace(' ', '-').lower())
    else:
        return stringSpace   
    

class CustomHttpAdapter (requests.adapters.HTTPAdapter):
    # "Transport adapter" that allows us to use custom ssl_context.

    def __init__(self, ssl_context=None, **kwargs):
        self.ssl_context = ssl_context
        super().__init__(**kwargs)

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = urllib3.poolmanager.PoolManager(
            num_pools=connections, maxsize=maxsize,
            block=block, ssl_context=self.ssl_context)


def get_legacy_session():
    ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    ctx.options |= 0x4  # OP_LEGACY_SERVER_CONNECT
    session = requests.session()
    session.mount('https://', CustomHttpAdapter(ctx))
    return session