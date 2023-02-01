### import libraries
import nltk
from nltk.parse.generate import generate, demo_grammar
from nltk import CFG
from nltk.parse import ShiftReduceParser
import sys
import time
from nltk.parse.chart import demo_grammar
from nltk.parse.earleychart import EarleyChartParser, perf_counter
import re
import sqlite3
import csv
import pandas as pd
import os
import json

### Hypothesis Parser
def parser(
    print_times=False,
    print_grammar=False,
    print_trees=True,
    trace=2,
    sent=" ",
    grammar = demo_grammar(),
):
    ################
    # This is the parser for hypothesis grammar. 
    # It uses Earley Parser algorithm to do the parsing.
    ################
    # print_times: if True, print the parsing time
    # print_grammar: if True, print the input grammar
    # trace: to what extend a user want to trace the parse chart
    # sent: input sentence
    # grammar: input grammar used to parse sent

    # The grammar for ChartParser and SteppingChartParser:
    if print_grammar:
        print("* Grammar")
        print(grammar)

    # Tokenize the sample sentence.
    print("* Sentence:\n")
    print(sent)
    tokens = sent.split()
    print("\n* Tokens:\n")
    print(tokens)
    print()

    # Do the parsing.
    earley = EarleyChartParser(grammar, trace=trace)
    t = perf_counter()
    chart = earley.chart_parse(tokens)
    parses = list(chart.parses(grammar.start()))
    t = perf_counter() - t

    # Print results.
    assert len(parses) != 0, "Invalid Input"
    if print_trees:
        print("* PARSE TREE\n")
        for tree in parses:
            print(tree)
    else:
        print("Nr trees:", len(parses))
    if print_times:
        print("Time:", t)
        
    return parses[0][0]


### Hypothesis Iterator
def Iterator(
    grammar,
    num = 10
):
    sent_dict = {}
    index = 0
    for sentence in generate(grammar, n = num):
        sent = str(' '.join(sentence))
        evaluation = 1
        dictionary = {"sentence": sent,"evaluation":1}
        sent_dict.update({index: dictionary})
        index = index + 1
        # print([str(' '.join(sentence))])
    
    return sent_dict

### Write data to JSON file
def sentence_to_json(
    data,
    filename
):
    with open(filename, "w") as file:
        json.dump(data, file)