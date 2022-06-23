from typing import Set
from dataclasses import dataclass
from toolz.curried import pipe, map, reduce

from parsec import Parser, sepBy1, spaces, string, choice, optional

def margin(expr: Parser):
    return spaces() >> expr << spaces()

def variable(variables: Set[str]) -> Parser:
    return pipe(
        variables,
        map(string),
        reduce(choice)
    )

def negation(expr: Parser) -> Parser:
    return optional(string("-")) >> expr

def literal(variables: Set[str]) -> Parser:
    return negation(variable(variables))

def conjunction(expr: Parser) -> Parser:
    return sepBy1(expr, string("*"))


def disjunction(expr: Parser) -> Parser:
    return sepBy1(expr, string("+"))


def disjunctive_normal_form(variables: Set[str]):
    return disjunction(
        conjunction(
            margin(literal(variables))
        )
    )

def conjunctive_normal_form(variables: Set[str]):
    return conjunction(
        disjunction(
            margin(literal(variables))
        )
    )
