import pandas as pd
import os, json

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
data_dir = os.path.join(parent_dir, 'data-collection')
csv_dir = os.path.join(data_dir, 'CSV')
data_path = os.path.join(current_dir, 'data.jsonl') 
progress_file = os.path.join(current_dir, 'progress.txt') 

def get_csv_files():
    if not os.path.exists(csv_dir):
        print(f'Please Generate the CSVs using Scraper: {os.path.join(data_dir, "scrapper.py")}')
    else:
        csv_files = [os.path.join(csv_dir, file) for file in \
                     os.listdir(csv_dir) if file.endswith('.csv') \
                     and os.path.isfile(os.path.join(csv_dir, file))]
        return csv_files
    

system_prompt = 'You are an assistant for question-answering tasks about amazon web service.'
csv_files = get_csv_files()

total_faqs = sum([len(pd.read_csv(csv)) for csv in csv_files])
print(f'Total FAQs: {total_faqs}')

with open(data_path, 'w', encoding='utf-8') as json_file, open(progress_file, 'w', encoding='utf-8') as progress:
    count = 1
    progress.write(f"Total FAQs: {total_faqs}\n")
    for i, csv in enumerate(csv_files):    
        df = pd.read_csv(csv)
        progress.write(f"====== {df.iloc[0]['category']}======\n\n")
        for row in df.iterrows():
            json_dic = {"messages":[{"role":"system", "content":system_prompt}, 
                                    {"role":"user", "content": row[1]['question'].replace('\n', '').strip()},
                                    {"role":"assistant", "content":row[1]['answer'].replace('\n', '').strip()}]}
            
            # don't append the '\n' if it is the last row
            if i == len(csv_files)-1 and row[0] == len(df)-1:
                s = json.dumps(json_dic)
                json_file.write(s)
                progress.write(f"Processing {count}/{total_faqs} FAQs")
            else:
                s = json.dumps(json_dic)+'\n'
                json_file.write(s)
                progress.write(f"Processing {count}/{total_faqs} FAQs\n")
            count+=1
        progress.write("\n")