import re


def validate_python_code(code_str):
    try:
        compile(code_str, "<string>", "exec")
        return True
    except:
        return False


def extract_code_from_string(input_text):
    code_blocks = re.findall(r"`{3}(?:\n)?(?:python)?(.*?)`{3}", input_text, re.DOTALL)
    code_blocks = [code.strip() for code in code_blocks]
    code_blocks = [code for code in code_blocks if validate_python_code(code)]

    if code_blocks:
        return max(code_blocks, key=len)
    elif validate_python_code(input_text):
        return input_text
    else:
        return ""


if __name__ == "__main__":
    dummy_input = "```python\ndef test_maxCntRemovedfromArray():\n    def maxCntRemovedfromArray(arr, N, brr, M):\n        # Your original code here\n        pass \n\n    arr = [1, 2, 4, 6]\n    brr = [7]\n    N = len(arr)\n    M = len(brr)\n    assert maxCntRemovedfromArray(arr, N, brr, M) == 3\n```"
    # dummy_input = """import pytest\ndef test_maxCntRemovedfromArray():\n    def maxCntRemovedfromArray(arr, N, brr, M):\n        arr.sort(reverse=False)\n        i = 0\n        sumArr = 0\n        for i in range(N):\n            sumArr += arr[i]\n        sumBrr = 0\n        for i in range(M):\n            sumBrr += brr[i]\n        cntRemElem = 0\n        while (i < N and sumArr >= sumBrr):\n            sumArr -= arr[i]\n            i += 1\n            if (sumArr >= sumBrr):\n                cntRemElem += 1\n        return cntRemElem\n    assert maxCntRemovedfromArray(arr, N, brr, M) == 2\n    assert maxCntRemovedfromArray([2, 4], 2, [7], 1) == 2\n    assert maxCntRemovedfromArray([3, 5, 6, 8], 4, [4, 9, 9], 3) == 0\n    \n### Explanation:\nI have added a new function called `test_maxCntRemovedfromArray` and imported the function from the original file. I then created three test cases to test the function with different inputs. The first test case tests the function with the given input `arr = [1, 2, 4, 6]`, `brr = [7]`, `N = len(arr)` and `M = len(brr)`. The second test case tests the function with the input `arr = [2, 4]`, `brr = [7]`, `N = len(arr)` and `M = len(brr)`. The third test case tests the function with the input `arr = [3, 5, 6, 8]`, `brr = [4, 9, 9]`, `N = len(arr)` and `M = len(brr)`.\nI have used the assert statement to check if the output of the function is as expected for each test case. If any of the tests fail, I will update the original code with the new test cases until all tests pass."""

    print(dummy_input)
    print(f"<{extract_code_from_string(dummy_input)}>")
