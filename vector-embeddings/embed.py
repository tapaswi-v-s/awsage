
import pandas as pd
import requests
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
import time
from dotenv import load_dotenv
load_dotenv()

def split_text(text, chunk_size=200, chunk_overlap=30):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = splitter.split_text(text)
    return chunks

def get_embeddings(chunks, jina_embedding_model = "jina-embeddings-v2-base-en"):
    url = 'https://api.jina.ai/v1/embeddings'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {os.environ["JINA_API_KEY"]}'
    }
    data = {
        "model": jina_embedding_model,
        "embedding_type": "float",
        "input": chunks
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        embeddings = [e['embedding'] for e in response.json()['data']]
        return embeddings
    else:
        response.raise_for_status()

def get_csv_files():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    data_dir = os.path.join(parent_dir, 'data-collection')
    csv_dir = os.path.join(data_dir, 'CSV')

    if not os.path.exists(csv_dir):
        print(f'Please Generate the CSVs using Scraper: {os.path.join(data_dir, "scrapper.py")}')
    else:
        csv_files = [os.path.join(csv_dir, file) for file in \
                     os.listdir(csv_dir) if file.endswith('.csv') \
                     and os.path.isfile(os.path.join(csv_dir, file))]
        return csv_files


def generate_embeddings(csv_files, output_dir, progress_dir):
    for csv in csv_files:
        progress_file = os.path.join(progress_dir, (os.path.basename(csv).split('.')[0] + '.txt'))
        
        print(f"Generating embeddings for: {os.path.basename(csv)}")
        
        with open(progress_file, 'w') as pf:
            def embed(row,total):
                pf.write(f'Processing {row.name+1}/{total} row\n')
                return get_embeddings(row['chunks'])

            df = pd.read_csv(csv)
            df['chunks'] = df['answer'].apply(lambda x: split_text(x.strip()))
            df['embeddings'] = df.apply(lambda row : embed(row, len(df)), axis=1)
            
            out_file = os.path.join(output_dir, os.path.basename(csv))
            df.to_csv(out_file, index=False)
            print(f'[DONE] Embeddings saved to: {out_file}\n')
    

progress_dir = os.path.join(os.path.dirname(__file__), 'progress') 
output_dir = os.path.join(os.path.dirname(__file__), 'embeddings')
csv_files = get_csv_files()

if not os.path.exists(progress_dir):
    os.mkdir(progress_dir)

if not os.path.exists(output_dir):
    os.mkdir(output_dir)

start_time = time.time()
generate_embeddings(csv_files, output_dir, progress_dir)
end_time = time.time()

print(f'Time Taken: {round((end_time-start_time)/60, 2)} minutes')