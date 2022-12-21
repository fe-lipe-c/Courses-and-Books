"""Notebook to Lecture1 of the course."""

from nltk.corpus import wordnet as wn

# Synonyms sets containing the word
posed = {"n": "noun", "v": "verb", "s": "adj (s)", "a": "adj", "r": "adv"}

word = "dog"

for synset in wn.synsets(word):
    print(
        "(",
        posed[synset.pos()],
        ")",
        synset.lemmas()[0].name(),
        ":",
        synset.definition(),
    )

for synset in wn.synsets(word):
    print(
        "{0}: ({1})".format(
            posed[synset.pos()], ", ".join([l.name() for l in synset.lemmas()])
        )
    )

synset.lemmas()[0].name()

# Hypernyms of the word

word = "machine.n.01"
hypernyms = lambda s: s.hypernyms()
hy_list = list(wn.synset(word).closure(hypernyms))
hy_list = [hy.lemmas()[0].name() for hy in hy_list]
hy_list
