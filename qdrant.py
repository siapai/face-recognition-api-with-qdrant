import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from qdrant_client.http.exceptions import UnexpectedResponse

load_dotenv()

client = QdrantClient(host=os.getenv("QDRANT_HOST", "localhost"), port=6333)

result = client.get_collections()
person = next((col for col in result.collections if col.name == 'Persons'), None)
if person is None:
    client.create_collection(
       collection_name="Persons",
       vectors_config=VectorParams(size=512, distance=Distance.COSINE),
    )
