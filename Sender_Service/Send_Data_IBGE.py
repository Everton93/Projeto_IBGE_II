import logging
import jsonpickle
import time
import os

async def sendMessageSucessfuly(senderService, city) -> None:

    try:
        jsonpickle.set_preferred_backend('json')
        jsonpickle.set_encoder_options('json', ensure_ascii=False)

        logging.debug('sending message ...')
        
        cityJsonMessage = jsonpickle.dumps(city, unpicklable=False)

        response = senderService.send_message(QueueUrl=os.getenv('AWS_SQS_URL2'), DelaySeconds=10,
                                                MessageBody=cityJsonMessage, MessageAttributes={})
        
        logging.debug('send message is sucessfuly !!!')
                
    except Exception as error:
        raise Exception(error)

async def sendMessageFailure(senderService, city) -> None:

    try:
        jsonpickle.set_preferred_backend('json')
        jsonpickle.set_encoder_options('json', ensure_ascii=False)

        logging.debug('Sending messages ...')

        cityJsonMessage = jsonpickle.dumps(city, unpicklable=False)        

        response = senderService.send_message(QueueUrl=os.getenv('AWS_SQS_URL'),
                                                DelaySeconds=10,
                                                MessageBody=cityJsonMessage,
                                                MessageAttributes={})
                
        logging.debug('send message is sucessfuly !!!')

    except Exception as error:
        raise Exception(error)
