
import logging
from contextlib import asynccontextmanager

import pandas as pd

from fastapi import FastAPI, Query
from typing import Union, List
from typing_extensions import Annotated

from inputlog.language_detection import MODEL as LanguageDetector
from inputlog.frequency import MODEL as FreqModel
from inputlog.linguistics import MODEL as LinguisticsModel
from inputlog.hyphenation import MODEL as HyphenationModel
from inputlog.settings import settings, setup_logger


setup_logger()
logger = logging.getLogger(__name__)


description = """
## Introduction

The app takes sentences as input and produces an annotated document

## Use case

The input is generally specified as an xml file.
The output is an enriched version of the input xml.
"""

@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.needs_language_detection:
        LanguageDetector.load(settings)
    LinguisticsModel.load(settings)
    FreqModel.load(settings)
    HyphenationModel.load(settings)
    yield


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
    return {'message': "InputLog Linguistic Analysis Service"}


class InvalidColsException:
    pass


def validate_cols(payload, cols):
    


def postprocess_output(tokens, cols, lang):
    output = []
    for token_data in tokens:
        # syllabify
        syll = HyphenationModel.hyphenate(token_data['Token'], lang)
        # frequency data
        log_freq, rel_freq = FreqModel.get_freqs(token_data['Token'].lower(), lang)

        output.append(dict(token_data, **{
            # other info
            'LogFreq': log_freq,
            'RelFreq': rel_freq,
            'Syll': '-'.join(syll),
            '#Chars': len(token_data['Token'])}))

    payload = pd.DataFrame.from_dict(output)

    return payload.to_csv(index=None, )


@app.get('/analyze/')
async def analyze(
        text: Annotated[str, Query(description="Input sentence to annotate")],
        lang: Annotated[Union[str, None], Query(description="Optional language of the input sentence")]=None,
        cols: Annotated[Union[List[str], None], Query(description="Optional list to specify the desired order of the columns in the output")]=None):
    """
    General endpoint to analyze a full input text.
    """
    # input language
    detected_lang = lang is None
    if settings.needs_language_detection:
        lang = lang or LanguageDetector.detect_language(text)
    else:
        lang = settings.default_language
    # processing
    payload = LinguisticsModel.process_text(text, lang)
    output = postprocess_output(payload, cols, lang)

    return {'output': output, 'meta': {'detectedLang': detected_lang, 'language': lang}}


if __name__ == '__main__':
    import sys
    import subprocess
    import argparse
    import spacy
    import stanza
    import benepar

    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true')
    args = parser.parse_args()

    for language in settings.languages:
        if language.model == 'spacy' and not spacy.util.is_package(language.model_path):
            logger.info("Installing spacy model: {} for language: {}".format(language.model_path, language.language))
            subprocess.check_call([sys.executable, "-m", "spacy", "download", language.model_path])
        if language.constituency == 'benepar':
            logger.info("Checking benepar model: {} for language: {}".format(language.model_path, language.language))
            benepar.download(language.constituency_path)
        if language.model == 'stanza':
            logger.info("Checking stanza model: {} for language: {}".format(language.model_path, language.language))
            stanza.Pipeline(language.language)

    import uvicorn
    uvicorn.run("main:app",
                host='0.0.0.0',
                port=settings.port,
                reload=args.debug,
                workers=3)
