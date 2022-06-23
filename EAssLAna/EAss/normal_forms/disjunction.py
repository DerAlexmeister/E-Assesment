from typing import Set
from toolz.curried import pipe, map, reduce

from parsec import Parser, sepBy1, spaces, string, choice


def margin(parser: Parser):
    return spaces() >> parser << spaces()

def variable(variables: Set[str]) -> Parser:
    return pipe(
        variables,
        map(string),
        reduce(choice)
    )


def conjunction(expr: Parser) -> Parser:
    return sepBy1(expr, string("*"))


def disjunction(expr: Parser) -> Parser:
    return sepBy1(expr, string("+"))


def disjunctive_normal_form(variables: Set[str]):
    return disjunction(
        conjunction(
            margin(variable(variables))
        )
    )
