def tupleProc(input):
    result = [(0, 'не выбрано')]
    result += [(i + 1, item[0]) for i, item in enumerate(input)]
    return result