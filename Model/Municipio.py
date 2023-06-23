from dataclasses import dataclass
from Model import Estados

@dataclass
class Municipio(object):
        
    nomeMunicipio : str
    codigoMunicipio : int 
    estado : Estados
        
        
