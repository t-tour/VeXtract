from helper import logger
log = logger.Logger(__name__)

import argparse
import json
import sys

import googleapiclient.discovery


def get_native_encoding_type():
    """Returns the encoding type that matches Python's native strings."""
    if sys.maxunicode == 65535:
        return 'UTF16'
    else:
        return 'UTF32'


def analyze_sentiment(text, encoding='UTF32'):
    body = {
        'document': {
            'type': 'PLAIN_TEXT',
            'content': text,
        },
        'encoding_type': encoding
    }

    service = googleapiclient.discovery.build('language', 'v1')

    request = service.documents().analyzeSentiment(body=body)
    response = request.execute()

    return response


def text_analyze(text):
    result = analyze_sentiment(text)
    sentiment = result['documentSentiment']
    log.i('text: {} score: {} analyzed...'.format(text, sentiment['score']))
    return sentiment['score']


if __name__ == '__main__':
    x = "這是一個測試的句子"
    print('請輸入要分析的句子：這是一個測試的句子')
    score = text_analyze(x)
    print("情緒分數為：", score)
