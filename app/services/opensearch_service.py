# app/services/opensearch_service.py
from opensearchpy import OpenSearch
from app.core.config import OPENSEARCH_HOST, OPENSEARCH_USER, OPENSEARCH_PASSWORD, OPENSEARCH_INDEX,OPENSEARCH_PORT

def get_opensearch_client():
    client = OpenSearch(
        hosts=[{"host": OPENSEARCH_HOST, "port": OPENSEARCH_PORT}],
        http_auth=(OPENSEARCH_USER, OPENSEARCH_PASSWORD),
        use_ssl=True,
        verify_certs=False,  # For local development; remove in production!
    )
    return client

def create_index_if_not_exists(client):
    if not client.indices.exists(index=OPENSEARCH_INDEX):
        index_body = {
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 0
            },
            "mappings": {
                "properties": {
                    "city": {"type": "text"},
                    "country": {"type": "text"},
                    "clues": {"type": "text"},
                    "fun_fact": {"type": "text"},
                    "trivia": {"type": "text"}
                }
            }
        }
        client.indices.create(index=OPENSEARCH_INDEX, body=index_body)
