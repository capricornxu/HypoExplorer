### import modules
import sys
import time
import re
import sqlite3
import pandas as pd
import os
import json
import nltk
from nltk.parse.generate import generate, demo_grammar
from nltk import CFG
from nltk.parse.chart import demo_grammar
from nltk.parse.earleychart import EarleyChartParser, perf_counter
import flask
from flask import Flask, request
from flask_cors import CORS

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
    
    # parses = chart.parses(grammar.start())
    return parses


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
def data_to_json(
    data,
    filename
):
    with open(filename, "w") as file:
        json.dump(data, file, indent = 2)


### Find deterministic tree
def tree_to_dict(tree):
    if isinstance(tree, nltk.Tree):
        return {'root': tree.label(), 
                'subtrees': [tree_to_dict(child) for child in tree]}
    else:
        return  {'root': tree, 'subtrees': []}

def findDeterministicTree(
    grammar
):
    # get lhs list of the grammar
    productions = grammar.productions()
    lhs_list = [prod.lhs() for prod in productions]

    # get the new lhs list of the deterministic tree
    new_lhs_list = []

    for lhs in lhs_list:
        if lhs_list.count(lhs) == 1:
            new_lhs_list.append(str(lhs))

    # join lhs in new_lhs_list with its rhs
    new_production_dict = {}
    for prod in productions:
        if(str(prod.lhs()) in new_lhs_list):
            rhs_list = []
            for rhs in prod.rhs():
                rhs_list.append(str(rhs))
            new_production_dict.update({str(prod.lhs()):rhs_list})

    # create new hypo_string for deterministic tree
    hypo_string = ""
    for lhs, rhs_list in new_production_dict.items():
        curr_string = lhs + " -> "
        for rhs in rhs_list:
            if not rhs in new_lhs_list:
                curr_string = curr_string + " " + "'" + rhs + "'"
            else:
                curr_string = curr_string + " " + rhs
        hypo_string = hypo_string + curr_string + "\n"


    # create grammar from hypo_string
    new_grammar = CFG.fromstring(hypo_string)

    # get deterministic tree
    for sentence in generate(new_grammar):
        deterministic_sent = ' '.join(sentence)

    deterministic_tree = parser(sent = deterministic_sent, grammar  = new_grammar)

    tree_dict = tree_to_dict(deterministic_tree[0])

    return deterministic_sent, tree_dict