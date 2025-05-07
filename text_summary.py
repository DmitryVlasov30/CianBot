import nltk
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer

def summy_message(text):
    nltk.download('punkt_tab')

    parser = PlaintextParser.from_string(text, Tokenizer("russian"))
    summarizer = TextRankSummarizer()

    summary = summarizer(parser.document, 3)  # получить 2 предложения

    return summary
