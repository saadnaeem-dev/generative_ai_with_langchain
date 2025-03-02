import requests

query = "How can Ray help with deploying LLMs?"
response = requests.get(f"http://localhost:8000/?query={query}")
results = response.json()["results"]


if __name__ == "__main__":
    for i, result in enumerate(results):
        print(f"Result {i+1}:")
        print(f"Source: {result['source']}")
        print(f"Content: {result['content'][:200]}...")
        print()
