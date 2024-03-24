### SERVER CONFIGURATION VARIABLES
SERVER_DETECTION_TIMEOUT = 0.2


### MODEL VARIABLES
EVALUATION_SYS_PROMPT = """You are a useful code assistant. A user will give you a code representing a python file. 
Your task is to take said code and generate a complete working testing file using Pytest. 
You may assume the original code can be found in a `source.py` file residing in the same directory as the test file, you must import it as such.
The user may further provide you with the pytest output after running the code you provided if there's any errors, in which case, you must return the fully updated and working test file.
If there are no errors, try to increase coverage as much as possible by updating the tests.
You *MUST* always provide the fully updated code with no other explanations. 
"""


### DUMMY VARIABLES FOR TESTING
dummy_code = """def maxCntRemovedfromArray ( arr , N , brr , M ) :
    arr . sort ( reverse = False )
    i = 0
    sumArr = 0
    for i in range ( N ) :
        sumArr += arr [ i ]
    sumBrr = 0
    for i in range ( M ) :
        sumBrr += brr [ i ]
    cntRemElem = 0
    while ( i < N and sumArr >= sumBrr ) :
        sumArr -= arr [ i ]
        i += 1
        if ( sumArr >= sumBrr ) :
            cntRemElem += 1
    return cntRemElem
if __name__ == '__main__' :
    arr = [ 1 , 2 , 4 , 6 ]
    brr = [ 7 ]
    N = len ( arr )
    M = len ( brr )
    print ( maxCntRemovedfromArray ( arr , N , brr , M ) )
    """

dummy_pytest_file = """from source import *
import pytest

def test_maxCntRemovedfromArray():
    arr = [1, 2, 4, 6]
    brr = [7]
    N = len(arr)
    M = len(brr)
    assert maxCntRemovedfromArray(arr, N, brr, M) == 2

def test_maxCntRemovedfromArray_empty_array():
    arr = []
    brr = [7]
    N = len(arr)
    M = len(brr)
    assert maxCntRemovedfromArray(arr, N, brr, M) == 0

def test_maxCntRemovedfromArray_large_input():
    arr = [i for i in range(1, 10 ** 5 + 1)]
    brr = [7] * 10 ** 5
    N = len(arr)
    M = len(brr)
    assert maxCntRemovedfromArray(arr, N, brr, M) == 1
    """
