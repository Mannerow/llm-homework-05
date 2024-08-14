from typing import Dict, List, Tuple, Union
import numpy as np
from elasticsearch import Elasticsearch
from datetime import datetime

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

def inspect_document_fields(documents):
    for i, document in enumerate(documents):
        print(f"Document {i+1}:")
        
        if isinstance(document, dict):
            for key, value in document.items():
                print(f"  {key}: {value}")
        else:
            print(f"  Warning: Document {i+1} is not a dictionary, it's a {type(document).__name__}")
            print(f"  Document content: {document}")
        
        print("\n")


@data_exporter
def elasticsearch(
    documents: List[Dict[str, Union[Dict, List[int], np.ndarray, str]]], *args, **kwargs,
):
    """
    Exports document data to an Elasticsearch database.
    """

    connection_string = kwargs.get('connection_string', 'http://localhost:9200')
    index_name_prefix = kwargs.get('index_name', 'documents')
    current_time = datetime.now().strftime("%Y%m%d_%M%S")
    index_name = f"{index_name_prefix}_{current_time}"
    print("index name:", index_name)

    from mage_ai.data_preparation.variable_manager import set_global_variable
    #save as global variable to access later
    set_global_variable('augmented_cosmos', 'index_name', index_name)

    number_of_shards = kwargs.get('number_of_shards', 1)
    number_of_replicas = kwargs.get('number_of_replicas', 0)

    es_client = Elasticsearch(connection_string)

    print(f'Connecting to Elasticsearch at {connection_string}')

    index_settings = {
        "settings": {
            "number_of_shards": number_of_shards,
            "number_of_replicas": number_of_replicas
        },
        "mappings": {
            "properties": {
                "text": {"type": "text"},
                "section": {"type": "text"},
                "question": {"type": "text"},
                "course": {"type": "keyword"},
                "document_id": {"type": "keyword"}
            }
        }
    }

    if not es_client.indices.exists(index=index_name):
        es_client.indices.create(index=index_name)
        print('Index created with properties:', index_settings)

    print(f'Indexing {len(documents)} documents to Elasticsearch index {index_name}')

    inspect_document_fields(documents)

    for document in documents:
        es_client.index(index=index_name, document=document)
    print(document)