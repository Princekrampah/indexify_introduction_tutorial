from indexify import IndexifyClient, ExtractionGraph
from langchain_community.document_loaders import WikipediaLoader

client = IndexifyClient()


def load_data(query):
    docs = WikipediaLoader(query=query, load_max_docs=1).load()
    
    for doc in docs:
        client.add_documents("wiki_extraction_pipeline_tutorial", doc.page_content)
        
        
if __name__ == "__main__":
    load_data(query="Python (programming language)")
    load_data(query="Java (programming language)")