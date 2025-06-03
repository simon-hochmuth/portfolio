def main():
    from datasets import load_dataset
    from transformers import AutoTokenizer, AutoModelForSequenceClassification
    from transformers import TrainingArguments, Trainer
    import numpy as np
    from sklearn.metrics import accuracy_score, f1_score
    import torch
    import time

    # ---- 1. Load IMDb dataset from Hugging Face ----
    dataset = load_dataset("imdb")
    dataset = dataset["train"].train_test_split(test_size=0.2)

    # ---- 2. Load Tokenizer ----
    model_name = "bert-base-uncased"
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    def tokenize_function(example):
        return tokenizer(example["text"], padding="max_length", truncation=True)

    tokenized_datasets = dataset.map(tokenize_function, batched=True)

    # ---- 3. Load Pretrained Model ----
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)
    model.to(device)

    # ---- 4. Define Metrics ----
    def compute_metrics(eval_pred):
        logits, labels = eval_pred
        predictions = np.argmax(logits, axis=1)
        return {
            "accuracy": accuracy_score(labels, predictions),
            "f1": f1_score(labels, predictions),
        }

    # ---- 5. Define Training Arguments ----
    training_args = TrainingArguments(
        output_dir="./results",
        evaluation_strategy="epoch",
        save_strategy="epoch",
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        num_train_epochs=2,
        weight_decay=0.01,
        logging_dir="./logs",
        logging_steps=10,

        # 🆕 Recommended additions:
        fp16=True,                   # enables mixed-precision for speedup on RTX 4070
        dataloader_num_workers=4     # uses 4 CPU threads to speed up data loading
    )

    # ---- 6. Trainer Setup ----
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_datasets["train"],
        eval_dataset=tokenized_datasets["test"],
        tokenizer=tokenizer,
        compute_metrics=compute_metrics,
    )

    # ---- 7. Train ----
    trainer.train()

    # ---- 8. Save Model ----
    model.save_pretrained("./my_sentiment_model")
    tokenizer.save_pretrained("./my_sentiment_model")

    print("Model training complete and saved to ./my_sentiment_model")
if __name__ == "__main__":
    from multiprocessing import freeze_support
    freeze_support()
    main() 
