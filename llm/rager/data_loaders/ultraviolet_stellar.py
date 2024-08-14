from typing import Dict, List, Union

import numpy as np
from elasticsearch import Elasticsearch
from mage_ai.data_preparation.variable_manager import get_global_variable

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def search(*args, **kwargs) -> List[Dict]:
    connection_string = kwargs.get('connection_string', 'http://localhost:9200')
    index_name = get_global_variable('eldritch_celestial', 'index_name')
    top_k = kwargs.get('top_k', 5)
    chunk_column = 'text' # Col to search

    es_client = Elasticsearch(connection_string)

    query_text = "When is the next cohort?"

    # Constructing a basic match query
    search_query = {
        "match": {
            chunk_column: query_text #determines which field to look for matches in
        }
    }

    response = es_client.search(
        index=index_name,
        query=search_query,
        size=top_k,
        _source=[chunk_column, 'document_id'], # _source defines the fields to include in output_
    )

    # Extract both the document_id and text content
    res = [{
        'document_id': hit['_source']['document_id'],
        chunk_column: hit['_source'][chunk_column]
    } for hit in response['hits']['hits']]
    
    if res:
        top_result_id = res[0]['document_id']  # Get the document_id of the top result
        print(f'Top result document_id: {top_result_id}')
    
    print(res)
    return res
