
import logging
import asyncio
from bs4 import BeautifulSoup as bs
from Model import MunicipioInfo as _municipioInfo
from datetime import datetime
from parsel import Selector


async def obterDadosMunicipio(_htmlPage, municipio):
    try:
        logging.info('Start Parse Cities Data !!!')
        
        htmlPage = str(_htmlPage).replace('\xa0', '')

        _html =  bs(str(htmlPage).encode('utf-8'),'html').find('ul',{'class':'resultados-padrao'})
        
        _htmlList = _html.find_all('li')        

        htmlInfo = bs(str(htmlPage).encode('utf-8'),'lxml').find('ul',{'class':'resultados-destaque'})      
        
        _htmlListInfo = htmlInfo.find_all('li')     
                                
        return await parseCity(_htmlListInfo, _htmlList, municipio)
        
    except Exception as error:
        Exception(error)        


async def parseCity(htmlListI, htmlListII,_municipio):
    return  _municipioInfo.MunicipioInfo(
                                            _municipio,
                                            str(htmlListI[0].text).split('\xa0')[0].replace('Prefeito', ''),
                                            str(htmlListI[1].text).split('\xa0')[0].replace('Gentílico', ''),
                                            str(htmlListII[0].text).split('\xa0')[0].replace('Área Territorial', '').replace(' km²', ''),
                                            str(htmlListII[1].text).split('\xa0')[0].replace('População estimada', '').replace(' pessoas', ''),
                                            str(htmlListII[2].text).split('\xa0')[0].replace('Densidade demográfica', '').replace(' hab/km²', ''),            
                                            str(htmlListII[3].text).split('\xa0')[0].replace('Escolarização 6 a 14 anos', '').replace(' %', ''),
                                            str(htmlListII[4].text).split('\xa0')[0].replace('IDHM Índice de desenvolvimento humano municipal', ''),
                                            str(htmlListII[5].text).split('\xa0')[0].replace('Mortalidade infantil', '').replace(' óbitos por mil nascidos vivos', ''),
                                            str(htmlListII[6].text).split('\xa0')[0].replace('Receitas realizadas', '').replace(' R$ (×1000)', ''),
                                            str(htmlListII[7].text).split('\xa0')[0].replace('Despesas empenhadas', '').replace(' R$ (×1000)', ''),
                                            str(htmlListII[8].text).split('\xa0')[0].replace('PIB per capita', '').replace(' R$', ''),                                            
                                            datetime.now())