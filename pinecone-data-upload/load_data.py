from pinecone.grpc import PineconeGRPC as Pinecone
import pandas as pd
import uuid
from pinecone import ServerlessSpec
from dotenv import load_dotenv
import os, ast, itertools
load_dotenv()

def get_embedding_csv_files():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    embeddings_dir = os.path.join(os.path.join(parent_dir, 'vector-embeddings'), 'embeddings')

    if not os.path.exists(embeddings_dir):
        print(f'Please Generate the embeddings using: {os.path.join(os.path.dirname(embeddings_dir), "embed.py")}')
    else:
        csv_files = [os.path.join(embeddings_dir, file) for file in \
                     os.listdir(embeddings_dir) if file.endswith('.csv') \
                     and os.path.isfile(os.path.join(embeddings_dir, file))]
        return csv_files

def get_pinecone_index():
    pc = Pinecone(api_key=os.environ['PINECONE_API_KEY'])
    index_name = os.environ['PINECONE_INDEX_NAME']
    if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name,
            dimension=768,
            metric="cosine",
            spec=ServerlessSpec(
                cloud='aws', 
                region='us-east-1'
            ) 
        )
    return pc.Index(index_name)

def get_data_to_upsert(embedding_csv_files):
    data = []
    for csv in embedding_csv_files:
        print(f"Upserting embeddings for: {os.path.basename(csv)}")
        
        df = pd.read_csv(csv)
        for row in df.iterrows():
            for embedding in ast.literal_eval(row[1]['embeddings']):
                vector_dict = {}
                vector_dict['id'] = str(uuid.uuid1())
                vector_dict['values'] = embedding
                vector_dict['metadata'] = {
                    'question': row[1]['question'],
                    'answer': row[1]['answer'],
                    'category': row[1]['category'],
                    'sub_category': row[1]['sub_category']}
                data.append(vector_dict)
        
    return data

def split_batches(iterable, batch_size=100):
    it = iter(iterable)
    chunk = tuple(itertools.islice(it, batch_size))
    while chunk:
        yield chunk
        chunk = tuple(itertools.islice(it, batch_size))

def upsert_data(embedding_csv_files, progress_file, batch_size = 100):
    data_to_upsert = get_data_to_upsert(embedding_csv_files)
    
    with open(progress_file, 'w') as pf:
        pf.write(f'Total records: {len(data_to_upsert)}, Batch Size: {batch_size}\n')
        index = get_pinecone_index()
        for i, batch in enumerate(split_batches(data_to_upsert, batch_size)):
            index.upsert(
                vectors=batch,
                namespace='FAQ'
            )
            pf.write(f'Inserted batch: {i+1}, with {len(batch)} objects\n')
             



csv_files = get_embedding_csv_files()
progress_file = os.path.join(os.path.dirname(__file__), 'progress.txt')

upsert_data(csv_files, progress_file)