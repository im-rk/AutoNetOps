from transformers import AutoTokenizer,AutoModelForTokenClassification
from transformers import pipeline
import nltk
import re

model_name="dslim/bert-base-NER"
tokenizer=AutoTokenizer.from_pretrained(model_name)
model=AutoModelForTokenClassification.from_pretrained(model_name)

nlp_pipeline=pipeline("ner",model=model,tokenizer=tokenizer,grouped_entities=True)
print('done')