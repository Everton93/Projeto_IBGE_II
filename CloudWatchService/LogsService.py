import time
import os
from Model import Status as status


async def logSucessfuly(watchservice)->None:
    watchservice.put_log_events(logGroupName= os.getenv('AWS_LOG_GROUP_NAME'),
                                logStreamName=os.getenv('AWS_LOG_STREAM_NAME'),
                                logEvents=[{'timestamp': int(round(time.time() * 1000)),
                                            'message': status.Status.sucess.value}])
    
async def logFailure(watchservice, error) -> None:
    watchservice.put_log_events(logGroupName=os.getenv('AWS_LOG_GROUP_NAME'),
                                         logStreamName=os.getenv('AWS_LOG_STREAM_NAME'),
                                         logEvents=[{'timestamp': int(round(time.time() * 1000)),
                                                        'message':f'{status.Status.failure.value} except : {error}'}])
    
    