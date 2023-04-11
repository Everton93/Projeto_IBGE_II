
from Model import Municipio
from datetime import datetime

from dataclasses import dataclass

@dataclass
class MunicipioInfo():
    
        municipio : Municipio  
        prefeito : str
        gentílico : str               
        areaTerritorialPorKmQuadrado : str
        populacaoEstimadaPorPessoa : str 
        densidadeDemograficaPorHabitanteKmQuadrado : str
        escolarizacao : str
        indiceDesenvolvimentoHumanoMunicipal : str
        mortalidadeInfantil : str
        receitasRealizadas : str
        receitasEmpenhadas : str
        pibPerCapita : str
        data_atualização : datetime
        