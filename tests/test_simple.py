from yajs import tokenize_string


def test_simple():
    assert list(tokenize_string('')) == []

    assert list(tokenize_string('{}')) == [
        ('start_map', None),
        ('end_map', None),
    ]

    assert list(tokenize_string('[]')) == [
        ('start_array', None),
        ('end_array', None),
    ]

    assert list(tokenize_string('1')) == [
        ('value', 1),
    ]

    tokens = list(tokenize_string('[1]'))
    assert len(tokens) == 3
    assert tokens[1] == ('value', 1)
