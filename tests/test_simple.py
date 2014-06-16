from jsonstream import tokenize_string


def test_simple():
    assert tokenize_string('') == []
