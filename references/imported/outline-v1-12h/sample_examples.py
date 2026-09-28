"""列表样片的独立演示与答案核对。Python 3，无第三方依赖。"""
def select_greater(nums, threshold):
    result = []
    for n in nums:
        if n > threshold:
            result.append(n)
    return result

def verify():
    a = [2, 4]
    assert a.append(6) is None and a == [2, 4, 6]
    a = [2, 4]
    a.append([6, 8])
    assert a == [2, 4, [6, 8]] and len(a) == 3
    a = [2, 4]
    assert a.extend([6, 8]) is None and a == [2, 4, 6, 8]
    b = [1]
    b.extend("ab")
    assert b == [1, "a", "b"]
    a = [8, 3, 8, 5]
    assert a.remove(8) is None and a == [3, 8, 5]
    a = [8, 3, 8, 5]
    x = a.pop(1)
    assert x == 3 and a == [8, 8, 5]
    a = [8, 3, 8, 5]
    assert a.pop() == 5 and a == [8, 3, 8]
    for action, expected in [
        (lambda: [1].append(2, 3), TypeError),
        (lambda: [1].remove(9), ValueError),
        (lambda: [1].pop(9), IndexError),
        (lambda: [].pop(), IndexError),
    ]:
        try:
            action()
        except expected:
            pass
        else:
            raise AssertionError("预期错误未发生")
    a = [6, 2, 6, 9]
    a.remove(6)
    x = a.pop(0)
    assert x == 2 and a == [6, 9]
    nums = [5, 8, 12, 7, 10]
    evens = []
    for n in nums:
        if n % 2 == 0:
            evens.append(n)
    assert evens == [8, 12, 10]
    for n in nums:
        evens = []
        if n % 2 == 0:
            evens.append(n)
    assert evens == [10]  # 故意错误版本
    assert select_greater([6, 9, 2, 14, 9], 8) == [9, 14, 9]
    assert select_greater([1, 2], 8) == []
    assert select_greater([], 8) == []
    assert select_greater([9, 11], 8) == [9, 11]
    a = [1, 3]
    a.append([5, 7])
    assert a == [1, 3, [5, 7]] and len(a) == 3
    a = [1, 3]
    r = a.extend([5, 7])
    assert a == [1, 3, 5, 7] and r is None
    a = [4, 2, 4, 9]
    a.remove(4)
    x = a.pop(1)
    assert x == 4 and a == [2, 9]
    print("样片关键示例与出口题核对通过")

if __name__ == "__main__":
    verify()
