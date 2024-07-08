from openai import OpenAI
from indexify import IndexifyClient
from decouple import config


client = IndexifyClient()

client_openai = OpenAI(
    api_key=config("OPENAI_API_KEY")
)



def qeury_db(query: str, index: str, top_k: int):
    retrieved_results = client.search_index(
        name=index,query=query,top_k=top_k
    )
    
    context = "\n---\n".join([result["text"] for result in retrieved_results])
    
    print(context)
    
    response = client_openai.chat.completions.create(
        messages=[{
            "role": "system",
            "content": f"You are a helpful assistant. Help answer the user's question: {query} based on this provided context: {context}. If you do not know the answer simply say 'I do not know'."
        }],
        model="gpt-3.5-turbo",        
    )
    
    return response.choices[0].message.content


if __name__ == "__main__":
    query = "What is Jave Programming Language?"
    index = "wiki_extraction_pipeline_tutorial.wikiembedding.embedding"
    top_k = 2
    
    response = qeury_db(query=query, index=index, top_k=top_k)
    
    print("=== Response ===")
    print(response)