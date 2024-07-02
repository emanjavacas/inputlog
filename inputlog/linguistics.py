
import logging

import stanza
import spacy
import benepar

logger = logging.getLogger(__name__)


def collect_labels(root):
    q = [((None, ), root)]
    while q:
        prefix, (parent, *children) = q.pop()
        prefix = prefix + tuple([parent])
        if all([isinstance(c, str) for c in children]): # leaf
            yield prefix, children
        else:
            for child in children:
                q.append((prefix, child))


def tokenize(tree_string):
    return tree_string.replace('(', ' ( ').replace(')', ' ) ').split()


def read_from_tokens(tokens):
    if len(tokens) == 0:
        raise SyntaxError("unexpected EOF")
    token = tokens.pop(0)
    if token == '(':
        L = []
        while tokens[0] != ')':
            L.append(read_from_tokens(tokens))
        tokens.pop(0)
        return L
    elif token == ')':
        raise SyntaxError("unexpected )")
    else:
        return token


def parse_tree_string(string):
    return read_from_tokens(tokenize(string))


def add_chunks(tree_string, tokens):
    i, last_label = 0, None
    for prefix, word in list(collect_labels(parse_tree_string(tree_string)))[::-1]:
        # double checking
        assert word[0] == tokens[i]['Token'], (word[0], tokens[i]['Token'])
        # select where to pick the label from (hack)
        if prefix[-2] == 'S':
            label = prefix[-1]
        else:
            label = prefix[-2]
        tokens[i]['ChunkB'] = label
        if label == last_label:
            tokens[i]['ChunkA'] = 'I'
        else:
            tokens[i]['ChunkA'] = 'B'
        i, last_label = i + 1, label


class LinguisticsModel:
    def __init__(self) -> None:
        self.settings = {}
        self.background_models = {}

    def load(self, settings):
        for language in settings.languages:
            logger.info("Loading background model for language '{}' from path '{}'...".format(
                language.language, language.model_path))
            # store settings
            self.settings[language.language] = language
            # spacy loading
            if language.model == 'spacy':
                self.background_models[language.language] = spacy.load(language.model_path)
                if language.constituency == 'benepar':
                    logger.info("Adding 'benepar' constituency parser to language '{}' from '{}'".format(
                        language.language, language.constituency_path))
                    self.background_models[language.language].add_pipe(
                        'benepar', config={'model': language.constituency_path})
                else:
                    logger.info("No constituency model available for language: {}".format(
                        language.language))
            # stanza loading
            elif language.model == 'stanza':
                assert language.constituency == 'stanza', "Expected constituency model to be 'stanza'"
                self.background_models[language.language] = stanza.Pipeline(language.model_path)
            else:
                raise ValueError("Unknown config - language: {}, model: {}".format(
                    language.language, language.model))
            
    def process_text(self, text, language):
        output = []
        doc = self.background_models[language](text)
        # spacy
        if self.settings[language].model == 'spacy':
            for sent in doc.sents:
                tokens = get_tokens_spacy(sent)
                if self.settings[language].constituency is not None:
                    add_chunks(sent._.parse_string, tokens)
                output.extend(tokens)
        else: # stanza
            for sent in doc.sentences:
                tokens = get_tokens_stanza(sent)
                if self.settings[language].constituency is not None:
                    add_chunks(str(sent.constituency), tokens)
                output.extend(tokens)

        return output


def get_tokens_spacy(sent):
    tokens = []
    for token in sent:
        token = {'Token': token.text,
                 'PosA': token.pos_,
                 'PosB': '-',
                 'Pos-Prob': None,
                 'Lemma': token.lemma_,
                 'Lemma-Prob': None,
                 'NE': token.ent_type,
                 'ChunkA': 'O',
                 'ChunkB': '-'}
        tokens.append(token)
    return tokens


def get_tokens_stanza(sent):
    tokens = []
    for token in sent.tokens:
        token = token.to_dict()[0]
        token = {'Token': token['text'],
                 'PosA': token['upos'],
                 'PosB': '-',
                 'Pos-Prob': None,
                 'Lemma': token['lemma'],
                 'Lemma-Prob': None,
                 'NE': token['ner'],
                 'ChunkA': 'O',
                 'ChunkB': '-'}
        tokens.append(token)
    return tokens


MODEL = LinguisticsModel()