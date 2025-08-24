# from sentence_transformers import SentenceTransformer
from enum import StrEnum

class ModelNameEnum( StrEnum):
    """
    List of available models - https://sbert.net/docs/sentence_transformer/pretrained_models.html
    """
    ALL_MINILM_L6_V2 = "all-MiniLM-L6-v2"
    ROBERTA_BASE_NLI_STSB_MEAN_TOKENS = "roberta-base-nli-stsb-mean-tokens"
    DISTILBERT_BASE_NLI_STSB_MEAN_TOKENS = "distilbert-base-nli-stsb-mean-tokens"
    BERT_BASE_NLI_MEAN_TOKENS = "bert-base-nli-mean-tokens"
