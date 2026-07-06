Title: Fine tuning the text to SQL using JAX echo System - Part 2
Date: 2026-05-05
Tags: Python, Nima Moradi, Jax, Applied AI, SQL, LLM, Gemma
Category: Guide
Summary: Loading a small Gemma model, preparing prompts, tokenizing text, and running the first zero-shot text-to-SQL examples

# Introduction

In the previous part, I loaded the Spider dataset, inspected a few samples, and attached the database schema definition to each record. That gave me the three main pieces I need for text-to-SQL:

1. the user question,
1. the target SQL query,
1. the database schema.

In this part, I move from data loading to model loading and zero-shot generation.

The goal is not fine-tuning yet. Before changing the model weights, I want to check the full path from a Spider sample to a prompt, from a prompt to tokens, and from the model output back to text. This gives me a baseline and also makes sure the model, tokenizer, and data loader are connected correctly.

# Why Gemma and JAX

At first I experimented with models from Hugging Face Transformers. That path is very flexible because it gives access to many decoder-only and encoder-decoder models, and it is easy to switch between model families.

But for this series I want to keep the project inside the JAX ecosystem as much as possible. Since the rest of the project already uses JAX-related tools, it is better if the model loading, sampling, and later fine-tuning also follow the same direction.

I looked at Flax and the JAX model-loading options, and for this project I selected the Gemma library from Google DeepMind. The Gemma package gives a simple way to load Gemma model definitions, load checkpoint parameters, initialize tokenizers, and then sample from the model.

For this experiment I use a very small Gemma model. The important reason is iteration speed. A small model will not give the best text-to-SQL accuracy, but it is much easier to load, inspect, debug, and fine-tune on limited hardware.

# Model weights and Kaggle

To use Gemma weights, I need to download the checkpoint. In my setup this means using Kaggle.

There are two important steps before the code can load the model:

1. accept the Gemma model license on Kaggle,
1. make the checkpoint available locally or in the path expected by the code.

This is an important practical step. The code can define the model architecture, but it cannot use the trained model until the model parameters are available. So the checkpoint path in the configuration must point to the downloaded weights.

For local development, the setup usually looks like this:

```bash
mkdir -p ~/.kaggle
cp kaggle.json ~/.kaggle/kaggle.json
chmod 600 ~/.kaggle/kaggle.json
```

After that, the model can be downloaded with the Kaggle tools or by following the download instructions from the Gemma page. In my code I keep the final checkpoint path as a configuration value, so the rest of the project does not need to know where the model came from.

# Factory pattern for model loading

I wanted the model-loading code to be replaceable. Today I am using a small Gemma model, but later I may want to try another Gemma size, another tokenizer, or even a different encoder/decoder setup.

For that reason I used a factory pattern.

The main model-loading logic is placed in:

```text
src/model_loading/llm_factory.py
```

The configuration is created in:

```text
src/main.py
```

The simplified version of the configuration looks like this:

```python
config = LLMFactoryConfig(
    ckpt_path=ckpt_path,
    tokenizer_path=tokenizer_path,
    model_cls=gm.nn.Gemma3_270M,
    tokenizer_cls=gm.text.Gemma3Tokenizer,
)
```

The exact fields can change as the code evolves, but the idea is the same: `main.py` decides *what* model and tokenizer to use, and the factory decides *how* to build them.

The factory then builds the model module:

```python
factory = LLMModuleFactory(config)
modules = factory.build()
```

Inside `build()`, the flow is:

1. instantiate the model architecture,
1. load the trained parameters from the checkpoint path,
1. initialize the tokenizer,
1. wrap the model and parameters in a sampler.

The sampler is the object I use later for generation.

A shortened version of the idea is:

```python
class LLMModuleFactory:
    def __init__(self, config: LLMFactoryConfig):
        self.config = config

    def build(self):
        model = self.config.model_cls()

        params = load_params(self.config.ckpt_path)

        tokenizer = self.config.tokenizer_cls()

        sampler = gm.text.Sampler(
            model=model,
            params=params,
            tokenizer=tokenizer,
        )

        return LLMModules(
            model=model,
            params=params,
            tokenizer=tokenizer,
            sampler=sampler,
        )
```

This is not meant to be the complete source code. It only shows the structure. The important part is that the caller does not need to manually load parameters, construct tokenizers, and wire the sampler every time.

# Tokenization

Before sending text to the model, I need to understand how the tokenizer sees the prompt.

The Gemma tokenizer can encode text into token ids and decode token ids back into text. For debugging, this is useful because the model never sees the original Python string directly. It sees token ids.

A simple check looks like this:

```python
tokenizer = modules.tokenizer

text = "How many singers do we have?"
token_ids = tokenizer.encode(text)

print(token_ids)
print(tokenizer.decode(token_ids))
```

For text-to-SQL, this matters because the prompt can become long after adding the database schema. Even a small natural language question can turn into a large input once we include all table definitions.

I also checked the more manual tokenizer methods from the Gemma tokenizer documentation. For now I keep the tokenization path simple because Part 2 is mainly about connecting the full pipeline. Later, when fine-tuning starts, tokenization will become more important because I need to prepare labels, masks, padding, and end-of-sequence behavior.

# Prompt format

The Spider sample gives me the question, the SQL query, and the schema.

For zero-shot generation I only give the model the schema and the question. The target SQL query is kept for comparison.

A simple prompt builder can look like this:

```python
def build_text_to_sql_prompt(record):
    return f"""You are a text-to-SQL assistant.

Given the database schema and a user question, write one valid SQLite SQL query.
Only use the tables and columns shown in the schema.
Return only the SQL query.

Database schema:
{record["db_definitions"]}

Question:
{record["question"]}

SQL:
"""
```

The main idea is to make the task explicit:

1. the model should generate SQL,
1. the SQL should match the provided schema,
1. the output should contain only the SQL query.

This prompt is still simple. I am not adding few-shot examples yet because I want to see how the model behaves before adding training examples or fine-tuning.

# Loading one Spider sample

The data loader from Part 1 already gives me records like this:

```python
sample = next(iter(dev_loader))
```

With `batch_size=1`, the values are wrapped in arrays, so I usually extract the first item before building the prompt:

```python
record = {
    "db_id": sample["db_id"][0],
    "question": sample["question"][0],
    "query": sample["query"][0],
    "db_definitions": sample["db_definitions"][0],
}

prompt = build_text_to_sql_prompt(record)
print(prompt)
```

For the first sample from the development split, the question is:

```text
How many singers do we have?
```

The target SQL is:

```sql
SELECT count(*) FROM singer
```

This is a good first example because the correct query is short and uses one table.

# Zero-shot generation

After loading the model and preparing the prompt, I can call the sampler.

In `src/main.py`, the flow is:

```python
modules = factory.build()

evaluate_text_to_sql(
    sampler=modules.sampler,
    loader=dev_loader,
    max_new_tokens=128,
    temperature=0.0,
)
```

The evaluation function loops over a few samples, builds the prompt, generates SQL, and compares it with the ground-truth query.

A simplified version is:

```python
def evaluate_text_to_sql(sampler, loader, max_new_tokens=128, temperature=0.0):
    for sample in loader:
        record = {
            "db_id": sample["db_id"][0],
            "question": sample["question"][0],
            "query": sample["query"][0],
            "db_definitions": sample["db_definitions"][0],
        }

        prompt = build_text_to_sql_prompt(record)

        generated_sql = sampler.sample(
            prompt,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
        )

        print("Question:")
        print(record["question"])

        print("Expected SQL:")
        print(record["query"])

        print("Generated SQL:")
        print(generated_sql)

        break
```

I use `temperature=0.0` for this stage because I want deterministic generation. For evaluation, randomness makes debugging harder. If the output changes every run, it is more difficult to know whether a change came from the model, the prompt, or the sampling settings.

# Comparing generated SQL with the target query

For now the comparison is simple. I print the generated SQL next to the expected SQL.

```text
Question:
How many singers do we have?

Expected SQL:
SELECT count(*) FROM singer

Generated SQL:
...
```

This is not a full text-to-SQL evaluation yet.

SQL evaluation is more complicated than normal string comparison because two SQL queries can be written differently and still return the same result. For example:

```sql
SELECT count(*) FROM singer
```

and:

```sql
SELECT COUNT(Singer_ID) FROM singer
```

may be equivalent depending on the database and the data.

So in this part I only use the output for inspection. Later in the series I will add a better evaluation step by executing generated SQL on SQLite and comparing the result with the expected query result.

# What I learned from this step

This step is mainly about making the project runnable end to end.

At this point, I have:

1. loaded Spider examples with schema definitions,
1. loaded a small Gemma model,
1. initialized the tokenizer,
1. created a prompt for text-to-SQL,
1. generated SQL in a zero-shot setting,
1. printed the generated SQL next to the target query.

The zero-shot result is only a baseline. I do not expect a very small model to solve Spider reliably without fine-tuning. But that is exactly why this baseline is useful. It shows the starting point before training.

# Notes and limitations

There are a few limitations in this version:

1. The prompt is simple and does not include examples.
1. The tokenizer path is kept simple.
1. I am not yet masking labels or preparing training batches.
1. The comparison is not execution-based.
1. The model may produce extra text around the SQL query.

These are acceptable for Part 2 because the goal is to test model loading and generation, not to claim strong accuracy.

# Next step

In the next part, I will start fine-tuning the model with LoRA.

The main change will be that the target SQL query will become part of the training example. Instead of only asking the model to generate SQL, I will prepare supervised examples where the model learns the mapping from:

```text
schema + question
```

to:

```text
SQL query
```

This will also require a more careful tokenization pipeline, because the model should learn from the SQL answer while not treating every part of the prompt in the same way during training.

# References

- Gemma official overview: https://ai.google.dev/gemma/docs
- Gemma GitHub repository: https://github.com/google-deepmind/gemma
- Gemma tokenizer documentation: https://gemma-llm.readthedocs.io/en/latest/colab_tokenizer.html
- Gemma on Kaggle: https://www.kaggle.com/models/google/gemma
