from typing import Set
from toolz.curried import pipe, map, reduce

from parsec import Parser, sepBy1, spaces, string, choice

from .normal_form import Literal, NormalForm

def margin(expr: Parser):
    return spaces() >> expr << spaces()

def variable(variables: Set[str]) -> Parser:
    return pipe(
        variables,
        map(string),
        reduce(choice)
    )

def negative(expr: Parser) -> Parser:
    return (string("-") >> expr)\
        .parsecmap(lambda v: Literal(v, False))

def positive(expr: Parser) -> Parser:
    return expr\
        .parsecmap(lambda v: Literal(v, True))

def literal(variables: Set[str]) -> Parser:
    parser = variable(variables)
    return negative(parser) | positive(parser)

def conjunction(expr: Parser) -> Parser:
    return sepBy1(expr, string("*"))


def disjunction(expr: Parser) -> Parser:
    return sepBy1(expr, string("+"))


def disjunctive_normal_form(variables: Set[str]):
    return disjunction(
        conjunction(
            margin(literal(variables))
        )
    ).parsecmap(NormalForm)

def conjunctive_normal_form(variables: Set[str]):
    return conjunction(
        disjunction(
            margin(literal(variables))
        )
    ).parsecmap(NormalForm)
