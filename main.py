
from contextlib import asynccontextmanager
from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List, Union
from typing_extensions import Annotated
import xmlrpc.client

# import stanza
# import spacy_stanza
import spacy
from lingua import Language, LanguageDetectorBuilder

from settings import settings


MODELS = {}

def detect_language(sentence):
    lang = MODELS['lingua'].detect_language_of(sentence)
    lang = {Language.ENGLISH: 'en',
            Language.SPANISH: 'es',
            Language.GERMAN: 'de',
            Language.FRENCH: 'fr',
            Language.DUTCH: 'nl'}[lang]
    return lang


def read_freqs(path):
    d = {}
    with open(path) as f:
        for line in f:
            w, freq = line.strip().split()
            d[w] = int(freq)
    total = sum(d.values())
    return {w.lower(): freq/total for w, freq in d.items()}


@asynccontextmanager
async def lifespan(app: FastAPI):
    # load models
    MODELS['nlp'] = {'en': spacy.load(settings.EN_MODEL),
                     'es': spacy.load(settings.ES_MODEL),
                     'de': spacy.load(settings.DE_MODEL),
                     'fr': spacy.load(settings.FR_MODEL),
                     'nl': spacy.load(settings.NL_MODEL)}
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
    MODELS['freqs'] = {'en': read_freqs(settings.EN_FREQS),
                       'es': read_freqs(settings.ES_FREQS),
                       'de': read_freqs(settings.DE_FREQS),
                       'fr': read_freqs(settings.FR_FREQS),
                       'nl': read_freqs(settings.NL_FREQS)}

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
    output = []
    for token in doc:

        # syllabify
        syls = MODELS['syl'].hyphenate(
            {"word": token.text, "lang": lang, "delimiter": settings.DELIMITER}
        ).split(settings.DELIMITER)

        output.append({'token': token.text,
                       'syllables': syls,
                       'lemma': token.lemma_,
                       'pos': token.pos_,
                       'dep': token.dep_,
                       'entity': token.ent_type,
                       'freq': MODELS['freqs'][lang].get(token.text.lower(), 0)})

    return {'output': output, 'meta': {'detectedLang': detected_lang, 'lang': lang}}


if __name__ == '__main__':
    import sys
    import subprocess
    import spacy

    models = [settings.EN_MODEL, settings.ES_MODEL, settings.NL_MODEL, settings.FR_MODEL, settings.DE_MODEL]
    for model in models:
        if not spacy.util.is_package(model):
            print("Installing ", model)
            subprocess.check_call([sys.executable, "-m", "spacy", "download", model])

    import uvicorn
    uvicorn.run("main:app",
                host='0.0.0.0',
                port=settings.PORT,
                reload=True,
                workers=3)