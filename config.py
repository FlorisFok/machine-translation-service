from pydantic import BaseModel
from typing import Optional

HUGGINGFACE_S3_BASE_URL="https://s3.amazonaws.com/models.huggingface.co/bert/Helsinki-NLP"
FILENAMES = ["config.json","pytorch_model.bin","source.spm","target.spm","tokenizer_config.json","vocab.json"]
MODEL_PATH = "data"
NORMAL_BATCH_SIZE = 32
JOB = None

class Input(BaseModel):
    text: str

class ChoseModel(BaseModel):
    source: Optional[str] = None
    target: str = 'en'

class ModelInput(Input, ChoseModel):
    batch_size: Optional[int] = None