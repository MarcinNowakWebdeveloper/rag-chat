from backend.core.vector_store import VectorDbCollection
from backend.core.config import config
from backend.constants.vector_collection import VectorCollection

VectorDbCollectionService = VectorDbCollection()
db = VectorDbCollectionService.get_vector_db_by_collection(
    VectorCollection.DEFAULT.value
)

total = db._collection.count()
if not total:
    raise ValueError(f"No results!")

print(f"📄 Chunks count: {total}")

data = db.get(limit=3)

for i, (doc, meta) in enumerate(zip(data["documents"], data["metadatas"])):
    print("\n--- RESULT", i + 1, "---")
    print(doc[:300])
    print("metadata:", meta)
