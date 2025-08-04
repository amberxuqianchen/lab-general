import os
import re
import pickle
import glob
import argparse
import pandas as pd
import numpy as np
from openai import OpenAI
from nltk.tokenize import sent_tokenize, word_tokenize
from concurrent.futures import ProcessPoolExecutor
import time
from collections import deque
import logging
from config import OPENAI_API_KEY
# Setup logging
logging.basicConfig(level=logging.INFO)

# Constants for rate limits
TOKEN_LIMIT_PER_MINUTE = 1_000_000
REQUEST_LIMIT_PER_MINUTE = 3_000
MAX_TOKENS_PER_REQUEST = 8192

# Queues to track token and request timestamps
token_timestamps = deque()
request_timestamps = deque()

def read_and_clean_article(file_path):
    with open(file_path, "r") as f:
        content = f.read()

    content = re.sub(r'<[hp]>|<\/[hp]>', '', content)
    content = re.sub(r' @ @', '', content)
    content = re.sub(r'\s+', ' ', content).strip()

    return content

def split_text_into_chunks(text, max_tokens=MAX_TOKENS_PER_REQUEST):
    tokens = word_tokenize(text)
    chunks = []
    
    for i in range(0, len(tokens), max_tokens):
        chunk = " ".join(tokens[i:i + max_tokens])
        chunks.append(chunk)

    return chunks

def get_gpt_embedding(text_to_embed):
    try:
        # Reinitialize the client within each worker process
        client = OpenAI(api_key=OPENAI_API_KEY)
        
        tokens = word_tokenize(text_to_embed)
        if len(tokens) > MAX_TOKENS_PER_REQUEST:
            chunks = split_text_into_chunks(text_to_embed)
            embeddings = []
            for chunk in chunks:
                enforce_rate_limit(len(word_tokenize(chunk)), 1)
                response = client.embeddings.create(
                    model="text-embedding-3-large",
                    input=[chunk]
                )
                embeddings.append(np.array(response.data[0].embedding))
            embedding = np.mean(embeddings, axis=0)
        else:
            enforce_rate_limit(len(tokens), 1)
            response = client.embeddings.create(
                model="text-embedding-3-large",
                input=[text_to_embed]
            )
            embedding = np.array(response.data[0].embedding)
        
        return embedding

    except Exception as e:
        logging.error(f"Error getting embedding: {e}")
        return None

def enforce_rate_limit(tokens_used, requests_used):
    current_time = time.time()

    while token_timestamps and current_time - token_timestamps[0] > 60:
        token_timestamps.popleft()
    while request_timestamps and current_time - request_timestamps[0] > 60:
        request_timestamps.popleft()

    tokens_in_last_minute = sum(token_timestamps)
    requests_in_last_minute = len(request_timestamps)

    if tokens_in_last_minute + tokens_used > TOKEN_LIMIT_PER_MINUTE or requests_in_last_minute + requests_used > REQUEST_LIMIT_PER_MINUTE:
        time_to_wait = max(
            (60 - (current_time - token_timestamps[0])) if token_timestamps else 0,
            (60 - (current_time - request_timestamps[0])) if request_timestamps else 0
        )
        logging.info(f"Rate limit exceeded. Waiting for {time_to_wait:.2f} seconds.")
        time.sleep(time_to_wait)

    token_timestamps.append(tokens_used)
    request_timestamps.append(requests_used)

def get_sentence_embeddings(text):
    sentences = sent_tokenize(text)
    embeddings = [get_gpt_embedding(sentence) for sentence in sentences]
    return np.array(embeddings)

def aggregate_sentence_embeddings(embeddings, method="mean"):
    if method == "mean":
        return np.mean(embeddings, axis=0)
    else:
        raise ValueError("Invalid aggregation method")

def get_missing_names(celebrity_names, file_path):
    df = pd.read_csv(file_path)
    names = df["IDnames"].apply(lambda x: " ".join(x.split("_")[2:])).tolist()
    names = [name.replace(' ', '_') for name in names]
    missingnames = [name for name in names if name not in celebrity_names]
    return missingnames

def process_celebrity_news(celebrity, news_folder, rdm_folder):
    file_paths = [i for i in os.listdir(news_folder) if celebrity in i]
    news_articles = [read_and_clean_article(os.path.join(news_folder, file)) for file in file_paths]
    sentences = '\n'.join(news_articles)
    # print(f"Processing {celebrity} with {len(sentences)} sentences: {sentences}")
    sentence_embeddings = get_sentence_embeddings(sentences)
    article_embedding = aggregate_sentence_embeddings(sentence_embeddings)
    with open(os.path.join(rdm_folder, celebrity + '.pkl'), 'wb') as f:
        pickle.dump(article_embedding, f)
    logging.info(f'{celebrity} done')

def process_celebrity_parallel(celebrity, news_folder, rdm_folder):
    if os.path.exists(os.path.join(rdm_folder, celebrity + '.pkl')):
        logging.info(f"{celebrity} already done, skipping...")
    else:
        logging.info(f"Processing {celebrity}...")
        process_celebrity_news(celebrity, news_folder, rdm_folder)

def main(startnum, endnum, news_folder='../newsText/', rdm_folder='../newsRDM_GPT3large/', max_workers=4):

    if not os.path.exists(rdm_folder):
        os.makedirs(rdm_folder)

    pkl_files = glob.glob(os.path.join(rdm_folder, "*.pkl"))
     # delete the pkl files if the npy shape is ()
    for file in pkl_files:
        with open(file, 'rb') as f:
            embedding = pickle.load(f)
            if embedding.shape == ():
                os.remove(file)
                print(f"Deleted {file} because it is empty")

    celebrity_names = list(set(os.path.basename(file_name).split('.')[0] for file_name in pkl_files))

    file_path = "../../data/CelebA_ID_Demographics.csv"
    missingnames = get_missing_names(celebrity_names, file_path)
    logging.info(f'names without embeddings: {missingnames}')

    missingnames = missingnames[startnum:endnum]

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        executor.map(process_celebrity_parallel, missingnames, [news_folder] * len(missingnames), [rdm_folder] * len(missingnames))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert text to GPT embeddings using parallel processing with rate limits.")
    parser.add_argument("startnum", type=int, help="Starting number of celebrities to process")
    parser.add_argument("endnum", type=int, help="Ending number of celebrities to process")
    parser.add_argument("--news_folder", default='../newsText/', help="Path to the news text folder")
    parser.add_argument("--rdm_folder", default='../newsRDM_GPT3large/', help="Path to the RDM output folder")
    parser.add_argument("--max_workers", type=int, default=8, help="Number of parallel workers")

    args = parser.parse_args()

    main(args.startnum, args.endnum, args.news_folder, args.rdm_folder, args.max_workers)
# # Example usage:
# # python celebrity_news_embeddings_GPT_chunking.py 0 1 --news_folder ../../newsText/ --rdm_folder ../../newsRDM_GPT3large_replicate/ --max_workers 8
# python celebrity_news_embeddings_GPT_chunking.py 0 50 --news_folder ../../wiki/ --rdm_folder ../../wikiRDM_GPT3large/ --max_workers 8