"""Ray Server with pre-built FAISS index."""
import ray
from ray import serve
from fastapi import FastAPI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Initialize Ray
ray.init()

# Define our FastAPI app
app = FastAPI()

@serve.deployment
class SearchDeployment:
    def __init__(self):
        print("Loading pre-built index...")
        # Initialize the embedding model - must match what was used for building
        self.embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-mpnet-base-v2')

        # Load the pre-built index
        try:
            self.index = FAISS.load_local("faiss_index", self.embeddings)
            print(f"Successfully loaded index")
        except Exception as e:
            print(f"Error loading index: {str(e)}")
            raise

        print("SearchDeployment initialized successfully")

    async def __call__(self, request):
        query = request.query_params.get("query", "")
        if not query:
            return {"results": []}

        # Search the index
        results = self.index.similarity_search_with_score(query, k=5)

        # Format results for response
        formatted_results = []
        for doc, score in results:
            formatted_results.append({
                "content": doc.page_content,
                "source": doc.metadata.get("source", "Unknown"),
                "score": float(score)  # Convert numpy float to Python float for JSON serialization
            })

        return {"results": formatted_results}

# For testing the deployment locally
@app.get("/search")
async def search(query: str = ""):
    handle = serve.get_deployment_handle("SearchDeployment")
    return await handle.remote({"query_params": {"query": query}})

if __name__ == "__main__":
    # Deploy the search service
    deployment = SearchDeployment.bind()
    serve.run(deployment)

    print("Service started at: http://localhost:8000/")
    print("Example query: http://localhost:8000/?query=How%20can%20Ray%20help%20with%20deploying%20LLMs%3F")