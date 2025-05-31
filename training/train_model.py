import torch
import json
import os
import sys
import glob
from transformers import GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments
from torch.utils.data import Dataset

class LyricsDataset(Dataset):
    def __init__(self, file_paths, tokenizer, max_length=512):
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.lyrics = []
        for file_path in file_paths:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        data = json.loads(line)
                        self.lyrics.append(data['lyrics'])
                    except json.JSONDecodeError:
                        continue
    
    def __len__(self):
        return len(self.lyrics)
    
    def __getitem__(self, idx):
        text = self.lyrics[idx]
        encoding = self.tokenizer(
            text,
            max_length=self.max_length,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )
        return {
            'input_ids': encoding['input_ids'].squeeze(),
            'attention_mask': encoding['attention_mask'].squeeze(),
            'labels': encoding['input_ids'].squeeze()
        }

def main():
    if len(sys.argv) < 2:
        print("Usage: python train_model.py <data_file1> [<data_file2> ...]")
        return
    data_files = sys.argv[1:]
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
    tokenizer.pad_token = tokenizer.eos_token
    checkpoints = sorted(glob.glob('results/checkpoint-*'), key=os.path.getmtime)
    if checkpoints:
        model_path = checkpoints[-1]
        print(f"Resuming training from {model_path}")
        model = GPT2LMHeadModel.from_pretrained(model_path)
    else:
        model = GPT2LMHeadModel.from_pretrained('gpt2')
    dataset = LyricsDataset(data_files, tokenizer)
    training_args = TrainingArguments(
        output_dir='./results',
        num_train_epochs=1,
        per_device_train_batch_size=4,
        save_steps=10_000,
        save_total_limit=10,
        logging_dir='./logs',
        logging_steps=500,
        learning_rate=5e-5,
        fp16=True,
        report_to='none',
        resume_from_checkpoint=bool(checkpoints)
    )
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
    )
    trainer.train()

if __name__ == "__main__":
    main()
