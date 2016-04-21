import ctypes
from cStringIO import StringIO as BytesIO

from yajs.lib import yajl


yajl_tok_bool, \
    yajl_tok_colon, \
    yajl_tok_comma, \
    yajl_tok_eof, \
    yajl_tok_error, \
    yajl_tok_left_bracket, \
    yajl_tok_left_brace, \
    yajl_tok_null, \
    yajl_tok_right_bracket, \
    yajl_tok_right_brace, \
    yajl_tok_integer, \
    yajl_tok_double, \
    yajl_tok_string, \
    yajl_tok_string_with_escapes, \
    yajl_tok_comment = range(15)

tokens_want_value = frozenset([
    yajl_tok_bool,
    yajl_tok_integer,
    yajl_tok_double,
    yajl_tok_string,
])


token_value_converters = {
    yajl_tok_bool: lambda x: x == 'true',
    yajl_tok_integer: int,
    yajl_tok_double: float,
    yajl_tok_string: lambda x: x.decode('utf-8'),
    yajl_tok_null: lambda x: None,
}


yajl_alloc_func_buffer = ctypes.c_void_p * 4

yajl_lex_alloc = yajl.yajl_lex_alloc
yajl_lex_alloc.argtypes = (ctypes.c_void_p, ctypes.c_uint, ctypes.c_uint)
yajl_lex_alloc.restype = ctypes.c_void_p

yajl_lex_free = yajl.yajl_lex_free
yajl_lex_free.argtypes = (ctypes.c_void_p,)

yajl_lex_lex = yajl.yajl_lex_lex
yajl_lex_lex.argtypes = (ctypes.c_void_p, ctypes.c_char_p,
                         ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t),
                         ctypes.POINTER(ctypes.c_char_p),
                         ctypes.POINTER(ctypes.c_size_t))

yajl_set_default_alloc_funcs = yajl.yajl_set_default_alloc_funcs
yajl_set_default_alloc_funcs.argtypes = (ctypes.c_void_p,)

yajl_buf_alloc = yajl.yajl_buf_alloc
yajl_buf_alloc.argtypes = (ctypes.c_void_p,)
yajl_buf_alloc.restype = ctypes.c_void_p

yajl_buf_free = yajl.yajl_buf_free
yajl_buf_free.argtypes = (ctypes.c_void_p,)

yajl_buf_data = yajl.yajl_buf_data
yajl_buf_data.restype = ctypes.c_char_p
yajl_buf_data.argtypes = (ctypes.c_void_p,)

yajl_buf_len = yajl.yajl_buf_len
yajl_buf_len.restype = ctypes.c_size_t
yajl_buf_len.argtypes = (ctypes.c_void_p,)

yajl_buf_clear = yajl.yajl_buf_clear
yajl_buf_clear.argtypes = (ctypes.c_void_p,)

yajl_string_decode = yajl.yajl_string_decode
yajl_string_decode.argtypes = (ctypes.c_void_p, ctypes.c_char_p,
                               ctypes.c_size_t)


def _ll_tokenize(chunk_iter, allow_comments):
    """Tokenizes data from an input stream."""
    alloc_funcs = yajl_alloc_func_buffer()
    yajl_set_default_alloc_funcs(ctypes.byref(alloc_funcs))

    lexer = yajl_lex_alloc(ctypes.byref(alloc_funcs), allow_comments, False)
    decode_buffer = yajl_buf_alloc(ctypes.byref(alloc_funcs))

    try:
        out_buffer = ctypes.c_char_p()
        out_buffer_ref = ctypes.byref(out_buffer)
        out_len = ctypes.c_size_t()
        out_len_ref = ctypes.byref(out_len)

        for chunk in chunk_iter:
            chunk_p = ctypes.c_char_p(chunk)
            chunk_len = len(chunk)
            offset = ctypes.c_size_t(0)
            offset_ref = ctypes.byref(offset)

            while 1:
                tok = yajl_lex_lex(lexer, chunk_p, chunk_len,
                                   offset_ref,
                                   out_buffer_ref,
                                   out_len_ref)
                if tok == yajl_tok_eof:
                    break
                elif tok == yajl_tok_error:
                    raise ValueError('Invalid JSON')
                elif tok == yajl_tok_comment:
                    continue
                elif tok == yajl_tok_string_with_escapes:
                    yajl_string_decode(decode_buffer,
                                       out_buffer, out_len.value)
                    value = ctypes.string_at(yajl_buf_data(decode_buffer),
                                             yajl_buf_len(decode_buffer))
                    yajl_buf_clear(decode_buffer)
                    tok = yajl_tok_string
                elif tok in tokens_want_value:
                    value = ctypes.string_at(out_buffer, out_len.value)
                else:
                    value = None
                yield tok, value
    finally:
        yajl_lex_free(lexer)
        yajl_buf_free(decode_buffer)


def tokenize(f, allow_comments=False, buffer_size=8 * 4096):
    """Tokenizes JSON from a given file stream.  It will consume up to
    `buffer_size` bytes at the time but it will not read past
    newlines.

    This always assumes UTF-8 encoding.
    """
    def _iter_chunks():
        while 1:
            line = f.readline(buffer_size)
            if not line:
                break
            yield line
        # We need to yield some extra whitespace to resolve the
        # case where a number would otherwise not be delimited.  This
        # solves a problem with the lexer being unsure if the number is
        # terminated or not.
        yield ' '

    def _build(token, value):
        if token == yajl_tok_left_brace:
            yield 'start_map', None
            first = True
            while 1:
                token, value = tokeniter.next()
                if token == yajl_tok_right_brace:
                    break
                if not first:
                    if token != yajl_tok_comma:
                        raise ValueError('Missing comma')
                    token, value = tokeniter.next()
                first = False
                for event in _build(token, value):
                    yield event
                token, _ = tokeniter.next()
                if token != yajl_tok_colon:
                    raise ValueError('Missing colon')
                for event in _build(*tokeniter.next()):
                    yield event
            yield 'end_map', None
        elif token == yajl_tok_left_bracket:
            yield 'start_array', None
            first = True
            while 1:
                token, value = tokeniter.next()
                if token == yajl_tok_right_bracket:
                    break
                if not first:
                    if token != yajl_tok_comma:
                        raise ValueError('Missing comma')
                    token, value = tokeniter.next()
                first = False
                for event in _build(token, value):
                    yield event
            yield 'end_array', None
        else:
            conv = token_value_converters.get(token)
            if conv is None:
                raise ValueError('Invalid JSON')
            yield 'value', conv(value)

    tokeniter = _ll_tokenize(_iter_chunks(), allow_comments)
    try:
        first = tokeniter.next()
    except StopIteration:
        return iter(())
    return _build(*first)


def tokenize_string(string, allow_comments=False):
    """Tokenizes a given unicode or literal string."""
    if isinstance(string, unicode):
        string = string.encode('utf-8')
    f = BytesIO(string)
    return tokenize(f, allow_comments)
