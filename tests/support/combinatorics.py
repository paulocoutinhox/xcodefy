from collections.abc import Sequence
from itertools import chain, combinations, permutations
from typing import Any


class Combinatorics:
    @staticmethod
    def subsets(values: Sequence[Any]) -> list[tuple[Any, ...]]:
        return list(chain.from_iterable(combinations(values, size) for size in range(len(values) + 1)))

    @staticmethod
    def subset_permutations(values: Sequence[Any]) -> list[tuple[Any, ...]]:
        return [permutation for subset in Combinatorics.subsets(values) for permutation in permutations(subset)]

    @staticmethod
    def subset_permutation_joinings(values: Sequence[str]) -> list[str]:
        return ["".join(permutation) for permutation in Combinatorics.subset_permutations(values)]
