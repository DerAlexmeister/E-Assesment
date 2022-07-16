import pandas as pd
from itertools import product

from dataclasses import dataclass
from typing import Set, Tuple, List


from ..normal_forms.normal_form import TruthTable


def to_str(x: bool, y: bool) -> str:
    return f"{int(x)}{int(y)}"

@dataclass
class Karnaugh:
    ones: Set[Tuple[(bool, bool, bool, bool)]]

    def __repr__(self) -> str:
        x = ["00", "01", "11", "10"]
        y = ["01", "00", "10", "11"]


        data = pd.DataFrame(0, index=y, columns=x)
        for a, b, c, d in self.ones:
            data.loc[to_str(c, d), to_str(a, b)] = 1
        return str(data)


def fromTruthTable(formula: TruthTable) -> Karnaugh:
    ones = set()
    for _, assignment in formula.table[formula.results==1].iterrows():
        ones.add(tuple(bool(b) for b in assignment.iloc[:4]))
    return Karnaugh(ones)


def to_json(karnaugh: Karnaugh) -> List[str]:
    print(karnaugh)
    return [
        "".join(
            str(int(
                tuple(bool(b) for b in x + y)\
                in karnaugh.ones
            ))
            for x in [(0, 0), (0, 1), (1, 1), (0, 1)]
        )
        for y in [(0, 1), (0, 0), (1, 0), (1, 1)]
    ]

def from_json(json: List[str]) -> Karnaugh:
    return Karnaugh({
        tuple(bool(int(s)) for s in string[:4])
        for string in json
    })
