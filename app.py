from transformers import TFGPT2LMHeadModel, GPT2Tokenizer
from transformers import TextDataset, DataCollatorForLanguageModeling
from transformers import Trainer, TrainingArguments

# Load the tokenizer and model
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = TFGPT2LMHeadModel.from_pretrained("gpt2")

# Load and preprocess your dataset
train_dataset = TextDataset(
    tokenizer=tokenizer,
    file_path="/Users/jayasri/Documents/chatbot/sample_enfection.rtf",  # Replace with the path to your plain text dataset
    block_size=128  # Adjust block size as needed
)

# Define data collator for language modeling
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer, mlm=False
)

# Define training arguments
training_args = TrainingArguments(
    output_dir="./gpt2-finetuned",  # Directory to save the fine-tuned model
    overwrite_output_dir=True,
    num_train_epochs=3,  # Adjust number of epochs as needed
    per_device_train_batch_size=4,  # Adjust batch size as needed
    save_steps=10_000,  # Save model checkpoints every n steps
    save_total_limit=2,  # Limit total number of saved checkpoints
)

# Initialize Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=train_dataset,
)

# Fine-tune the model
trainer.train()

# Save the fine-tuned model
model.save_pretrained("your_finetuned_model")

# Optionally, save the tokenizer as well
tokenizer.save_pretrained("your_finetuned_model")



from transformers import GPT2Tokenizer, GPT2LMHeadModel

# Load the tokenizer and model
tokenizer = GPT2Tokenizer.from_pretrained("your_finetuned_model")
model = GPT2LMHeadModel.from_pretrained("your_finetuned_model")

# Function to generate response
def generate_response(input_text, max_length=50):
    # Tokenize input text
    input_ids = tokenizer.encode(input_text, return_tensors="pt")

    # Generate response
    output = model.generate(input_ids, max_length=max_length, num_return_sequences=1)

    # Decode and return response
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    return response

# Example usage
user_input = "What is the purpose of your company?"
response = generate_response(user_input)
print("Bot:", response)

