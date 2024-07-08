from indexify import IndexifyClient

client = IndexifyClient()

ingested_content = client.list_content(
    "wiki_extraction_pipeline_tutorial"
)

content_id = ingested_content[0].id


chunks = client.get_extracted_content(
    content_id=content_id,
    graph_name="wiki_extraction_pipeline_tutorial",
    policy_name="embeddings"
)

print(chunks)