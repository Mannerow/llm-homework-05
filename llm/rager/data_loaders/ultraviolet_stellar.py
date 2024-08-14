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
    chunk_column = kwargs.get('chunk_column', 'content')

    es_client = Elasticsearch(connection_string)

    query_text = "When is the next cohort?"
    # Constructing a basic match query
    search_query = {
        "match": {
            chunk_column: query_text
        }
    }

    response = es_client.search(
        index=index_name,
        query=search_query,
        size=top_k,
        _source=[chunk_column],
    )
    res = [hit['_source'][chunk_column] for hit in response['hits']['hits']]
    print(res)
    return res


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
