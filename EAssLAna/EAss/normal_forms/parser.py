from typing import Set
from toolz.curried import pipe, map, reduce

from parsec import Parser, eof, one_of, sepBy1, spaces, string, choice

from .normal_form import Literal, NormalForm

def margin(expr: Parser):
    return spaces() >> expr << spaces()

def variable(variables: Set[str]) -> Parser:
    return one_of(variables)\
        .desc(f"Expected variables {', '.join(v for v in variables)}.")

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


def normal_form(outer, inner, variables: Set[str]):
    return outer(
        inner(
            margin(literal(variables))
        )
    ).parsecmap(NormalForm)

def disjunctive_normal_form(variables: Set[str]):
    return normal_form(disjunction, conjunction, variables)

def conjunctive_normal_form(variables: Set[str]):
    return normal_form(conjunction, disjunction, variables)
