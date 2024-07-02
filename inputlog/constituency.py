
from nltk.tree import Tree
import benepar
import spacy
import stanza
import spacy_stanza
from inputlog.settings import settings

from pyparsing import nested_expr

en = next(filter(lambda l: l.language=='en', settings.languages))

nlp = spacy.load(en.model_path)
nlp.add_pipe('benepar', config={'model': 'benepar_en3'})

def collect_labels(root):
    q = [((None, ), root)]
    while q:
        label, node = q.pop()
        if node.is_leaf():
            yield label, node
        for child in node.children:
            (node.label, label)
            q.append((label + tuple((node.label,)), child))

def collect_labels(root):
    q = [((None, ), root)]
    while q:
        prefix, (parent, *children) = q.pop()
        prefix = prefix + tuple([parent])
        print(children)
        if all([isinstance(c, str) for c in children]): # leaf
            yield prefix, children
        else:
            for child in children:
                q.append((prefix, child))

tree = nested_expr('(', ')').parse_string(tree_string).as_list()[0]
list(collect_labels(tree))[::-1]
tree[2]

dir(tree)
list(collect_labels(tree))
dir(tree)
list(tree.subtrees())


def get_constituents(root):
    output = []
    for labels, leaf in collect_labels(root):
        pass

es_text = 'Esta frase está en Español, también conocido como idioma castellano.'
es_text = 'Este es un texto escrito en verso.'
en_text = 'There is a man sleeping in an easy chair.'
doc = nlp(en_text)
tree_string = list(doc.sents)[0]._.parse_string
tree = Tree.fromstring()
tree.
root = doc.sentences[0].constituency.children[0]
list(collect_labels(root.reverse()))


# Stanza (for Spanish)
stanza.download('es')
# model = spacy_stanza.load_pipeline('es')
language = next(filter(lambda l: l.language == 'en', settings.languages))
model = stanza.Pipeline(language.language)
# model = spacy.load(settings.ES.MODEL_PATH)
es_text = 'Esta frase está en Español, también conocido como idioma castellano.'
es_text = 'Este es un texto escrito en verso.'
doc = model(es_text)
for tok in doc.sentences[0].tokens:
    print(tok.to_dict()[0])
for token in doc:
    print(token.text, token.pos_, token.tag_)
doc.sentences[0].constituency.leaf_labels()
for preterm in doc.sentences[0].constituency.yield_preterminals():
    preterm
    dir(preterm)

doc.sentences[0].constituency.children[0].label
doc.sentences[0].constituency.children[0].children[0]
# Benepar (for EN, DE, FR)
nlp = spacy.load(settings.EN.MODEL_PATH)
benepar.download(settings.EN.CONSTITUENCY_PATH)
nlp.add_pipe("benepar", config={"model": settings.EN.CONSTITUENCY_PATH})
en_text = 'This is an English sentence for you in order to test the models. This is a second sentence.'
doc = nlp(en_text)
list(doc.sents)
for sent in doc.sents:
    print(sent._.parse_string + '\n')

for token in doc:
    print(token._.labels)
next(doc.sents)._.parse_string
doc._.parse_string
token._.labels

list(sent.noun_chunks)
nlp2 = spacy.load(settings.EN.MODEL_PATH)
for sent in nlp2(en_text).sents:
    for tok in sent:
        print
        # print(tok.ent_id)
sent._.parse_string
dir(tok)

# For Dutch?