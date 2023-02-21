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
    num = None
):
    sent_dict = {}
    index = 0
    for sentence in generate(grammar, n = num):
        sent = str(' '.join(sentence))
        # sentence evaluation
        eval = evaluation(sent, grammar)
        dictionary = {"sentence": sent,"evaluation":eval}
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


### evaluate sentence
def evaluation(
    sentence,
    grammar
):
    ### Load database
    database = "Customers.db"

    sql_create_table = """CREATE TABLE IF NOT EXISTS Customers (
                        customer_id integer PRIMARY KEY,
                        first_name varchar[100],
                        last_name varchar[100],
                        age integer NOT NULL,
                        country varchar[100]
                    );"""

    # create a database connection
    os.remove("Customers.db")
    conn = sqlite3.connect(database)

    # create table
    if conn is not None:
        c = conn.cursor()
        c.execute(sql_create_table)
        df = pd.read_csv("Customers.csv")
        df.to_sql('Customers', conn, if_exists='append', index=False)
        conn.close()
    
    # transformation
    sql_template = """
    SELECT DISTINCT
    ( SELECT expr1 FROM Customers WHERE pred1 )
    =
    ( SELECT expr2 FROM Customers WHERE pred2 )
    FROM Customers
    """

    parse_tree = parser(sent = sentence, trace = 0, grammar = grammar)
    sql = hypo_to_sql(sql_template, parse_tree[0][0])

    ### Load database
    sql_text = sql

    # create a database connection
    conn = sqlite3.connect(database)

    # create table
    if conn is not None:
        c = conn.cursor()
        c.execute(sql_text)
        print("* Evaluation Result\n")
        eval = c.fetchall()[0][0]
        if eval == 1:
            print(True)
        else:
            print(False)

    return eval

# transform hypothesis to sql text
def hypo_to_sql(
    sql_template, 
    parse_tree
):
    expr_list = []
    pred_list = []
    op = '='

    for subtree in parse_tree:
        if not isinstance(subtree, str):
            if subtree.label() == 'expr':
                expr = ' '.join(subtree.leaves())
                expr_list.append(expr)
            if subtree.label() == 'pred':
                if subtree.leaves() == []:
                    pred = ' '.join(['true'])
                else:
                    pred = ' '.join(subtree.leaves())
                pred_list.append(pred)
            if subtree.label() == 'op':
                op = subtree.leaves()

    print("\n* SQL TEXT")
    sql = sql_template.replace('expr1', expr_list[0])
    sql = sql.replace('expr2', expr_list[1])
    sql = sql.replace('pred1', pred_list[0])
    sql = sql.replace('pred2', pred_list[1])
    sql = sql.replace('op', op[0])
    print(sql)
    
    return sql