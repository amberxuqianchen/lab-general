import os
import re
import pickle
import glob
import argparse
import pandas as pd
import numpy as np
import torch
from nltk.tokenize import sent_tokenize
from transformers import AutoTokenizer, AutoModel

def read_and_clean_article(file_path):
    with open(file_path, "r") as f:
        content = f.read()

    content = re.sub(r'<[hp]>|<\/[hp]>', '', content)
    content = re.sub(r' @ @', '', content)
    content = re.sub(r'\s+', ' ', content).strip()

    return content

def load_pretrained_bert_model(model_name):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)
    return tokenizer, model

def get_sentence_embeddings(text, tokenizer, model, device="gpu"):
    sentences = sent_tokenize(text)
    embeddings = []

    for sentence in sentences:
        # note: the tokenizer will truncate the input to 512 tokens /if it is too long
        inputs = tokenizer(sentence, return_tensors="pt", truncation=True, padding=True, max_length=512).to(device)
        with torch.no_grad():
            outputs = model(**inputs)
        embeddings.append(outputs.last_hidden_state.mean(dim=1).squeeze().cpu().numpy())

    return np.array(embeddings)

def aggregate_sentence_embeddings(embeddings, method="mean"):
    if method == "mean":
        return np.mean(embeddings, axis=0)
    else:
        raise ValueError("Invalid aggregation method")

def get_missing_names(celebrity_names, file_path):
    df = pd.read_csv(file_path)
    names = df["IDnames"].apply(lambda x: " ".join(x.split("_")[2:])).tolist()
    names = [name.replace(' ','_') for name in names]
    missingnames = [name for name in names if name not in celebrity_names]
    return missingnames

def process_celebrity_news(celebrity, news_folder,rdm_folder, tokenizer, model, device):
    file_paths = [i for i in os.listdir(news_folder) if celebrity in i]
    news_articles = [read_and_clean_article(news_folder + file) for file in file_paths]
    sentences = '\n'.join(news_articles)
    sentence_embeddings = get_sentence_embeddings(sentences, tokenizer, model, device)
    article_embedding = aggregate_sentence_embeddings(sentence_embeddings)
    with open(rdm_folder+ celebrity +  '.pkl', 'wb') as f:
        pickle.dump(article_embedding, f)
    print(celebrity + ' done')

def main(startnum, endnum, news_folder='./newsText/', rdm_folder='./newsRDM/'):
    
    # Ensure the output folder exists
    if not os.path.exists(rdm_folder):
        os.makedirs(rdm_folder)

    text_files = glob.glob(os.path.join(news_folder, "*.txt"))
    pkl_files = glob.glob(os.path.join(rdm_folder, "*.pkl"))
    
    # delete the pkl files if the npy shape is ()
    for file in pkl_files:
        with open(file, 'rb') as f:
            embedding = pickle.load(f)
            if embedding.shape == ():
                os.remove(file)
                print(f"Deleted {file} because it is empty")

    celebrity_names = list(set(os.path.basename(file_name).split('.')[0] for file_name in pkl_files))

    file_path = "./data/CelebA_ID_Demographics.csv"
    missingnames = get_missing_names(celebrity_names, file_path)
    print('names without embeddings: ', missingnames)
    # bert_model_name = "distilbert-base-uncased"
    # bert_model_name = "roberta-base"
    bert_model_name = "microsoft/deberta-base"

    tokenizer, model = load_pretrained_bert_model(bert_model_name)
    model.eval()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    for celebrity in missingnames[startnum:endnum]:
        if os.path.exists(os.path.join(rdm_folder, celebrity + '.pkl')):
            print(celebrity + ' already done')
            break
        process_celebrity_news(celebrity, news_folder,rdm_folder, tokenizer, model, device)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert text to BERT embeddings.")
    parser.add_argument("startnum", type=int, help="Starting number of celebrities to process")
    parser.add_argument("endnum", type=int, help="Ending number of celebrities to process")
    parser.add_argument("--news_folder", default='./newsText/', help="Path to the news text folder")
    parser.add_argument("--rdm_folder", default='./newsRDM/', help="Path to the news text folder")
    
    args = parser.parse_args()
    
    main(args.startnum, args.endnum,args.news_folder, args.rdm_folder)
# # Example usage:
# # python celebrity_news_embedding.py 0 5 --news_folder ./newsText/ --rdm_folder ./newsRDM_DeBERTa/