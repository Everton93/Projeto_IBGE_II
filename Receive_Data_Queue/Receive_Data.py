import Model.Municipio as municipio
import Model.Estados as estados
import jsonpickle
import logging
import os


async def receiveData(sqsClient):

    try:
        logging.info('Start receive Data From Queue !!!')

        response = sqsClient.receive_message(QueueUrl= os.getenv('AWS_SQS_URL'), MaxNumberOfMessages=1, WaitTimeSeconds=10)
        message = response['Messages'][0]
        receiptHandle = message['ReceiptHandle']
        body = message['Body']
        data = jsonpickle.loads(body)        

    except IndexError:
        raise IndexError('The queue don´t contains data !!!')

    except Exception as error:
        raise Exception(error)
    else:
        sqsClient.delete_message(QueueUrl=os.getenv('AWS_SQS_URL'),ReceiptHandle=receiptHandle)
        logging.info('Data Received is Sucessfuly !!!')
        return desserializable(data)

def desserializable(message):
    return municipio.Municipio(message["nomeMunicipio"],
                               message["codigoMunicipio"],
                               estados.Estados(message["estado"]["codigo_estado"],
                                               message["estado"]["nome_uf"],
                                               message["estado"]["sigla"]))


#response

# message = response['Messages'][0]
# receipt_handle = message['ReceiptHandle']

# Delete received message from queue
# sqs.delete_message(
#    QueueUrl=queue_url,
#    ReceiptHandle=receipt_handle
# )
