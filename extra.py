import requests
from bs4 import BeautifulSoup
import re
import spacy
import random
import string


freq_table = {}
first = set()
end = set()


class Freq_map:
    def __init__(self):
        self.map = {}

    def put(self, word):
        if word in self.map:
            self.map[word] += 1
        else:
            self.map[word] = 1

    def contains(self, word):
        return word in self.map

    def rand(self):
        sum = 0
        for value in self.map.values():
            sum += value

        rand_num = random.randrange(sum)
        for key in self.map.keys():
            if rand_num <= self.map[key]:
                return key
            else:
                rand_num -= self.map[key]

    def __repr__(self):
        return str(self.map)


def clean_poem(text):
    ending_punc = {'.', '!', '?', ';', '"'}
    all_words = text.split()
    splitted = []
    i = 1
    first.add(all_words[i])
    while i < len(all_words):
        word = all_words[i]
        i += 1
        first_letter = word[0]
        last_letter = word[len(word)-1]
        if last_letter in ending_punc:
            if first_letter.isalpha():
                end.add(word)
                splitted.append(word)
            else:
                continue
        else:
            if first_letter.isalpha():
                splitted.append(word)
                if all_words[i-1] in end:
                    first.add(word)
    return splitted


def store(splitted):
    for i in range(len(splitted) - 1):
        cur = splitted[i].lower()
        next = splitted[i+1].lower()
        if cur in freq_table:
            freq_table[cur].put(next)
        else:
            freq_table[cur] = Freq_map()
            freq_table[cur].put(next)


def gen(word, splitted):
    store(splitted)
    s = word
    i = 100
    last = word
    while i > 0:
        while (last not in end) and (last + "." not in end) and (last + "," not in end) and (last + ";" not in end):
            next = freq_table[last].rand()
            s = s + " " + next
            last = next
        s += "\n"
        i -= 1
        last = random.choice(list(first))

    lines = s.split("\n")
    fitness_check(word, lines)
    lines.sort(key=lambda line: scores.get(line), reverse=True)
    weight = []
    for line in lines:
        weight.append(scores[line])
    final = random.choices(lines, weights=weight, k=7)
    special_print(final)


def check_gram(all_lines):
    nlp = spacy.load('en_core_web_md')
    for line in all_lines:
        r = []
        for k in nlp(line):
            r.append(k.tag_)
        print(r)
