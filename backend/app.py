from flask import Flask, request
import flask
import json
from flask_cors import CORS

from funcs import *

hypo_string = """
    root -> hypo
    hypo -> expr '[' pred ']' op expr '[' pred ']'
    expr -> func '(' var ')' | var
    var -> attr | const
    pred -> var op const | pred '&' pred | 
    op -> '=' | '<'
    attr -> 'customer_id' | 'first_name' | 'last_name' | 'age' | 'country'
    const -> '1' | '2' | '3' | '4' | '5' | '22' | '25' | '28' | '31' 
    const -> "\'Robert\'" | "\'John\'" | "\'David\'" | "\'Betty\'" | "\'Doe\'" | "\'Luna\'" | "\'Robinson\'" | "\'Reinhartd\'" | "\'USA\'" | "\'UK\'" | "\'UAE\'"
    func -> 'AVG' | 'MAX' | 'MIN' | 'COUNT'
    """

if __name__ == "__main__":
    grammar = CFG.fromstring(hypo_string)
    sentence = "first_name [ customer_id = 2 ] = 'Robert' [ ]"
    parse_tree = parser(sent = sentence, trace = 0, grammar = grammar)
    