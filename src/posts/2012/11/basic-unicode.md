Date: 2012-11-10
Title: Character Encoding with Unicode
Tags: encoding, python
Slug: basic-unicode
Category: Blog

!! The Unicode Standard

It is always a pay off to understand how character encoding scheme works. Computer only understands number. So there is a need to have a convention to convert from character to number and vice versa. In essence, a string is represented as a array of bytes. A byte can represent 256 values. So it was fine at the begining when only English characters are used in digital world. Each byte simply represent one character. But problem arised when another languages come in with all the different characters. 256 values are not enough to accommodate all of them.    

You might think of using the same number to represent different characters under different schemes. But that will limit the interchangable of documents and limit a document to contain characters from only one language. 

Long story short, Unicode is a standard attempting to contain the alphabets for every human language. It does so by assigning an integer value (code point) to every alphabet. It is a document which maps every character (`LATIN SMALL LETTER A`, for example) to a number (`0061` in this case). 

!! Unicode Encoding

Remember computer stores string as an array of bytes? So how do we have a string of 8-bit values from code points? We use encoding. 

There are a number of different encoding schemes. UTF-32, UTF-16, UTF-8. UTF-8 is the most widely used and supported encoding. It better utilizes memory spaces and and solved compatibilities problems, compared to other encoding like UTF-32. 

*   For code point below 128, it encodes as the corresponding byte value. The 1st 128 code points represent the same character set as in ASCII code.  
*   For code point between 128 and 0x7ff, it encodes each code point by two byte values which are between 128 and 255
*   For code point greater than 0x7ff, it uses 3 to 4 bytes which are between 128 and 255. 

To summarize, there are, in general, two steps in storing a character in computer: 
    
    Character --> Integer Value (Code point) --> String of 8-bit values

The encoding of character to code point is handled by the Unicode standard. For the second step, any encoding scheme can be used besides UTF-8. Let's say if we use ASCII or ISO-8859-1, if string only contains code point below 128 or 255 respectively, we will have each byte as the same value of the code point. But it contains code point above these value, error will occur (program normally will throw exception).

!! Unicode in Python

In Python 2x, the default encoding is Extended ASCII. If you attempt to use a character with code point >= 256, exception will be thrown: 

    >>> chr(40000)
    Traceback (most recent call last):
       File "<stdin>", line 1, in <module>
       ValueError: chr() arg not in range(256)
    
To get the unicode character in the above case:

    >>> unichr(40000)
    u'\u9c40'

To create an unicode string, use this syntax:
    
    s = u"a\xac\u1234\u20ac\U00008000"

`u` denotes unicode string; `\x` for one byte character and `\u` for 2 byte character, `\U` for 4 byte character. 

Or create a Unicode string by decoding from a 8 bit string. For example: 

    >>> unicode('a\xc2\xac\xe1\x88\xb4\xe2\x82\xac\xe8\x80\x80', 'utf-8')
    u'a\xac\u1234\u20ac\u8000'
    
Or: 

    >>> s = 'a\xc2\xac\xe1\x88\xb4\xe2\x82\xac\xe8\x80\x80'
    >>> s.decode('utf-8')
    u'a\xac\u1234\u20ac\u8000'

The correct encoding scheme used to decode need to speicify. Otherwise, python will use the default `ascii` encoding, which will throw the error: 

    'ascii' codec can't decode byte 0xc2 in position 1: ordinal not in range(128)


In Python 3, the default encoding will be UTF-8. That means:
*   All `str` object will be `unicode` object. No more `u'...'`.  
*   Use `chr` instead of `unichr` for code point > 128
















