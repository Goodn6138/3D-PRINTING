import faiss
import numpy as np
from transformers import BertTokenizer, BertModel, GPT2LMHeadModel, GPT2Tokenizer
import torch

bert_tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
bert_model = BertModel.from_pretrained('bert-base-uncased')


gpt2_tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
gpt2_model = GPT2LMHeadModel.from_pretrained('gpt2')

documents = [
    "The burning of fossil fuels releases greenhouse gases into the atmosphere.",
    "Deforestation reduces the planet's ability to absorb carbon dioxide.",
    "Renewable energy sources include wind, solar, and hydro power.",
    "Climate change leads to more extreme weather events, like hurricanes and droughts."
]


def encode_documents(docs):
    encoded_docs = []
    for doc in docs:
        inputs = bert_tokenizer(doc, return_tensors='pt', max_length=512, truncation=True)
        with torch.no_grad():
            outputs = bert_model(**inputs)
            encoded_docs.append(outputs.last_hidden_state.mean(dim=1).numpy())
    return np.vstack(encoded_docs)

def initialize_faiss_index(embeddings):
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    return index

def generate_response(prompt, retrieved_docs):
    context = " ".join(retrieved_docs)
    input_text = f"{prompt} Context: {context}"
    inputs = gpt2_tokenizer(input_text, return_tensors='pt')
    with torch.no_grad():
        outputs = gpt2_model.generate(**inputs, max_length=150, num_return_sequences=1)
    response = gpt2_tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

def rag_model(query):
    # Encode documents and initialize FAISS index
    doc_embeddings = encode_documents(documents)
    index = initialize_faiss_index(doc_embeddings)
    
    # Encode the query
    query_embedding = encode_documents([query])
    
    # Retrieve relevant documents
    _, indices = index.search(query_embedding, k=2)  # Retrieve top-2 documents
    retrieved_docs = [documents[i] for i in indices[0]]
    
    # Generate response
    response = generate_response(query, retrieved_docs)
    return response

query = "What are the main causes of climate change?"
response = rag_model(query)
print(response)

