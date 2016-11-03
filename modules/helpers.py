import itertools

def get_hexdec_combos():
    COMBINATIONS = []
    hexdec_chars = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'a', 'b', 'c', 'd', 'e', 'f']
    for subset in itertools.combinations_with_replacement(hexdec_chars, 2):
        COMBINATIONS.append(''.join(list(subset)))
        COMBINATIONS.append(''.join(list(reversed(subset))))
    combinations_set = set(COMBINATIONS)
    COMBINATIONS = list(combinations_set)
    return COMBINATIONS
