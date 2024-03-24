def maxCntRemovedfromArray(arr, N, brr, M):
    arr.sort(reverse=False)
    i = 0
    sumArr = 0
    for i in range(N):
        sumArr += arr[i]
    sumBrr = 0
    for i in range(M):
        sumBrr += brr[i]
    cntRemElem = 0
    while i < N and sumArr >= sumBrr:
        sumArr -= arr[i]
        i += 1
        if sumArr >= sumBrr:
            cntRemElem += 1
    return cntRemElem


if __name__ == "__main__":
    arr = [1, 2, 4, 6]
    brr = [7]
    N = len(arr)
    M = len(brr)
    print(maxCntRemovedfromArray(arr, N, brr, M))
