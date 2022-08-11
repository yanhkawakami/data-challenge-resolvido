import json
import boto3
from reader import EventRead
from compare_schema_event import CompareEventSchema
import warnings

_SQS_CLIENT = None


def send_event_to_queue(event, queue_name):
    '''
     Responsável pelo envio do evento para uma fila
    :param event: Evento  (dict)
    :param queue_name: Nome da fila (str)
    :return: None
    '''

    sqs_client = boto3.client("sqs", region_name="us-east-1")
    response = sqs_client.get_queue_url(
        QueueName=queue_name
    )
    queue_url = response['QueueUrl']
    response = sqs_client.send_message(
        QueueUrl=queue_url,
        MessageBody=json.dumps(event)
    )
    print(f"Response status code: [{response['ResponseMetadata']['HTTPStatusCode']}]")


def handler(event):
    '''
    #  Função principal que é sensibilizada para cada evento
    Aqui você deve começar a implementar o seu código
    Você pode criar funções/classes à vontade
    Utilize a função send_event_to_queue para envio do evento para a fila,
        não é necessário alterá-la
    '''
    try:
        # Cria um objeto referenciando a classe EventRead
        event_rd = EventRead()
        # Cria um objeto trazendo as colunas do evento ordenadas
        event_columns = event_rd.get_event_columns_properties(event)
        # Cria um objeto referenciando a classe CompareEventSchema
        compare = CompareEventSchema(schema_file_path="schema.json")

        # Compara se o número de colunas do schema e do evento são iguais.
        # Caso não sejam, nem chega a comparar os elementos
        if compare.compare_size(event_columns):
            # Compara se evento e schema tem os mesmo valores
            if compare.compare_columns_properties(event_columns):
                # Envia o evento para a fila e retorna
                send_event_to_queue(event, "valid-events-queue")
                return
            # Gera o warning acusando que as colunas e/ou tipos estão
            # diferentes entre evento e schema
            warnings.warn("Event not accepted. Not same columns or types")
            return
        # Gera o warning acusando que o número de colunas entre evento
        # e schema são diferentes
        warnings.warn("Event not accepted. Not enough columns")
        return

    except Exception as e:
        raise RuntimeError("Impossible to valite message and send to queue",
                           str(e))
