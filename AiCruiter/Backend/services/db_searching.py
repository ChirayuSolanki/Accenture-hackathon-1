import json
from sentence_transformers import SentenceTransformer
import pinecone
import os
import os
from pinecone import Pinecone, ServerlessSpec

pc = Pinecone(
    api_key=os.environ.get("PINECONE_API_KEY")
)
index_name = 'resume'
# Now do stuff
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name, 
        dimension=1536, 
        metric='euclidean',
        spec=ServerlessSpec(
            cloud='aws',
            region='us-west-2'
        )
    )

index = pc.Index(index_name)

model = SentenceTransformer('all-MiniLM-L6-v2')




# 1. Define the search function
def search_resumes(job_description, top_k=5):
    # Step 1: Create embedding from JD
    jd_embedding = model.encode(job_description).tolist()

    # Step 2: Query Pinecone
    results = index.query(
        vector=jd_embedding,
        top_k=top_k,
        include_metadata=True
    )

    # Step 3: Return matches
    matches = []
    for match in results.get("matches", []):
        matches.append({
            "score": match["score"],
            "resume_id": match["id"],
            "sql_id": match["metadata"].get("sql_id"),
            "metadata": match["metadata"]
        })
    
    return matches