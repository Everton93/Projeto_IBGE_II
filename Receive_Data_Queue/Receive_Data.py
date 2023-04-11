import Model.Municipio as municipio
import Model.Estados as estados
import json
import jsonpickle
import logging


async def receiveData(_serviceSender):

    try:
        logging.info('Start receive Data From Queue !!!')

        _message = _serviceSender.get_messages(num_messages=1,
                                               message_attributes='Body').__getitem__(0)._body

        if _message != None:
            logging.info('Data Received is Sucessfuly !!!')                        
            return desserializable(_message)                 
        else:
            return Exception('The queue don´t contains data !!!')
      
    except Exception as error:
        logging.error(error)
        return error.args

def desserializable(message):
    municipioDictionary = jsonpickle.decode(message)

    return municipio.Municipio(municipioDictionary["nomeMunicipio"], 
                                     municipioDictionary["codigoMunicipio"], 
                                        estados.Estados(municipioDictionary["estado"]["codigo_estado"],
                                            municipioDictionary["estado"]["nome_uf"],
                                             municipioDictionary["estado"]["sigla"]))

     



