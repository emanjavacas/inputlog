
import math
import pandas as pd
from contextlib import asynccontextmanager
from fastapi import FastAPI, Query
from typing import List, Union
from typing_extensions import Annotated
import xmlrpc.client

# import stanza
# import spacy_stanza
import spacy
from lingua import Language, LanguageDetectorBuilder

from settings import settings


MODELS = {}
WEB1T = 1_024_908_267_229


def detect_language(sentence):
    lang = MODELS['lingua'].detect_language_of(sentence)
    lang = {Language.ENGLISH: 'en',
            Language.SPANISH: 'es',
            Language.GERMAN: 'de',
            Language.FRENCH: 'fr',
            Language.DUTCH: 'nl'}[lang]
    return lang


def safe_log(freq):
    if freq < 1:
        return 0
    return math.log(freq)


def read_freqs(path):
    d = {}
    with open(path) as f:
        for line in f:
            w, freq = line.strip().split()
            d[w] = int(freq)

    result_log, result_rel = {}, {}
    total = sum(d.values())
    for w, freq in d.items():
        logfreq = safe_log(freq * WEB1T / total)
        result_log[w.lower()] = logfreq
        result_rel[w.lower()] = freq / total
    return result_log, result_rel


@asynccontextmanager
async def lifespan(app: FastAPI):
    # load models
    MODELS['nlp'] = {'en': spacy.load(settings.EN.MODEL),
                     'es': spacy.load(settings.ES.MODEL),
                     'de': spacy.load(settings.DE.MODEL),
                     'fr': spacy.load(settings.FR.MODEL),
                     'nl': spacy.load(settings.NL.MODEL)}
    MODELS['syl'] = xmlrpc.client.ServerProxy(
        f"http://127.0.0.1:{settings.HYPHENATERPCPORT}")

    # language detection
    MODELS['lingua'] = LanguageDetectorBuilder.from_languages(
        Language.ENGLISH, 
        Language.DUTCH,
        Language.GERMAN, 
        Language.SPANISH,
        Language.FRENCH
    ).build()

    # freqs
    MODELS['relfreq'] = {}
    MODELS['logfreq'] = {}
    for lang in MODELS['nlp']:
        log_freq, freq_rel = read_freqs(settings.__getattribute__(lang.upper()).FREQS)
        MODELS['logfreq'][lang] = log_freq
        MODELS['relfreq'][lang] = freq_rel

    yield
    # unload models


description = """
## Introduction

The app takes sentences as input and produces an annotated document

## Use case

The input is generally specified as an xml file.
The output is an enriched version of the input xml.
"""

app = FastAPI(
    title='InputLog',
    description=description,
    summary='NLP Annotation pipeline for InputLog',
    version='0.0.1',
    lifespan=lifespan)


@app.get('/')
async def read_root():
    """
    Default dummy endpoint.
    """
    return {'message': "Hello World"}


def process_output(tokens, lang):
    output = []
    for token in tokens:

        # syllabify
        syll = MODELS['syl'].hyphenate(
            {"word": token.text, "lang": lang, "delimiter": settings.DELIMITER}
        ).split(settings.DELIMITER)

        output.append({'#Chars': len(token.text),
                       'Token': token.text,
                       'PosA': token.pos_,
                       'PosB': '-',
                       'Pos-Prob': None,
                       'Lemma': token.lemma_,
                       'Lemma-Prob': None,
                       'ChunkA': token.dep_,
                       'ChunkB': '-',
                       'NE': token.ent_type,
                       'LogFreq': MODELS['logfreq'][lang].get(token.text.lower(), 0),
                       'RelFreq': MODELS['relfreq'][lang].get(token.text.lower(), 0),
                       'Syll': '-'.join(syll)
                       })
        
    return pd.DataFrame.from_dict(output).to_csv()


@app.get('/analyze/')
async def analyze(
        sentence: Annotated[str, Query(description="Input sentence to annotate")],
        lang: Annotated[Union[str, None],
                        Query(description="Optional language of the input sentence")]=None):
    """
    General endpoint to analyze a full input text.
    """
    # input language
    detected_lang = False
    if lang is None:
        detected_lang = True
        lang = detect_language(sentence)

    # process input
    doc = MODELS['nlp'][lang](sentence)

    # prepare output
    output = process_output(doc, lang)

    return {'output': output, 'meta': {'detectedLang': detected_lang, 'lang': lang}}


if __name__ == '__main__':
    import sys
    import subprocess
    import spacy
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true')
    args = parser.parse_args()

    models = [settings.EN.MODEL, settings.ES.MODEL, settings.NL.MODEL, settings.FR.MODEL, settings.DE.MODEL]
    for model in models:
        if not spacy.util.is_package(model):
            print("Installing ", model)
            subprocess.check_call([sys.executable, "-m", "spacy", "download", model])

    import uvicorn
    uvicorn.run("main:app",
                host='0.0.0.0',
                port=settings.PORT,
                reload=args.debug,
                workers=3)