import os
import sys

from cffi import FFI

ffi = FFI()

# yajl_common.h
ffi.cdef("""
typedef void * (*yajl_malloc_func)(void *ctx, size_t sz);
typedef void (*yajl_free_func)(void *ctx, void * ptr);
typedef void * (*yajl_realloc_func)(void *ctx, void * ptr, size_t sz);
typedef struct
{
    yajl_malloc_func malloc;
    yajl_realloc_func realloc;
    yajl_free_func free;
    void * ctx;
} yajl_alloc_funcs;
""")

# yajl_alloc.h (internal)
ffi.cdef("""
void yajl_set_default_alloc_funcs(yajl_alloc_funcs * yaf);
""")

# yajl_buf.h (internal)
ffi.cdef("""
typedef struct yajl_buf_t * yajl_buf;
yajl_buf yajl_buf_alloc(yajl_alloc_funcs * alloc);
void yajl_buf_free(yajl_buf buf);
void yajl_buf_append(yajl_buf buf, const void * data, size_t len);
void yajl_buf_clear(yajl_buf buf);
const unsigned char * yajl_buf_data(yajl_buf buf);
size_t yajl_buf_len(yajl_buf buf);
void yajl_buf_truncate(yajl_buf buf, size_t len);
""")

# yajl_encode.h (internal)
ffi.cdef("""
void yajl_string_encode(const yajl_print_t printer,
                        void * ctx,
                        const unsigned char * str,
                        size_t length,
                        int escape_solidus);

void yajl_string_decode(yajl_buf buf, const unsigned char * str,
                        size_t length);

int yajl_string_validate_utf8(const unsigned char * s, size_t len);
""")

# yajl_lex.h (internal)
ffi.cdef("""
typedef enum {
    yajl_tok_bool,
    yajl_tok_colon,
    yajl_tok_comma,
    yajl_tok_eof,
    yajl_tok_error,
    yajl_tok_left_brace,
    yajl_tok_left_bracket,
    yajl_tok_null,
    yajl_tok_right_brace,
    yajl_tok_right_bracket,
    yajl_tok_integer,
    yajl_tok_double,
    yajl_tok_string,
    yajl_tok_string_with_escapes,
    yajl_tok_comment
} yajl_tok;

typedef struct yajl_lexer_t * yajl_lexer;

yajl_lexer yajl_lex_alloc(yajl_alloc_funcs * alloc,
                          unsigned int allowComments,
                          unsigned int validateUTF8);

void yajl_lex_free(yajl_lexer lexer);

yajl_tok yajl_lex_lex(yajl_lexer lexer, const unsigned char * jsonText,
                      size_t jsonTextLen, size_t * offset,
                      const unsigned char ** outBuf, size_t * outLen);

yajl_tok yajl_lex_peek(yajl_lexer lexer, const unsigned char * jsonText,
                       size_t jsonTextLen, size_t offset);


typedef enum {
    yajl_lex_e_ok = 0,
    yajl_lex_string_invalid_utf8,
    yajl_lex_string_invalid_escaped_char,
    yajl_lex_string_invalid_json_char,
    yajl_lex_string_invalid_hex_char,
    yajl_lex_invalid_char,
    yajl_lex_invalid_string,
    yajl_lex_missing_integer_after_decimal,
    yajl_lex_missing_integer_after_exponent,
    yajl_lex_missing_integer_after_minus,
    yajl_lex_unallowed_comment
} yajl_lex_error;

const char * yajl_lex_error_to_string(yajl_lex_error error);
yajl_lex_error yajl_lex_get_error(yajl_lexer lexer);
size_t yajl_lex_current_offset(yajl_lexer lexer);
size_t yajl_lex_current_line(yajl_lexer lexer);
size_t yajl_lex_current_char(yajl_lexer lexer);
""")


if sys.platform == 'darwin':
    soname = 'libyajl.dylib'
else:
    soname = 'libyajl.so'

libpath = os.path.join(os.path.dirname(__file__), soname)

lib = ffi.dlopen(libpath)

# yajl = ffi.verify("""
# #include "yajl/yajl_common.h"
# #include "yajl/yajl_tree.h"
# """,
# libraries=[libpath], ext_package='yajl')
