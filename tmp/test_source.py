import pytest
from source import maxCntRemovedfromArray


def test_maxCntRemovedfromArray():
    arr = [1, 2, 4, 6]
    brr = [7]
    N = len(arr)
    M = len(brr)
    assert maxCntRemovedfromArray(arr, N, brr, M) == 3
