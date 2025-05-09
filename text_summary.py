from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer

def summy_message(text):
    parser = PlaintextParser.from_string(text, Tokenizer("russian"))
    summarizer = TextRankSummarizer()

    summary = summarizer(parser.document, 3)
    text_ads = ""
    for sentence in summary:
        text_ads += str(sentence) + "\n"
    return text_ads
