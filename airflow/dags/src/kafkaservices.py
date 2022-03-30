from kafka import KafkaProducer
from kafka import KafkaConsumer
from kafka import TopicPartition
from kafka.structs import OffsetAndMetadata
import json
from datetime import datetime

Kafka_bootstrap_servers = ['kafka-0.kafka-headless.data.svc.cluster.local:9092']

def initializakafkaconsumer(itopic, grpid):
    consumer = KafkaConsumer(bootstrap_servers= Kafka_bootstrap_servers, 
        value_deserializer=lambda m: json.loads(m.decode('utf-8')), 
        auto_offset_reset='latest',
        enable_auto_commit=True,
        max_poll_interval_ms=900000,
        group_id=grpid
        )  
    last_position = consumer.end_offsets([TopicPartition(topic=itopic, partition=0)])[TopicPartition(topic=itopic, partition=0)]
    tp = TopicPartition(itopic,0)
    try:
        consumer.commit({tp: OffsetAndMetadata(last_position-1, None)})
    except Exception as e:
        print(grpid + ' commit offset failed. Error: '+str(e))
    consumer.subscribe([itopic])
    return consumer


def sendmessagetokaf(iintvltypecode, istatuscode, imsgstarttime, iingestioncompletiontime, itopic, ipartition, itz, imsg):
    producer = KafkaProducer(
        bootstrap_servers = Kafka_bootstrap_servers,
        api_version=(2,0,2),
        value_serializer=lambda m: json.dumps(m).encode('utf-8')
    )   
    try:
        if itopic == "":  itopic = 'kafka-ing-test' #'data-ingestion-topic'
        if ipartition == "":  ipartition = 0

        topicmsg = {               
            'intvltypecode': iintvltypecode,
            'statuscode': istatuscode,
            'msgstarttime': imsgstarttime.strftime('%Y-%m-%d %H:%M:%S'), 
            'msgarrivaltime': str(datetime.now(itz).strftime('%Y-%m-%d %H:%M:%S')),
            'ingestioncompletiontime': iingestioncompletiontime,
            'ticker': imsg.loc[imsg.index[0],'ticker'],
            'high': imsg.loc[imsg.index[0],'high'],
            'low': imsg.loc[imsg.index[0],'low'],
            'close': imsg.loc[imsg.index[0],'close'],
            'open': imsg.loc[imsg.index[0],'open'],
            'timestamp': (imsg.loc[imsg.index[0],'timestamp']).strftime('%Y-%m-%d %H:%M:%S'),
            'volume': imsg.loc[imsg.index[0],'volume'],

        }
        print(topicmsg)
        producer.send(topic=itopic,value=json.dumps(topicmsg,default=str),key=None,partition=ipartition)
        producer.flush()
        producer.close()
        
        print("message sent to kafka topic: ", itopic)
    except Exception as e:              
        print("Error sending message to kafka... errorcode={}".format(str(e))) 
        pass
