# MODEL HOSTED HERE:
https://huggingface.co/spaces/SimonHochmuth1/Bert_Sentiment_Model


# Sentiment Classifier API with Hugging Face and FastAPI

This project fine-tunes a `bert-base-uncased` model on the IMDb dataset using Hugging Face's `transformers` and serves predictions via a FastAPI web API.
Rather than hosting it, I use uvicorn to test the application

---

##  Features

- Fine-tunes a BERT model for sentiment classification
- FastAPI-based REST endpoint for real-time predictions
- Accepts raw text input and returns `POSITIVE` / `NEGATIVE` sentiment
- Trained using Hugging Face `Trainer` API on IMDb dataset

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```
### 2. Create venv & Install Dependencies
```bash
py -3.10 -m venv venv310
.\venv310\Scripts\activate
pip install -r requirements.txt
```

### 3. Training the Model
```bash
python train_model.py
```

This will save to: ./my_sentiment_model/

### 4. Launching the API Server
```bash
uvicorn app:app --reload
```

### 5. Example API Request
```bash
curl -X POST http://localhost:8000/predict \
     -H "Content-Type: application/json" \
     -d "{\"text\": \"This movie was surprisingly good!\"}"
```
### Expected Output
```
{
  "label": "POSITIVE",
  "score": 0.9872
}
```