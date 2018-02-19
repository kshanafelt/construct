# -*- coding: utf-8 -*-

from declarativeunittest import *
from construct import *
from construct.lib import *


def test_bytes():
    common(Bytes(4), b"1234", b"1234", 4)
    assert Bytes(4).parse(b"12345678") == b"1234"
    assert raises(Bytes(4).parse, b"") == StreamError
    assert raises(Bytes(4).build, b"toolong") == StreamError
    assert Bytes(4).build(1) == b"\x00\x00\x00\x01"
    assert Bytes(4).build(0x01020304) == b"\x01\x02\x03\x04"
    assert Bytes(4).sizeof() == 4

    assert Bytes(this.n).parse(b"12345678",n=4) == b"1234"
    assert Bytes(this.n).build(b"1234",n=4) == b"1234"
    assert Bytes(this.n).sizeof(n=4) == 4
    assert Bytes(this.n).build(1, n=4) == b"\x00\x00\x00\x01"
    assert raises(Bytes(this.n).build, b"", n=4) == StreamError
    assert raises(Bytes(this.n).build, b"toolong", n=4) == StreamError
    assert raises(Bytes(this.n).sizeof) == SizeofError

def test_greedybytes():
    common(GreedyBytes, b"1234", b"1234", SizeofError)

def test_bitwise():
    common(Bitwise(Bytes(8)), b"\xff", b"\x01\x01\x01\x01\x01\x01\x01\x01", 1)
    common(Bitwise(Array(8,Bit)), b"\xff", [1,1,1,1,1,1,1,1], 1)
    common(Bitwise(Array(2,Nibble)), b"\xff", [15,15], 1)
    common(Bitwise(Array(1,Octet)), b"\xff", [255], 1)

def test_bytewise():
    common(Bitwise(Bytewise(Bytes(1))), b"\xff", b"\xff", 1)
    common(BitStruct("p1"/Nibble, "num"/Bytewise(Int24ub), "p2"/Nibble), b"\xf0\x10\x20\x3f", Container(p1=15)(num=0x010203)(p2=15), 4)
    common(Bitwise(Sequence(Nibble, Bytewise(Int24ub), Nibble)), b"\xf0\x10\x20\x3f", [0x0f,0x010203,0x0f], 4)

def test_ints():
    common(Byte, b"\xff", 255, 1)
    common(Short, b"\x00\xff", 255, 2)
    common(Int, b"\x00\x00\x00\xff", 255, 4)
    common(Long, b"\x00\x00\x00\x00\x00\x00\x00\xff", 255, 8)
    assert Int8ub.parse(b"\x01") == 0x01
    assert Int8ub.build(0x01) == b"\x01"
    assert Int8ub.sizeof() == 1
    assert Int16ub.parse(b"\x01\x02") == 0x0102
    assert Int16ub.build(0x0102) == b"\x01\x02"
    assert Int16ub.sizeof() == 2
    assert Int32ub.parse(b"\x01\x02\x03\x04") == 0x01020304
    assert Int32ub.build(0x01020304) == b"\x01\x02\x03\x04"
    assert Int32ub.sizeof() == 4
    assert Int64ub.parse(b"\x01\x02\x03\x04\x05\x06\x07\x08") == 0x0102030405060708
    assert Int64ub.build(0x0102030405060708) == b"\x01\x02\x03\x04\x05\x06\x07\x08"
    assert Int64ub.sizeof() == 8
    assert Int8sb.parse(b"\x01") == 0x01
    assert Int8sb.build(0x01) == b"\x01"
    assert Int8sb.sizeof() == 1
    assert Int16sb.parse(b"\x01\x02") == 0x0102
    assert Int16sb.build(0x0102) == b"\x01\x02"
    assert Int16sb.sizeof() == 2
    assert Int32sb.parse(b"\x01\x02\x03\x04") == 0x01020304
    assert Int32sb.build(0x01020304) == b"\x01\x02\x03\x04"
    assert Int32sb.sizeof() == 4
    assert Int64sb.parse(b"\x01\x02\x03\x04\x05\x06\x07\x08") == 0x0102030405060708
    assert Int64sb.build(0x0102030405060708) == b"\x01\x02\x03\x04\x05\x06\x07\x08"
    assert Int64sb.sizeof() == 8
    assert Int8ul.parse(b"\x01") == 0x01
    assert Int8ul.build(0x01) == b"\x01"
    assert Int8ul.sizeof() == 1
    assert Int16ul.parse(b"\x01\x02") == 0x0201
    assert Int16ul.build(0x0201) == b"\x01\x02"
    assert Int16ul.sizeof() == 2
    assert Int32ul.parse(b"\x01\x02\x03\x04") == 0x04030201
    assert Int32ul.build(0x04030201) == b"\x01\x02\x03\x04"
    assert Int32ul.sizeof() == 4
    assert Int64ul.parse(b"\x01\x02\x03\x04\x05\x06\x07\x08") == 0x0807060504030201
    assert Int64ul.build(0x0807060504030201) == b"\x01\x02\x03\x04\x05\x06\x07\x08"
    assert Int64ul.sizeof() == 8
    assert Int8sl.parse(b"\x01") == 0x01
    assert Int8sl.build(0x01) == b"\x01"
    assert Int8sl.sizeof() == 1
    assert Int16sl.parse(b"\x01\x02") == 0x0201
    assert Int16sl.build(0x0201) == b"\x01\x02"
    assert Int16sl.sizeof() == 2
    assert Int32sl.parse(b"\x01\x02\x03\x04") == 0x04030201
    assert Int32sl.build(0x04030201) == b"\x01\x02\x03\x04"
    assert Int32sl.sizeof() == 4
    assert Int64sl.parse(b"\x01\x02\x03\x04\x05\x06\x07\x08") == 0x0807060504030201
    assert Int64sl.build(0x0807060504030201) == b"\x01\x02\x03\x04\x05\x06\x07\x08"
    assert Int64sl.sizeof() == 8

def test_ints24():
    common(Int24ub, b"\x01\x02\x03", 0x010203, 3)
    common(Int24ul, b"\x01\x02\x03", 0x030201, 3)
    common(Int24sb, b"\xff\xff\xff", -1, 3)
    common(Int24sl, b"\xff\xff\xff", -1, 3)

def test_floats():
    assert Single.build(1.2) == b"?\x99\x99\x9a"
    assert Double.build(1.2) == b"?\xf3333333"

def test_formatfield():
    common(FormatField("<","L"), b"\x12\x34\x56\x78", 0x78563412, 4)
    assert raises(FormatField("<","L").parse, b"") == StreamError
    assert raises(FormatField("<","L").parse, b"\x12\x34\x56") == StreamError
    assert raises(FormatField("<","L").build, "string not int") == FormatFieldError
    assert raises(FormatField("<","L").build, 2**100) == FormatFieldError
    assert raises(FormatField("<","L").build, 9e9999) == FormatFieldError

def test_formatfield_ints_randomized():
    for endianess,dtype in itertools.product("<>=","bhlqBHLQ"):
        d = FormatField(endianess, dtype)
        for i in range(100):
            obj = random.randrange(0, 256**d.sizeof()//2)
            assert d.parse(d.build(obj)) == obj
            data = os.urandom(d.sizeof())
            assert d.build(d.parse(data)) == data

def test_formatfield_floats_randomized():
    # there is a roundoff eror because Python float is a C double
    # http://stackoverflow.com/questions/39619636/struct-unpackstruct-packfloat-has-roundoff-error
    # and analog although that was misplaced
    # http://stackoverflow.com/questions/39676482/struct-packstruct-unpackfloat-is-inconsistent-on-py3
    for endianess,dtype in itertools.product("<>=","fd"):
        d = FormatField(endianess, dtype)
        for i in range(100):
            x = random.random()*12345
            if dtype == "d":
                assert d.parse(d.build(x)) == x
            else:
                assert abs(d.parse(d.build(x)) - x) < 1e-3
        for i in range(100):
            b = os.urandom(d.sizeof())
            if not math.isnan(d.parse(b)):
                assert d.build(d.parse(b)) == b

def test_bytesinteger():
    common(BytesInteger(4), b"\x00\x00\x00\xff", 255, 4)
    common(BytesInteger(4, signed=True), b"\xff\xff\xff\xff", -1, 4)
    assert raises(BytesInteger(this.missing).sizeof) == SizeofError
    assert raises(BytesInteger(4, signed=False).build, -1) == IntegerError
    common(BytesInteger(0), b"", 0, 0)

def test_bitsinteger():
    assert BitsInteger(8).parse(b"\x01\x01\x01\x01\x01\x01\x01\x01") == 255
    assert BitsInteger(8).build(255) == b"\x01\x01\x01\x01\x01\x01\x01\x01"
    assert BitsInteger(8).sizeof() == 8
    assert BitsInteger(8, signed=True).parse(b"\x01\x01\x01\x01\x01\x01\x01\x01") == -1
    assert BitsInteger(8, signed=True).build(-1) == b"\x01\x01\x01\x01\x01\x01\x01\x01"
    assert raises(BitsInteger(this.missing).sizeof) == SizeofError
    assert raises(BitsInteger(8, signed=False).build, -1) == IntegerError
    common(BitsInteger(0), b"", 0, 0)

def test_varint():
    common(VarInt, b"\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x10", 2**123, SizeofError)
    for n in [0,1,5,100,255,256,65535,65536,2**32,2**100]:
        assert VarInt.parse(VarInt.build(n)) == n
        assert len(VarInt.build(n)) >= len("%x" % n)//2
    for n in range(0, 127):
        common(VarInt, int2byte(n), n, SizeofError)

    assert raises(VarInt.parse, b"") == StreamError
    assert raises(VarInt.build, -1) == IntegerError

def test_string():
    common(String(10, encoding="utf8"), b"hello\x00\x00\x00\x00\x00", u"hello", 10)

    for e,us in [("utf8",1),("utf16",2),("utf_16_le",2),("utf32",4),("utf_32_le",4)]:
        s = u"Афон"
        data = (s.encode(e)+b"\x00"*100)[:100]
        common(String(100, encoding=e), data, s, 100)
        s = u""
        data = b"\x00"*100
        common(String(100, encoding=e), data, s, 100)

    for e in ["ascii","utf8","utf16","utf-16-le","utf32","utf-32-le"]:
        String(10, encoding=e).sizeof() == 10
        String(this.n, encoding=e).sizeof(n=10) == 10

def test_pascalstring():
    for e,us in [("utf8",1),("utf16",2),("utf_16_le",2),("utf32",4),("utf_32_le",4)]:
        for sc in [Byte, Int16ub, Int16ul, VarInt]:
            s = u"Афон"
            data = sc.build(len(s.encode(e))) + s.encode(e)
            common(PascalString(sc, encoding=e), data, s)
            common(PascalString(sc, encoding=e), sc.build(0), u"")

    for e in ["utf8","utf16","utf-16-le","utf32","utf-32-le","ascii"]:
        raises(PascalString(Byte, encoding=e).sizeof) == SizeofError
        raises(PascalString(VarInt, encoding=e).sizeof) == SizeofError

def test_cstring():
    for e,us in [("utf8",1),("utf16",2),("utf_16_le",2),("utf32",4),("utf_32_le",4)]:
        s = u"Афон"
        common(CString(encoding=e), s.encode(e)+b"\x00"*us, s)
        common(CString(encoding=e), b"\x00"*us, u"")

    CString(encoding="utf8").build(s) == b'\xd0\x90\xd1\x84\xd0\xbe\xd0\xbd'+b"\x00"
    CString(encoding="utf16").build(s) == b'\xff\xfe\x10\x04D\x04>\x04=\x04'+b"\x00\x00"
    CString(encoding="utf32").build(s) == b'\xff\xfe\x00\x00\x10\x04\x00\x00D\x04\x00\x00>\x04\x00\x00=\x04\x00\x00'+b"\x00\x00\x00\x00"

    for e in ["utf8","utf16","utf-16-le","utf32","utf-32-le","ascii"]:
        raises(CString(encoding=e).sizeof) == SizeofError

def test_greedystring():
    for e,us in [("utf8",1),("utf16",2),("utf_16_le",2),("utf32",4),("utf_32_le",4)]:
        s = u"Афон"
        common(GreedyString(encoding=e), s.encode(e), s)
        common(GreedyString(encoding=e), b"", u"")

    for e in ["utf8","utf16","utf-16-le","utf32","utf-32-le","ascii"]:
        raises(GreedyString(encoding=e).sizeof) == SizeofError

def test_string_encodings():
    # checks that "-" is replaced with "_"
    common(GreedyString("utf-8"), b"", u"")
    common(GreedyString("utf-8"), b'\xd0\x90\xd1\x84\xd0\xbe\xd0\xbd', u"Афон")

def test_flag():
    common(Flag, b"\x00", False, 1)
    common(Flag, b"\x01", True, 1)

def test_enum():
    d = Enum(Byte, one=1, two=2, four=4, eight=8)
    common(d, b"\x01", "one", 1)
    common(d, b"\xff", 255, 1)
    assert d.parse(b"\x01") == d.one
    assert d.parse(b"\x01") == "one"
    assert int(d.parse(b"\x01")) == 1
    assert d.parse(b"\xff") == 255
    assert int(d.parse(b"\xff")) == 255
    assert d.build(8) == b'\x08'
    assert d.build(255) == b"\xff"
    assert d.build(d.eight) == b'\x08'
    assert d.one == "one"
    assert int(d.one) == 1
    assert raises(d.build, "unknown") == MappingError
    assert raises(lambda: d.missing) == AttributeError

@xfail(not supportsintenum, raises=AttributeError, reason="IntEnum introduced in 3.4, IntFlag introduced in 3.6")
def test_enum_enum34():
    import enum
    class E(enum.IntEnum):
        a = 1
    class F(enum.IntEnum):
        b = 2
    common(Enum(Byte, E, F), b"\x01", "a", 1)
    common(Enum(Byte, E, F), b"\x02", "b", 1)

@xfail(not supportsintflag, raises=AttributeError, reason="IntEnum introduced in 3.4, IntFlag introduced in 3.6")
def test_enum_enum36():
    import enum
    class E(enum.IntEnum):
        a = 1
    class F(enum.IntFlag):
        b = 2
    common(Enum(Byte, E, F), b"\x01", "a", 1)
    common(Enum(Byte, E, F), b"\x02", "b", 1)

def test_enum_issue_298():
    st = Struct(
        "ctrl" / Enum(Byte,
            NAK = 0x15,
            STX = 0x02,
        ),
        "optional" / If(this.ctrl == "NAK", Byte),
    )
    common(st, b"\x15\xff", Container(ctrl='NAK')(optional=255))
    common(st, b"\x02", Container(ctrl='STX')(optional=None))

    # FlagsEnum is not affected by same bug
    st = Struct(
        "flags" / FlagsEnum(Byte, a=1),
        Check(lambda ctx: ctx.flags == Container(a=1)),
    )
    common(st, b"\x01", dict(flags=Container(a=True)), 1)

    # Flag is not affected by same bug
    st = Struct(
        "flag" / Flag,
        Check(lambda ctx: ctx.flag == True),
    )
    common(st, b"\x01", dict(flag=True), 1)

def test_flagsenum():
    d = FlagsEnum(Byte, one=1, two=2, four=4, eight=8)
    common(d, b"\x03", Container(one=True)(two=True)(four=False)(eight=False), 1)
    assert d.build({}) == b'\x00'
    assert d.build(dict(one=True,two=True)) == b'\x03'
    assert d.build(8) == b'\x08'
    assert d.build(1|2) == b'\x03'
    assert d.build(255) == b"\xff"
    assert d.build(d.eight) == b'\x08'
    assert d.build(d.one|d.two) == b'\x03'
    assert raises(d.build, dict(unknown=True)) == MappingError
    assert raises(d.build, "unknown") == MappingError
    assert d.one == "one"
    assert d.one|d.two == "one|two"
    assert raises(lambda: d.missing) == AttributeError

@xfail(not supportsintenum, raises=AttributeError, reason="IntEnum introduced in 3.4, IntFlag introduced in 3.6")
def test_flagsenum_enum34():
    import enum
    class E(enum.IntEnum):
        a = 1
    class F(enum.IntEnum):
        b = 2
    common(FlagsEnum(Byte, E, F), b"\x01", Container(a=True,b=False), 1)
    common(FlagsEnum(Byte, E, F), b"\x02", Container(a=False,b=True), 1)
    common(FlagsEnum(Byte, E, F), b"\x03", Container(a=True,b=True), 1)

@xfail(not supportsintflag, raises=AttributeError, reason="IntEnum introduced in 3.4, IntFlag introduced in 3.6")
def test_flagsenum_enum36():
    import enum
    class E(enum.IntEnum):
        a = 1
    class F(enum.IntFlag):
        b = 2
    common(FlagsEnum(Byte, E, F), b"\x01", Container(a=True,b=False), 1)
    common(FlagsEnum(Byte, E, F), b"\x02", Container(a=False,b=True), 1)
    common(FlagsEnum(Byte, E, F), b"\x03", Container(a=True,b=True), 1)

def test_mapping():
    d = Mapping(Byte, {"zero":0})
    common(d, b"\x00", "zero", 1)

def test_struct():
    common(Struct(), b"", Container(), 0)
    common(Struct("a"/Int16ul, "b"/Byte), b"\x01\x00\x02", Container(a=1,b=2), 3)
    common(Struct("a"/Struct("b"/Byte)), b"\x01", Container(a=Container(b=1)), 1)
    assert raises(Struct("missingkey"/Byte).build, dict()) == KeyError
    assert Struct("a"/Byte, "a"/VarInt, "a"/Pass).build(dict(a=1)) == b"\x01\x01"
    common(Struct(), b"", Container(), 0)
    common(Struct(Padding(2)), b"\x00\x00", Container(), 2)
    assert raises(Struct(Bytes(this.missing)).sizeof) == SizeofError

def test_struct_nested_embedded():
    common(Struct("a"/Byte, "b"/Int16ub, "inner"/Struct("c"/Byte, "d"/Byte)), b"\x01\x00\x02\x03\x04", Container(a=1,b=2,inner=Container(c=3,d=4)), 5)
    common(Struct("a"/Byte, "b"/Int16ub, Embedded("inner"/Struct("c"/Byte, "d"/Byte))), b"\x01\x00\x02\x03\x04", Container(a=1,b=2,c=3,d=4), 5)

@xfail(not supportskwordered, reason="ordered kw was introduced in 3.6")
def test_struct_kwctor():
    common(Struct(a=Byte, b=Byte, c=Byte, d=Byte), b"\x01\x02\x03\x04", Container(a=1,b=2,c=3,d=4), 4)

def test_struct_proper_context():
    # adjusted to support new embedding semantics
    d1 = Struct(
        "x"/Byte,
        "inner"/Struct(
            "y"/Byte,
            "a"/Computed(this._.x+1),
            "b"/Computed(this.y+2),
        ),
        "c"/Computed(this.x+3),
        "d"/Computed(this.inner.y+4),
    )
    d2 = Struct(
        "x"/Byte,
        "inner"/Embedded(Struct(
            "y"/Byte,
            "a"/Computed(this.x+1),  # important
            "b"/Computed(this.y+2),  # important
        )),
        "c"/Computed(this.x+3),
        "d"/Computed(this.y+4),
    )
    assert d1.parse(b"\x01\x0f") == Container(x=1)(inner=Container(y=15)(a=2)(b=17))(c=4)(d=19)
    # a-field computed on nested context, merged only after entire inner-struct returns
    assert d2.parse(b"\x01\x0f") == Container(x=1)(y=15)(a=2)(b=17)(c=4)(d=19)

def test_struct_sizeof_context_nesting():
    st = Struct(
        "a" / Computed(1),
        "inner" / Struct(
            "b" / Computed(2),
            Check(this._.a == 1),
            Check(this.b == 2),
        ),
        Check(this.a == 1),
        Check(this.inner.b == 2),
    )
    assert st.sizeof() == 0

def test_struct_issue_566():
    inner = Struct(
        Embedded(Struct(
            "b" / Byte,
        )),
        "c" / If(this._.a > 0, Byte),
    )
    outer = Struct(
        "a" / Byte,
        "inner" / inner,
    )
    outer.parse(b'\x01\x02\x03') == Container(a=1)(inner=Container(b=2)(c=3))
    outer.build(Container(a=1)(inner=Container(b=2)(c=3))) == b'\x01\x02\x80\x03\x04'

def test_sequence():
    common(Sequence(), b"", [], 0)
    common(Sequence(Int8ub, Int16ub), b"\x01\x00\x02", [1,2], 3)
    common(Int8ub >> Int16ub, b"\x01\x00\x02", [1,2], 3)

def test_sequence_nested_embedded():
    common(Sequence(Int8ub, Int16ub, Sequence(Int8ub, Int8ub)), b"\x01\x00\x02\x03\x04", [1,2,[3,4]], 5)
    common(Sequence(Int8ub, Int16ub, Embedded(Sequence(Int8ub, Int8ub))), b"\x01\x00\x02\x03\x04", [1,2,3,4], 5)

def test_array():
    common(Byte[0], b"", [], 0)

    assert Byte[4].parse(b"1234") == [49,50,51,52]
    assert Byte[4].build([49,50,51,52]) == b"1234"

    assert Array(3,Byte).parse(b"\x01\x02\x03") == [1,2,3]
    assert Array(3,Byte).build([1,2,3]) == b"\x01\x02\x03"
    assert Array(3,Byte).parse(b"\x01\x02\x03additionalgarbage") == [1,2,3]
    assert raises(Array(3,Byte).parse, b"") == StreamError
    assert raises(Array(3,Byte).build, [1,2]) == RangeError
    assert raises(Array(3,Byte).build, [1,2,3,4,5,6,7,8]) == RangeError
    assert Array(3,Byte).sizeof() == 3

    assert Array(3, Byte).parse(b"\x01\x02\x03", n=3) == [1,2,3]
    assert Array(3, Byte).parse(b"\x01\x02\x03additionalgarbage", n=3) == [1,2,3]
    assert raises(Array(3, Byte).parse, b"", n=3) == StreamError
    assert Array(3, Byte).build([1,2,3], n=3) == b"\x01\x02\x03"
    assert raises(Array(3, Byte).build, [1,2], n=3) == RangeError
    assert Array(this.n, Byte).parse(b"\x01\x02\x03", n=3) == [1,2,3]
    assert Array(this.n, Byte).build([1,2,3], n=3) == b"\x01\x02\x03"
    assert raises(Array(this.n, Byte).sizeof) == SizeofError
    assert Array(this.n, Byte).sizeof(n=4) == 4

def test_array_nontellable():
    assert Array(5, Byte).parse_stream(devzero) == [0,0,0,0,0]

def test_greedyrange():
    common(GreedyRange(Byte), b"", [], SizeofError)
    common(GreedyRange(Byte), b"\x01\x02", [1,2], SizeofError)
    common(Byte[:], b"", [], SizeofError)
    common(Byte[:], b"\x01\x02", [1,2], SizeofError)

def test_repeatuntil():
    assert RepeatUntil(obj_ == 9, Byte).parse(b"\x02\x03\x09garbage") == [2,3,9]
    assert RepeatUntil(obj_ == 9, Byte).build([2,3,9,1,1,1]) == b"\x02\x03\x09"
    assert raises(RepeatUntil(obj_ == 9, Byte).parse, b"\x02\x03\x08") == StreamError
    assert raises(RepeatUntil(obj_ == 9, Byte).build, [2,3,8]) == RepeatError
    assert raises(RepeatUntil(obj_ == 9, Byte).sizeof) == SizeofError
    assert RepeatUntil(lambda x,lst,ctx: lst[-2:]==[0,0], Byte).parse(b"\x01\x00\x00\xff") == [1,0,0]
    assert RepeatUntil(lambda x,lst,ctx: lst[-2:]==[0,0], Byte).build([1,0,0,4]) == b"\x01\x00\x00"
    assert RepeatUntil(True, Byte).parse(b"\x00") == [0]
    assert RepeatUntil(True, Byte).build([0]) == b"\x00"

def test_const():
    common(Const(b"MZ"), b"MZ", b"MZ", 2)
    common(Const(b"****", Bytes(4)), b"****", b"****", 4)
    common(Const(255, Int32ul), b"\xff\x00\x00\x00", 255, 4)
    assert raises(Const(b"MZ").parse, b"ELF") == ConstError
    assert raises(Const(b"MZ").build, b"???") == ConstError
    assert raises(Const(255, Int32ul).parse, b"\x00\x00\x00\x00") == ConstError
    common(Struct(sig=Const(b"MZ")), b"MZ", Container(sig=b"MZ"), 2)
    assert Struct(sig=Const(b"MZ")).build({}) == b"MZ"

def test_const_nonbytes():
    # non-prefixed string literals are unicode on Python 3
    assert raises(lambda: Const(u"no prefix string")) == StringError

def test_computed():
    assert Computed("moo").parse(b"") == "moo"
    assert Computed("moo").build(None) == b""
    assert Computed("moo").sizeof() == 0
    assert Struct("c" / Computed("moo")).parse(b"") == Container(c="moo")
    assert Struct("c" / Computed("moo")).build({}) == b""
    assert Struct("c" / Computed("moo")).build(dict()) == b""
    assert Struct("c" / Computed("moo")).build(Container()) == b""
    assert raises(Computed(lambda ctx: ctx.missing).parse, b"") == AttributeError
    assert raises(Computed(lambda ctx: ctx["missing"]).parse, b"") == KeyError

    assert Computed(255).parse(b"") == 255
    assert Computed(255).build(None) == b""
    assert Struct(c=Computed(255)).parse(b"") == dict(c=255)
    assert Struct(c=Computed(255)).build({}) == b""

def test_index():
    d = Array(3, Bytes(this._index+1))
    common(d, b"abbccc", [b"a", b"bb", b"ccc"])
    d = GreedyRange(Bytes(this._index+1))
    common(d, b"abbccc", [b"a", b"bb", b"ccc"])
    d = RepeatUntil(lambda o,l,ctx: ctx._index == 2, Bytes(this._index+1))
    common(d, b"abbccc", [b"a", b"bb", b"ccc"])

    d = Array(3, Struct("i" / Index))
    common(d, b"", [Container(i=0),Container(i=1),Container(i=2)], 0)
    d = GreedyRange(Struct("i" / Index, "d" / Bytes(this.i+1)))
    common(d, b"abbccc", [Container(i=0,d=b"a"),Container(i=1,d=b"bb"),Container(i=2,d=b"ccc")])
    d = RepeatUntil(lambda o,l,ctx: ctx._index == 2, Index)
    common(d, b"", [0,1,2])

def test_rebuild():
    d = Struct("count"/Rebuild(Byte, len_(this.items)), "items"/Byte[this.count])
    assert d.parse(b"\x02ab") == Container(count=2)(items=[97,98])
    assert d.build(dict(count=None,items=[255])) == b"\x01\xff"
    assert d.build(dict(items=[255])) == b"\x01\xff"

def test_default():
    common(Struct("a"/Default(Byte,0), "b"/Default(Byte,0)), b"\x01\x02", Container(a=1)(b=2), 2)
    assert Struct("a"/Default(Byte,0), "b"/Default(Byte,0)).build(dict(a=1)) == b"\x01\x00"

def test_check():
    common(Check(True), b"", None, 0)
    common(Check(this.x == 255), b"", None, 0, x=255)
    common(Check(len_(this.a) == 3), b"", None, 0, a=[1,2,3])
    assert raises(Check(False).parse, b"") == CheckError
    assert raises(Check(this.x == 255).parse, b"", x=0) == CheckError
    assert raises(Check(len_(this.a) == 3).parse, b"", a=[]) == CheckError

def test_error():
    assert raises(Error.parse, b"") == ExplicitError
    assert raises(Error.build, None) == ExplicitError
    assert ("x"/Int8sb >> IfThenElse(this.x > 0, Int8sb, Error)).parse(b"\x01\x05") == [1,5]
    assert raises(("x"/Int8sb >> IfThenElse(this.x > 0, Int8sb, Error)).parse, b"\xff\x05") == ExplicitError

def test_focusedseq():
    assert FocusedSeq(1, Const(b"MZ"), "num"/Byte, Terminated).parse(b"MZ\xff") == 255
    assert FocusedSeq(1, Const(b"MZ"), "num"/Byte, Terminated).build(255) == b"MZ\xff"
    assert FocusedSeq(1, Const(b"MZ"), "num"/Byte, Terminated).sizeof() == 3
    assert FocusedSeq("num", Const(b"MZ"), "num"/Byte, Terminated).parse(b"MZ\xff") == 255
    assert FocusedSeq("num", Const(b"MZ"), "num"/Byte, Terminated).build(255) == b"MZ\xff"
    assert FocusedSeq("num", Const(b"MZ"), "num"/Byte, Terminated).sizeof() == 3
    assert FocusedSeq(this._.s, Const(b"MZ"), "num"/Byte, Terminated).parse(b"MZ\xff", s=1) == 255
    assert FocusedSeq(this._.s, Const(b"MZ"), "num"/Byte, Terminated).sizeof(s=1) == 3
    assert FocusedSeq(this._.s, Const(b"MZ"), "num"/Byte, Terminated).parse(b"MZ\xff", s="num") == 255
    assert FocusedSeq(this._.s, Const(b"MZ"), "num"/Byte, Terminated).sizeof(s="num") == 3

    assert raises(FocusedSeq(123, Pass).parse, b"") == IndexError
    assert raises(FocusedSeq(123, Pass).build, {}) == IndexError
    # assert raises(FocusedSeq(123, Pass).sizeof) == IndexError
    assert raises(FocusedSeq("missing", Pass).parse, b"") == KeyError
    assert raises(FocusedSeq("missing", Pass).build, {}) == KeyError
    # assert raises(FocusedSeq("missing", Pass).sizeof) == KeyError
    assert raises(FocusedSeq(this.missing, Pass).parse, b"") == KeyError
    assert raises(FocusedSeq(this.missing, Pass).build, {}) == KeyError
    # assert raises(FocusedSeq(this.missing, Pass).sizeof) == SizeofError

def test_pickled():
    import pickle
    obj = [(), 1, 2.3, {}, [], bytes(1), ""]
    data = pickle.dumps(obj)
    common(Pickled, data, obj)

@xfail(not supportsnumpy, reason="numpy is not installed?")
def test_numpy():
    import numpy
    obj = numpy.array([1,2,3], dtype=numpy.int64)
    assert numpy.array_equal(Numpy.parse(Numpy.build(obj)), obj)

def test_namedtuple():
    coord = collections.namedtuple("coord", "x y z")

    Coord = NamedTuple("coord", "x y z", Byte[3])
    assert Coord.parse(b"123") == coord(49,50,51)
    assert Coord.build(coord(49,50,51)) == b"123"
    assert Coord.sizeof() == 3

    Coord = NamedTuple("coord", "x y z", GreedyRange(Byte))
    assert Coord.parse(b"123") == coord(49,50,51)
    assert Coord.build(coord(49,50,51)) == b"123"
    assert raises(Coord.sizeof) == SizeofError

    Coord = NamedTuple("coord", "x y z", Byte >> Byte >> Byte)
    assert Coord.parse(b"123") == coord(49,50,51)
    assert Coord.build(coord(49,50,51)) == b"123"
    assert Coord.sizeof() == 3

    Coord = NamedTuple("coord", "x y z", Struct("x"/Byte, "y"/Byte, "z"/Byte))
    assert Coord.parse(b"123") == coord(49,50,51)
    assert Coord.build(coord(49,50,51)) == b"123"
    assert Coord.sizeof() == 3

    assert raises(lambda: NamedTuple("coord", "x y z", BitStruct("x"/Byte, "y"/Byte, "z"/Byte))) == NamedTupleError

def test_timestamp():
    import arrow
    d = Timestamp(Int64ub, "unix", "unix")
    common(d, b'\x00\x00\x00\x00ZIz\x00', arrow.Arrow(2018,1,1), 8)
    d = Timestamp(Int64ub, "macosx", "macosx")
    common(d, b'\x00\x00\x00\x00\xd6o*\x80', arrow.Arrow(2018,1,1), 8)
    d = Timestamp(Int64ub, "windows", "windows")
    common(d, b'\x01\xd4\xa2.\x1a\xa8\x00\x00', arrow.Arrow(2018,1,1), 8)
    d = Timestamp(Int32ub, "msdos", "msdos")
    common(d, b'H9\x8c"', arrow.Arrow(2016,1,25,17,33,4), 4)

def test_hex():
    d = Hex(Int32ub)
    common(d, b"\x00\x00\x01\x02", 0x0102, 4)
    obj = d.parse(b"\x00\x00\x01\x02")
    assert str(obj) == "0x00000102"
    assert str(obj) == "0x00000102"

    d = Hex(GreedyBytes)
    common(d, b"\x00\x00\x01\x02", b"\x00\x00\x01\x02")
    common(d, b"", b"")
    obj = d.parse(b"\x00\x00\x01\x02")
    assert str(obj) == "unhexlify('00000102')"
    assert str(obj) == "unhexlify('00000102')"

    d = Hex(RawCopy(Int32ub))
    common(d, b"\x00\x00\x01\x02", dict(data=b"\x00\x00\x01\x02", value=0x0102, offset1=0, offset2=4, length=4), 4)
    obj = d.parse(b"\x00\x00\x01\x02")
    assert str(obj) == "unhexlify('00000102')"
    assert str(obj) == "unhexlify('00000102')"

def test_hexdump():
    d = HexDump(GreedyBytes)
    common(d, b"abcdef", b"abcdef")
    common(d, b"", b"")
    obj = d.parse(b"\x00\x00\x01\x02")
    repr = \
'''hexundump("""
0000   00 00 01 02                                       ....
""")
'''
    pass
    assert str(obj) == repr
    assert str(obj) == repr

    d = HexDump(RawCopy(Int32ub))
    common(d, b"\x00\x00\x01\x02", dict(data=b"\x00\x00\x01\x02", value=0x0102, offset1=0, offset2=4, length=4), 4)
    obj = d.parse(b"\x00\x00\x01\x02")
    repr = \
'''hexundump("""
0000   00 00 01 02                                       ....
""")
'''
    assert str(obj) == repr
    assert str(obj) == repr

def test_regression_188():
    # Hex HexDump were not inheriting subcon flags
    d = Struct(Hex(Const(b"MZ")))
    assert d.parse(b"MZ") == Container()
    assert d.build(dict()) == b"MZ"
    d = Struct(HexDump(Const(b"MZ")))
    assert d.parse(b"MZ") == Container()
    assert d.build(dict()) == b"MZ"

def test_union():
    assert Union(None, "a"/Bytes(2), "b"/Int16ub).parse(b"\x01\x02") == Container(a=b"\x01\x02")(b=0x0102)
    assert raises(Union(123, Pass).parse, b"") == KeyError
    assert raises(Union("missing", Pass).parse, b"") == KeyError

    assert Union(None, "a"/Bytes(2), "b"/Int16ub).build(dict(a=b"zz"))  == b"zz"
    assert Union(None, "a"/Bytes(2), "b"/Int16ub).build(dict(b=0x0102)) == b"\x01\x02"
    assert Union(None, "a"/Bytes(2), "b"/Int16ub, Pass).build(dict()) == b""
    assert raises(Union(None, "a"/Bytes(2), "b"/Int16ub).build, dict()) == UnionError
    # build skips parsefrom, invalid or not
    # assert raises(Union(123, Pass).build, None) == None
    # assert raises(Union("missing", Pass).build, None) == None

    assert raises(Union(None, Byte).sizeof) == SizeofError
    assert raises(Union(None, VarInt).sizeof) == SizeofError
    assert raises(Union(0, Byte, VarInt).sizeof) == SizeofError
    assert raises(Union(1, Byte, VarInt).sizeof) == SizeofError
    assert raises(Union(123, Pass).sizeof) == SizeofError
    assert raises(Union("missing", Pass).sizeof) == SizeofError
    assert raises(Union(this.missing, Pass).sizeof) == SizeofError

    # regression check, so first subcon is not parsefrom by accident
    assert raises(Union, Byte, VarInt) == UnionError

def test_union_embedded():
    d = Union(None, "a"/Int16ub, Embedded(Struct("b"/Int8ub, "c"/Int8ub))) >> Byte
    assert d.parse(b"\x01\x02\x03") == [Container(a=0x0102, b=0x01, c=0x01), 0x01]

    d = Union(None, "a"/Int16ub, Embedded(Struct("b"/Int8ub, "c"/Int8ub)))
    assert d.parse(b"\x01\x02") == Container(a=0x0102, b=0x01, c=0x01)
    assert d.build(dict(a=0x0102)) == b"\x01\x02"
    assert d.build(dict(b=0x01)) == b"\x01"
    assert d.build(dict(c=0x01)) == b"\x01"
    assert raises(d.build, dict()) == UnionError

@xfail(not supportskwordered, reason="ordered kw was introduced in 3.6")
def test_union_kwctor():
    st = Union(None, a=Int8ub, b=Int16ub, c=Int32ub)
    assert st.parse(b"\x01\x02\x03\x04") == Container(a=0x01,b=0x0102,c=0x01020304)
    assert st.build(Container(c=0x01020304)) == b"\x01\x02\x03\x04"

def test_union_issue_348():
    u = Union(None,
        Int8=Prefixed(Int16ub, Int8ub[:]),
        Int16=Prefixed(Int16ub, Int16ub[:]),
        Int32=Prefixed(Int16ub, Int32ub[:]),
    )
    assert u.parse(b'\x00\x04\x11\x22\x33\x44') == {'Int16': [4386, 13124], 'Int32': [287454020], 'Int8': [17, 34, 51, 68]}
    assert u.build(dict(Int16=[4386, 13124])) == b'\x00\x04\x11\x22\x33\x44'
    assert u.build(dict(Int32=[287454020])) == b'\x00\x04\x11\x22\x33\x44'

def test_select():
    assert raises(Select(Int32ub, Int16ub).parse, b"\x07") == SelectError
    assert Select(Int32ub, Int16ub, Int8ub).parse(b"\x07") == 7
    assert Select(Int32ub, Int16ub, Int8ub).build(7) == b"\x00\x00\x00\x07"
    assert Select("a"/Int32ub, "b"/Int16ub, "c"/Int8ub, includename=True).parse(b"\x07") == ("c", 7)
    assert Select("a"/Int32ub, "b"/Int16ub, "c"/Int8ub, includename=True).build((("c", 7))) == b"\x07"
    assert raises(Select("a"/Int32ub, "b"/Int16ub, "c"/Int8ub, includename=True).build, (("d", 7))) == SelectError
    assert raises(Select(Byte).sizeof) == SizeofError

@xfail(not supportskwordered, reason="ordered kw was introduced in 3.6")
def test_select_kwctor():
    st = Select(a=Int8ub, b=Int16ub, c=Int32ub)
    assert st.parse(b"\x01\x02\x03\x04") == 0x01
    assert st.build(0x01020304) == b"\x01\x02\x03\x04"

def test_optional():
    assert Optional(Int32ul).parse(b"\x01\x00\x00\x00") == 1
    assert Optional(Int32ul).build(1) == b"\x01\x00\x00\x00"
    assert Optional(Int32ul).parse(b"???") == None
    assert Optional(Int32ul).build(None) == b""
    assert raises(Optional(Int32ul).sizeof) == SizeofError

def test_if():
    common(If(True,  Byte), b"\x01", 1, 1)
    common(If(False, Byte), b"", None, 0)

def test_ifthenelse():
    common(IfThenElse(True,  Int8ub, Int16ub), b"\x01", 1, 1)
    common(IfThenElse(False, Int8ub, Int16ub), b"\x00\x01", 1, 2)

def test_switch():
    d = Switch(this.x, {1:Int8ub, 2:Int16ub, 4:Int32ub})
    common(d, b"\x01", 0x01, 1, x=1)
    common(d, b"\x01\x02", 0x0102, 2, x=2)
    assert raises(d.sizeof) == SizeofError
    assert raises(d.parse, b"", x=255) == SwitchError
    assert raises(d.build, 0, x=255) == SwitchError

    d = Switch(this.x, {1:Int8ub, 2:Int16ub, 4:Int32ub}, default=Pass)
    common(d, b"", None, 0, x=255)
    common(d, b"", None, 0, x="unknown")

def test_switch_issue_357():
    inner = Struct(
        "computed" / Computed(4),
    )
    inner2 = Struct(
        "computed" / Computed(7),
    )
    st1 = Struct(
        "a" / inner,
        "b" / Switch(5, {1: inner2}, inner),
        Probe(),
    )
    st2 = Struct(
        "a" / inner,
        "b" / Switch(5, {}, inner),
        Probe(),
    )
    assert st1.parse(b"") == st2.parse(b"")

def test_embeddedswitch():
    d = EmbeddedSwitch(
        Struct(
            "type" / Byte,
        ),
        this.type,
        {
            0: Struct("name" / PascalString(Byte, "utf8")),
            1: Struct("value" / Byte),
        }
    )
    common(d, b"\x00\x00", Container(type=0, name=u"", value=None))
    common(d, b"\x01\x00", Container(type=1, name=None, value=0))

def test_stopif():
    d = Struct("x"/Byte, StopIf(this.x == 0), "y"/Byte)
    common(d, b"\x00", Container(x=0))
    common(d, b"\x01\x02", Container(x=1,y=2))

    d = Sequence("x"/Byte, StopIf(this.x == 0), "y"/Byte)
    common(d, b"\x00", [0])
    common(d, b"\x01\x02", [1,None,2])

    d = GreedyRange(FocusedSeq(0, "x"/Byte, StopIf(this.x == 0)))
    assert d.parse(b"\x01\x00?????") == [1]
    assert d.build([]) == b""
    assert d.build([0]) == b"\x00"
    assert d.build([1]) == b"\x01"
    assert d.build([1,0,2]) == b"\x01\x00"

def test_padding():
    common(Padding(4), b"\x00\x00\x00\x00", None, 4)
    assert raises(Padding, 4, pattern=b"?????") == PaddingError
    assert raises(Padding, 4, pattern=u"?") == PaddingError

def test_padded():
    common(Padded(4, Byte), b"\x01\x00\x00\x00", 1, 4)
    assert raises(Padded, 4, Byte, pattern=b"?????") == PaddingError
    assert raises(Padded, 4, Byte, pattern=u"?") == PaddingError
    assert Padded(4, VarInt).sizeof() == 4
    assert Padded(4, Byte[this.missing]).sizeof() == 4

def test_aligned():
    assert Aligned(4, Byte).parse(b"\x01\x00\x00\x00") == 1
    assert Aligned(4, Byte).build(1) == b"\x01\x00\x00\x00"
    assert Aligned(4, Byte).sizeof() == 4
    assert Struct(Aligned(4, "a"/Byte), "b"/Byte).parse(b"\x01\x00\x00\x00\x02") == Container(a=1)(b=2)
    assert Struct(Aligned(4, "a"/Byte), "b"/Byte).build(Container(a=1)(b=2)) == b"\x01\x00\x00\x00\x02"
    assert Struct(Aligned(4, "a"/Byte), "b"/Byte).sizeof() == 5
    assert Aligned(4, Int8ub).build(1) == b"\x01\x00\x00\x00"
    assert Aligned(4, Int16ub).build(1) == b"\x00\x01\x00\x00"
    assert Aligned(4, Int32ub).build(1) == b"\x00\x00\x00\x01"
    assert Aligned(4, Int64ub).build(1) == b"\x00\x00\x00\x00\x00\x00\x00\x01"
    assert Aligned(this.m, Byte).parse(b"\xff\x00", m=2) == 255
    assert Aligned(this.m, Byte).build(255, m=2) == b"\xff\x00"
    assert Aligned(this.m, Byte).sizeof(m=2) == 2
    assert raises(Aligned(this.m, Byte).sizeof) == SizeofError

def test_alignedstruct():
    assert AlignedStruct(4, "a"/Int8ub, "b"/Int16ub).parse(b"\x01\x00\x00\x00\x00\x05\x00\x00") == Container(a=1)(b=5)
    assert AlignedStruct(4, "a"/Int8ub, "b"/Int16ub).build(dict(a=1,b=5)) == b"\x01\x00\x00\x00\x00\x05\x00\x00"

def test_bitstruct():
    assert BitStruct("a"/BitsInteger(3), "b"/Flag, Padding(3), "c"/Nibble, "d"/BitsInteger(5)).parse(b"\xe1\x1f") == Container(a=7)(b=False)(c=8)(d=31)
    assert BitStruct("a"/BitsInteger(3), "b"/Flag, Padding(3), "c"/Nibble, "d"/BitsInteger(5)).build(Container(a=7)(b=False)(c=8)(d=31)) == b"\xe1\x1f"
    assert BitStruct("a"/BitsInteger(3), "b"/Flag, Padding(3), "c"/Nibble, "d"/BitsInteger(5)).sizeof() == 2
    assert BitStruct("a"/BitsInteger(3), "b"/Flag, Padding(3), "c"/Nibble, "sub"/Struct("d"/Nibble, "e"/Bit)).parse(b"\xe1\x1f") == Container(a=7)(b=False)(c=8)(sub=Container(d=15)(e=1))
    assert BitStruct("a"/BitsInteger(3), "b"/Flag, Padding(3), "c"/Nibble, "sub"/Struct("d"/Nibble, "e"/Bit)).sizeof() == 2
    assert BitStruct("a"/BitsInteger(3), "b"/Flag, Padding(3), "c"/Nibble, "sub"/Struct("d"/Nibble, "e"/Bit)).build(Container(a=7)(b=False)(c=8)(sub=Container(d=15)(e=1))) == b"\xe1\x1f"

def test_pointer():
    common(Pointer(2,             Byte), b"\x00\x00\x07", 7, SizeofError)
    common(Pointer(lambda ctx: 2, Byte), b"\x00\x00\x07", 7, SizeofError)

def test_peek():
    assert Peek(Int8ub).parse(b"\x01") == 1
    assert Peek(Int8ub).parse(b"") == None
    assert Peek(Int8ub).build(1) == b""
    assert Peek(Int8ub).build(None) == b""
    assert Peek(Int8ub).sizeof() == 0
    assert Peek(VarInt).sizeof() == 0
    assert Struct(Peek("a"/Int8ub), "b"/Int16ub).parse(b"\x01\x02") == Container(a=1)(b=0x0102)
    assert Struct(Peek("a"/Int8ub), "b"/Int16ub).build(dict(a=1,b=0x0102)) == b"\x01\x02"
    assert Struct(Peek("a"/Byte), Peek("b"/Int16ub)).parse(b"\x01\x02") == Container(a=1)(b=0x0102)
    assert Struct(Peek("a"/Byte), Peek("b"/Int16ub)).build(dict(a=0,b=0x0102)) == b""
    assert Struct(Peek("a"/Byte), Peek("b"/Int16ub)).sizeof() == 0

def test_seek():
    assert Seek(5).parse(b"") == 5
    assert Seek(5).build(None) == b""
    assert (Seek(5) >> Byte).parse(b"01234x") == [5,120]
    assert (Seek(5) >> Byte).build([5,255]) == b"\x00\x00\x00\x00\x00\xff"
    assert (Bytes(10) >> Seek(5) >> Byte).parse(b"0123456789") == [b"0123456789",5,ord('5')]
    assert (Bytes(10) >> Seek(5) >> Byte).build([b"0123456789",None,255]) == b"01234\xff6789"
    assert Struct("data"/Bytes(10), Seek(5), "addin"/Byte).parse(b"0123456789") == Container(data=b"0123456789")(addin=53)
    assert Struct("data"/Bytes(10), Seek(5), "addin"/Byte).build(dict(data=b"0123456789",addin=53)) == b"01234\x356789"
    assert (Seek(10,1) >> Seek(-5,1) >> Bytes(1)).parse(b"0123456789") == [10,5,b"5"]
    assert (Seek(10,1) >> Seek(-5,1) >> Bytes(1)).build([None,None,255]) == b"\x00\x00\x00\x00\x00\xff"
    assert raises(Seek(5).sizeof) == SizeofError

def test_tell():
    assert Tell.parse(b"") == 0
    assert Tell.build(None) == b""
    assert Tell.sizeof() == 0
    assert Struct("a"/Tell, "b"/Byte, "c"/Tell).parse(b"\xff") == Container(a=0)(b=255)(c=1)
    assert Struct("a"/Tell, "b"/Byte, "c"/Tell).build(Container(a=0)(b=255)(c=1)) == b"\xff"
    assert Struct("a"/Tell, "b"/Byte, "c"/Tell).build(dict(b=255)) == b"\xff"

def test_pass():
    common(Pass, b"", None, 0)
    common(Struct("empty"/Pass), b"", Container(empty=None), 0)

@xfail(reason="unknown cause, Bitwise was reimplemented using TransformData")
def test_terminated():
    common(Terminated, b"", None, 0)
    common(Struct(Terminated), b"", Container(), 0)
    common(BitStruct(Terminated), b"", Container(), 0)
    assert raises(Terminated.parse, b"x") == TerminatedError
    assert raises(Struct(Terminated).parse, b"x") == TerminatedError
    assert raises(BitStruct(Terminated).parse, b"x") == TerminatedError

def test_rawcopy():
    assert RawCopy(Byte).parse(b"\xff") == dict(data=b"\xff", value=255, offset1=0, offset2=1, length=1)
    assert RawCopy(Byte).build(dict(data=b"\xff")) == b"\xff"
    assert RawCopy(Byte).build(dict(value=255)) == b"\xff"
    assert RawCopy(Byte).sizeof() == 1

def test_rawcopy_issue_289():
    # When you build from a full dict that has all the keys, the if data kicks in, and replaces the context entry with a subset of a dict it had to begin with.
    st = Struct(
        "raw" / RawCopy(Struct("x"/Byte, "len"/Byte)),
        "array" / Byte[this.raw.value.len],
    )
    print(st.parse(b"\x01\x02\xff\x00"))
    print(st.build(dict(raw=dict(value=dict(x=1, len=2)), array=[0xff, 0x01])))
    print(st.build(st.parse(b"\x01\x02\xff\x00")))
    # this is not buildable, array is not passed and cannot be deduced from raw data
    # print(st.build(dict(raw=dict(data=b"\x01\x02\xff\x00"))))

def test_rawcopy_issue_358():
    # RawCopy overwritten context value with subcon return obj regardless of None
    d = Struct("a"/RawCopy(Byte), "check"/Check(this.a.value == 255))
    assert d.build(dict(a=dict(value=255))) == b"\xff"

def test_byteswapped():
    d = ByteSwapped(Bytes(5))
    common(d, b"12345", b"54321", 5)
    d = ByteSwapped(Struct("a"/Byte, "b"/Byte))
    common(d, b"\x01\x02", Container(a=2)(b=1), 2)

def test_byteswapped_from_issue_70():
    assert ByteSwapped(BitStruct("flag1"/Bit, "flag2"/Bit, Padding(2), "number"/BitsInteger(16), Padding(4))).parse(b'\xd0\xbc\xfa') == Container(flag1=1)(flag2=1)(number=0xabcd)
    assert BitStruct("flag1"/Bit, "flag2"/Bit, Padding(2), "number"/BitsInteger(16), Padding(4)).parse(b'\xfa\xbc\xd1') == Container(flag1=1)(flag2=1)(number=0xabcd)

def test_bitsswapped():
    d = BitsSwapped(Bytes(2))
    common(d, b"\x0f\x01", b"\xf0\x80", 2)
    d = Bitwise(Bytes(8))
    common(d, b"\xf2", b'\x01\x01\x01\x01\x00\x00\x01\x00', 1)
    d = BitsSwapped(Bitwise(Bytes(8)))
    common(d, b"\xf2", b'\x00\x01\x00\x00\x01\x01\x01\x01', 1)
    d = BitStruct("a"/Nibble, "b"/Nibble)
    common(d, b"\xf1", Container(a=15)(b=1), 1)
    d = BitsSwapped(BitStruct("a"/Nibble, "b"/Nibble))
    common(d, b"\xf1", Container(a=8)(b=15), 1)

def test_bitsswapped_from_issue_145():
    def LBitStruct(*subcons):
        return BitsSwapped(BitStruct(*subcons))
    assert LBitStruct("num"/Octet).parse(b"\x01") == Container(num=0x80)

def test_prefixed():
    assert Prefixed(Byte, Int16ul).parse(b"\x02\xff\xff??????") == 65535
    assert Prefixed(Byte, Int16ul).build(65535) == b"\x02\xff\xff"
    assert Prefixed(Byte, Int16ul).sizeof() == 3
    assert Prefixed(VarInt, GreedyBytes).parse(b"\x03abc??????") == b"abc"
    assert Prefixed(VarInt, GreedyBytes).build(b"abc") == b'\x03abc'
    assert Prefixed(Byte, Int64ub).sizeof() == 9
    assert Prefixed(Byte, Sequence(Peek(Byte), Int16ub, GreedyBytes)).parse(b"\x02\x00\xff????????") == [0,255,b'']
    assert raises(Prefixed(VarInt, GreedyBytes).sizeof) == SizeofError

def test_prefixedarray():
    common(PrefixedArray(Byte,Byte), b"\x02\x0a\x0b", [10,11], SizeofError)
    assert PrefixedArray(Byte, Byte).parse(b"\x03\x01\x02\x03") == [1,2,3]
    assert PrefixedArray(Byte, Byte).parse(b"\x00") == []
    assert PrefixedArray(Byte, Byte).build([1,2,3]) == b"\x03\x01\x02\x03"
    assert raises(PrefixedArray(Byte, Byte).parse, b"") == StreamError
    assert raises(PrefixedArray(Byte, Byte).parse, b"\x03\x01") == StreamError
    assert raises(PrefixedArray(Byte, Byte).sizeof) == SizeofError

def test_restreamdata():
    d = RestreamData(b"\xff", Byte)
    common(d, b"", 255, 0)

def test_transformdata():
    d = TransformData(Bytes(16), bytes2bits, 2, bits2bytes, 16//8)
    common(d, b"\x00"*2, b"\x00"*16, 2)

def test_restreamed():
    assert Restreamed(Int16ub, ident, 1, ident, 1, ident).parse(b"\x00\x01") == 1
    assert Restreamed(Int16ub, ident, 1, ident, 1, ident).build(1) == b"\x00\x01"
    assert Restreamed(Int16ub, ident, 1, ident, 1, ident).sizeof() == 2
    assert raises(Restreamed(VarInt, ident, 1, ident, 1, ident).sizeof) == SizeofError
    assert Restreamed(Bytes(2), lambda b: b*2, 1, None, None, None).parse(b"a") == b"aa"
    assert Restreamed(Bytes(1), None, None, lambda b: b*2, 1, None).build(b"a") == b"aa"
    assert Restreamed(Bytes(5), None, None, None, None, lambda n: n*2).sizeof() == 10

def test_restreamed_partial_read():
    d = Restreamed(Bytes(255), ident, 1, ident, 1, ident)
    assert raises(d.parse, b"") == StreamError

def test_checksum():
    d = Struct(
        "fields" / RawCopy(Struct(
            "a" / Byte,
            "b" / Byte,
        )),
        "checksum" / Checksum(Bytes(64), lambda data: hashlib.sha512(data).digest(), this.fields.data),
    )

    c = hashlib.sha512(b"\x01\x02").digest()
    assert d.parse(b"\x01\x02"+c) == Container(fields=dict(data=b"\x01\x02", value=Container(a=1)(b=2), offset1=0, offset2=2, length=2))(checksum=c)
    assert d.build(dict(fields=dict(data=b"\x01\x02"))) == b"\x01\x02"+c
    assert d.build(dict(fields=dict(value=dict(a=1,b=2)))) == b"\x01\x02"+c

def test_checksum_nonbytes_issue_323():
    st = Struct(
        "vals" / Byte[2],
        "checksum" / Checksum(Byte, lambda vals: sum(vals) & 0xFF, this.vals),
    )
    assert st.parse(b"\x00\x00\x00") == Container(vals=[0, 0])(checksum=0)
    assert raises(st.parse, b"\x00\x00\x01") == ChecksumError

def test_compressed_zlib():
    zeros = bytes(10000)
    d = Compressed(GreedyBytes, "zlib")
    assert d.parse(d.build(zeros)) == zeros
    assert len(d.build(zeros)) < 50
    assert raises(d.sizeof) == SizeofError
    d = Compressed(GreedyBytes, "zlib", level=9)
    assert d.parse(d.build(zeros)) == zeros
    assert len(d.build(zeros)) < 50
    assert raises(d.sizeof) == SizeofError

@xfail(not PY>=(3,2), raises=AttributeError, reason="gzip module was added in 3.2")
def test_compressed_gzip():
    zeros = bytes(10000)
    d = Compressed(GreedyBytes, "gzip")
    assert d.parse(d.build(zeros)) == zeros
    assert len(d.build(zeros)) < 50
    assert raises(d.sizeof) == SizeofError
    d = Compressed(GreedyBytes, "gzip", level=9)
    assert d.parse(d.build(zeros)) == zeros
    assert len(d.build(zeros)) < 50
    assert raises(d.sizeof) == SizeofError

def test_compressed_bzip2():
    zeros = bytes(10000)
    d = Compressed(GreedyBytes, "bzip2")
    assert d.parse(d.build(zeros)) == zeros
    assert len(d.build(zeros)) < 50
    assert raises(d.sizeof) == SizeofError
    d = Compressed(GreedyBytes, "bzip2", level=9)
    assert d.parse(d.build(zeros)) == zeros
    assert len(d.build(zeros)) < 50
    assert raises(d.sizeof) == SizeofError

@xfail(not PY>=(3,3), raises=ImportError, reason="lzma module was added in 3.3")
def test_compressed_lzma():
    zeros = bytes(10000)
    d = Compressed(GreedyBytes, "lzma")
    assert d.parse(d.build(zeros)) == zeros
    assert len(d.build(zeros)) < 200
    assert raises(d.sizeof) == SizeofError
    d = Compressed(GreedyBytes, "lzma", level=9)
    assert d.parse(d.build(zeros)) == zeros
    assert len(d.build(zeros)) < 200
    assert raises(d.sizeof) == SizeofError

def test_compressed_prefixed():
    zeros = bytes(10000)
    d = Prefixed(VarInt, Compressed(GreedyBytes, "zlib"))
    st = Struct("one"/d, "two"/d)
    assert st.parse(st.build(Container(one=zeros,two=zeros))) == Container(one=zeros,two=zeros)
    assert raises(d.sizeof) == SizeofError

def test_rebuffered():
    data = b"0" * 1000
    assert Rebuffered(Array(1000,Byte)).parse_stream(io.BytesIO(data)) == [48]*1000
    assert Rebuffered(Array(1000,Byte), tailcutoff=50).parse_stream(io.BytesIO(data)) == [48]*1000
    assert Rebuffered(Byte).sizeof() == 1
    assert raises(Rebuffered(Byte).sizeof) == None
    assert raises(Rebuffered(VarInt).sizeof) == SizeofError

def test_lazybound():
    d = LazyBound(lambda: Byte)
    common(d, b"\x01", 1)

    d = Struct(
        "value" / Byte,
        "next" / If(this.value > 0, LazyBound(lambda: d)),
    )
    common(d, b"\x05\x09\x00", Container(value=5)(next=Container(value=9)(next=Container(value=0)(next=None))))

    d = Struct(
        "value" / Byte,
        "next" / GreedyBytes,
    )
    data = b"\x05\x09\x00"
    while data:
        x = d.parse(data)
        data = x.next
        print(x)

def test_expradapter():
    MulDiv = ExprAdapter(Byte, obj_ * 7, obj_ // 7)
    assert MulDiv.parse(b"\x06") == 42
    assert MulDiv.build(42) == b"\x06"
    assert MulDiv.sizeof() == 1

    Ident = ExprAdapter(Byte, obj_-1, obj_+1)
    assert Ident.parse(b"\x02") == 1
    assert Ident.build(1) == b"\x02"
    assert Ident.sizeof() == 1

def test_exprsymmetricadapter():
    pass

def test_exprvalidator():
    One = ExprValidator(Byte, lambda obj,ctx: obj in [1,3,5])
    assert One.parse(b"\x01") == 1
    assert raises(One.parse, b"\xff") == ValidationError
    assert One.build(5) == b"\x05"
    assert raises(One.build, 255) == ValidationError
    assert One.sizeof() == 1

def test_ipaddress_adapter_issue_95():
    class IpAddressAdapter(Adapter):
        def _encode(self, obj, context, path):
            return list(map(int, obj.split(".")))
        def _decode(self, obj, context, path):
            return "{0}.{1}.{2}.{3}".format(*obj)
    IpAddress = IpAddressAdapter(Byte[4])

    assert IpAddress.parse(b"\x7f\x80\x81\x82") == "127.128.129.130"
    assert IpAddress.build("127.1.2.3") == b"\x7f\x01\x02\x03"
    assert IpAddress.sizeof() == 4

    IpAddress = ExprAdapter(Byte[4],
        encoder = lambda obj,ctx: list(map(int, obj.split("."))),
        decoder = lambda obj,ctx: "{0}.{1}.{2}.{3}".format(*obj), )

    assert IpAddress.parse(b"\x7f\x80\x81\x82") == "127.128.129.130"
    assert IpAddress.build("127.1.2.3") == b"\x7f\x01\x02\x03"
    assert IpAddress.sizeof() == 4

def test_oneof():
    assert OneOf(Byte,[4,5,6,7]).parse(b"\x05") == 5
    assert OneOf(Byte,[4,5,6,7]).build(5) == b"\x05"
    assert raises(OneOf(Byte,[4,5,6,7]).parse, b"\x08") == ValidationError
    assert raises(OneOf(Byte,[4,5,6,7]).build, 8) == ValidationError

def test_noneof():
    assert NoneOf(Byte,[4,5,6,7]).parse(b"\x08") == 8
    assert raises(NoneOf(Byte,[4,5,6,7]).parse, b"\x06") == ValidationError

def test_filter():
    assert Filter(obj_ != 0, Byte[:]).parse(b"\x00\x02\x00") == [2]
    assert Filter(obj_ != 0, Byte[:]).build([0,1,0,2,0]) == b"\x01\x02"

def test_slicing():
    assert Slicing(Array(4,Byte), 4, 1, 3, empty=0).parse(b"\x01\x02\x03\x04") == [2,3]
    assert Slicing(Array(4,Byte), 4, 1, 3, empty=0).build([2,3]) == b"\x00\x02\x03\x00"
    assert Slicing(Array(4,Byte), 4, 1, 3, empty=0).sizeof() == 4

def test_indexing():
    assert Indexing(Array(4,Byte), 4, 2, empty=0).parse(b"\x01\x02\x03\x04") == 3
    assert Indexing(Array(4,Byte), 4, 2, empty=0).build(3) == b"\x00\x00\x03\x00"
    assert Indexing(Array(4,Byte), 4, 2, empty=0).sizeof() == 4

def test_probe():
    Probe().parse(b"")
    Probe().build(None)
    Struct("inserted"/Probe()).parse(b"")
    Struct("inserted"/Probe()).build({})

def test_probeinto():
    Struct("inner"/Struct("nums"/Byte[:]), ProbeInto(this.inner)).parse(b"\x01\xff")
    Struct("inner"/Struct("nums"/Byte[:]), ProbeInto(this.inner)).build(dict(inner=dict(nums=[1,255])))
    Struct(ProbeInto(this.inner)).parse(b"")
    Struct(ProbeInto(this.inner)).build({})

def test_operators():
    common(Struct("new" / ("old" / Byte)), b"\x01", Container(new=1), 1)
    common(Struct(Renamed(Renamed(Byte, newname="old"), newname="new")), b"\x01", Container(new=1), 1)

    common(Array(4, Byte), b"\x01\x02\x03\x04", [1,2,3,4], 4)
    common(Byte[4], b"\x01\x02\x03\x04", [1,2,3,4], 4)
    common(Struct("nums" / Byte[4]), b"\x01\x02\x03\x04", Container(nums=[1,2,3,4]), 4)

    common(Int8ub >> Int16ub, b"\x01\x00\x02", [1,2], 3)
    common(Int8ub >> Int16ub >> Int32ub, b"\x01\x00\x02\x00\x00\x00\x03", [1,2,3], 7)
    common(Int8ub[2] >> Int16ub[2], b"\x01\x02\x00\x03\x00\x04", [[1,2],[3,4]], 6)

    common(Sequence(Embedded(Sequence(Int8ub)), Embedded(Sequence(Int16ub)) ), b"\x01\x00\x02", [1,2], 3)
    common(Sequence(Int8ub) >> Sequence(Int16ub), b"\x01\x00\x02", [1,2], 3)
    common(Struct("count"/Byte, "items"/Byte[this.count], Pass, Terminated), b"\x03\x01\x02\x03", Container(count=3)(items=[1,2,3]), SizeofError)
    common("count"/Byte + "items"/Byte[this.count] + Pass + Terminated, b"\x03\x01\x02\x03", Container(count=3)(items=[1,2,3]), SizeofError)
    common(Struct(Embedded(Struct(a=Byte)), Embedded(Struct(b=Byte)) ), b"\x01\x02", Container(a=1)(b=2), 2)
    common(Struct(a=Byte) + Struct(b=Byte), b"\x01\x02", Container(a=1)(b=2), 2)

    d = Byte * "description"
    assert d.docs == "description"
    d = "description" * Byte
    assert d.docs == "description"
    """
    description
    """ * \
    Byte
    assert d.docs == "description"
    d = Renamed(Renamed(Byte, newdocs="old"), newdocs="new")
    assert d.docs == "new"

def test_operators_issue_87():
    assert ("string_name" / Byte).parse(b"\x01") == 1
    assert (u"unicode_name" / Byte).parse(b"\x01") == 1
    assert (b"bytes_name" / Byte).parse(b"\x01") == 1
    assert (None / Byte).parse(b"\x01") == 1

def test_from_issue_76():
    assert Aligned(4, Struct("a"/Byte, "f"/Bytes(lambda ctx: ctx.a))).parse(b"\x02\xab\xcd\x00") == Container(a=2)(f=b"\xab\xcd")
    assert Aligned(4, Struct("a"/Byte, "f"/Bytes(lambda ctx: ctx.a))).build(Container(a=2)(f=b"\xab\xcd")) == b"\x02\xab\xcd\x00"

def test_from_issue_60():
    Header = Struct(
        "type" / Int8ub,
        "size" / Switch(lambda ctx: ctx.type,
        {
            0: Int8ub,
            1: Int16ub,
            2: Int32ub,
        }),
        "length" / Tell,
    )
    assert Header.parse(b"\x00\x05")             == Container(type=0)(size=5)(length=2)
    assert Header.parse(b"\x01\x00\x05")         == Container(type=1)(size=5)(length=3)
    assert Header.parse(b"\x02\x00\x00\x00\x05") == Container(type=2)(size=5)(length=5)
    assert Header.build(dict(type=0, size=5)) == b"\x00\x05"
    assert Header.build(dict(type=1, size=5)) == b"\x01\x00\x05"
    assert Header.build(dict(type=2, size=5)) == b"\x02\x00\x00\x00\x05"

    HeaderData = Struct(
        Embedded(Header),
        "data" / Bytes(lambda ctx: ctx.size),
    )
    assert HeaderData.parse(b"\x00\x0512345")             == Container(type=0)(size=5)(length=2)(data=b"12345")
    assert HeaderData.parse(b"\x01\x00\x0512345")         == Container(type=1)(size=5)(length=3)(data=b"12345")
    assert HeaderData.parse(b"\x02\x00\x00\x00\x0512345") == Container(type=2)(size=5)(length=5)(data=b"12345")
    assert HeaderData.build(dict(type=0, size=5, data=b"12345")) == b"\x00\x0512345"
    assert HeaderData.build(dict(type=1, size=5, data=b"12345")) == b"\x01\x00\x0512345"
    assert HeaderData.build(dict(type=2, size=5, data=b"12345")) == b"\x02\x00\x00\x00\x0512345"

def test_from_issue_171():
    attributes = BitStruct(
        "attr" / Aligned(8, Array(3, Struct(
            "attrCode" / BitsInteger(16),
            "attrValue" / Switch(this.attrCode, {
                34: BitsInteger(8),
                205: BitsInteger(2),
                512: BitsInteger(2)
            }),
        ))),
    )
    blob = b"\x00\x22\x82\x00\xCD\x80\x80\x10"
    assert attributes.parse(blob) == Container(attr=[
        Container(attrCode=34)(attrValue=130),
        Container(attrCode=205)(attrValue=2),
        Container(attrCode=512)(attrValue=1), ])

def test_from_issue_175():
    @FuncPath
    def comp_(num_array):
        return sum(x << ((len(num_array)-1-i)*8) for i,x in enumerate(num_array))

    test = Struct(
        "numArray" / RepeatUntil(obj_ < 128, Byte),
        "value" / Computed(comp_(this.numArray))
    )
    assert test.parse(b'\x87\x0f').value == 34575

def test_from_issue_71():
    Inner = Struct(
        'name' / PascalString(Byte, "utf8"),
        'occupation' / PascalString(Byte, "utf8"),
    )
    Outer = Struct(
        'struct_type' / Int16ub,
        'payload_len' / Int16ub,
        'payload' / RawCopy(Inner),
        'serial' / Int16ub,
        'checksum' / Checksum(Bytes(64),
            lambda data: hashlib.sha512(data).digest(),
            this.payload.data),
        Check(len_(this.payload.data) == this.payload_len),
        Terminated,
    )

    payload = Inner.build(Container(
        name=u"unknown",
        occupation=u"worker",
        ))
    Outer.build(Container(
        struct_type=9001,
        payload_len=len(payload),
        payload=Container(data=payload),
        serial=12345,
        ))

def test_from_issue_231():
    u = Union(0, "raw"/Byte[8], "ints"/Int[2])
    s = Struct("u"/u, "d"/Byte[4])

    buildret = s.build(dict(u=dict(ints=[1,2]),d=[0,1,2,3]))
    assert buildret == b"\x00\x00\x00\x01\x00\x00\x00\x02\x00\x01\x02\x03"
    assert s.build(s.parse(buildret)) == buildret

def test_from_issue_246():
    NumVertices = Bitwise(Aligned(8, Struct(
        'numVx4' / BitsInteger(4),
        'numVx8' / If(this.numVx4 == 0, BitsInteger(8)),
        'numVx16' / If(this.numVx4 == 0 & this.numVx8 == 255, BitsInteger(16)),
    )))
    common(NumVertices, b'\x02\x30', Container(numVx4=0, numVx8=35, numVx16=None))

    testBit = BitStruct(
        'a' / BitsInteger(8),
        'b' / If(this.a == 97, BitsInteger(8))
    )
    testByte = Struct(
        'a' / Byte,
        'b' / If(this.a == 97, Byte)
    )
    common(testBit, b'ab', Container(a=97, b=98))
    common(testByte, b'ab', Container(a=97, b=98))

    NumVertices = Union(None,
        'numVx4' / Bitwise(Aligned(8, Struct('num'/ BitsInteger(4) ))),
        'numVx8' / Bitwise(Aligned(8, Struct('num'/ BitsInteger(12)))),
        'numVx16'/ Bitwise(Aligned(8, Struct('num'/ BitsInteger(28)))),
    )
    assert NumVertices.parse(b'\x01\x34\x56\x70') == Container(numVx4=Container(num=0))(numVx8=Container(num=19))(numVx16=Container(num=1262951))

def test_from_issue_244():
    class AddIndexes(Adapter):
        def __init__(self, subcon):
            super(AddIndexes, self).__init__(subcon)
        def _decode(self, obj, context, path):
            for i,con in enumerate(obj):
                con.index = i
            return obj

    assert AddIndexes(Struct("num"/Byte)[4]).parse(b"abcd") == [Container(num=97)(index=0),Container(num=98)(index=1),Container(num=99)(index=2),Container(num=100)(index=3),]

def test_from_issue_269():
    st = Struct("enabled" / Byte, If(this.enabled, Padding(2)))
    assert st.build(dict(enabled=1)) == b"\x01\x00\x00"
    assert st.build(dict(enabled=0)) == b"\x00"
    st = Struct("enabled" / Byte, "pad" / If(this.enabled, Padding(2)))
    assert st.build(dict(enabled=1)) == b"\x01\x00\x00"
    assert st.build(dict(enabled=0)) == b"\x00"

def test_hanging_issue_280():
    st = BitStruct('a'/BitsInteger(20), 'b'/BitsInteger(12))
    assert raises(st.parse, b'\x00') == StreamError

def test_from_issue_324():
    d = Struct(
        "vals" / Prefixed(Byte, RawCopy(
            Struct("a" / Byte[2]),
        )),
        "checksum" / Checksum(
            Byte,
            lambda data: sum(iterateints(data)) & 0xFF,
            this.vals.data
        ),
    )
    assert d.build(dict(vals=dict(value=dict(a=[0,1])))) == b"\x02\x00\x01\x01"
    assert d.build(dict(vals=dict(data=b"\x00\x01"))) == b"\x02\x00\x01\x01"

def test_from_issue_357():
    inner = Struct(
        "computed" / Computed(4),
    )
    st1 = Struct(
        "a" / inner,
        Check(this.a.computed == 4),
    )
    st2 = Struct(
        "b" / Switch(0, {}, inner),
        Check(this.b.computed == 4),
    )
    assert st1.build(dict(a={})) == b""
    assert st2.build(dict(b={})) == b""

def test_context_is_container():
    st = Struct(Check(lambda ctx: type(ctx) is Container))
    st.parse(b"")

def test_from_issue_362():
    FORMAT = Struct(
        "my_tell" / Tell,
        "my_byte" / Byte,
    )
    BIT_FORMAT = BitStruct(
        "my_tell" / Tell,
        "my_bits" / Bit[8],
    )
    for i in range(5):
        assert FORMAT.parse(b'\x00').my_tell == 0
    for i in range(5):
        assert BIT_FORMAT.parse(b'\x00').my_tell == 0

def test_compiler_recursion():
    raises(Construct().compile) == NotImplementedError

@xfail(reason="unknown cause")
def test_this_expresion_compare_container():
    # lambda is fine, but this equality with Container fails
    st = Struct(
        "flags" / FlagsEnum(Byte, a=1),
        Check(this.flags == Container(a=1)),
    )
    common(st, b"\x01", dict(flags=Container(a=True)), 1)

@xfail(not supportscompiler, reason="compiler requires Python 3.6")
def test_empty_struct_compiled():
    Struct().compile()
    Sequence().compile()

@xfail(not supportscompiler, reason="compiler requires Python 3.6")
def test_compiled_benchmark_testcompiled():
    Struct().compile().benchmark(b"")
    Struct().compile().testcompiled(b"")

@xfail(reason="unknown causes")
def test_pickling_constructs():
    # it seems there are few problems:
    # - this expressions, ExprMixin added __get(set)state__
    # - CompilableMacro not pickle, eg. IfThenElse
    # what was fixed so far:
    # - singleton decorator adds __reduce__ to instance

    import pickle

    d = Struct(
        "count" / Byte,
        "greedybytes" / Prefixed(Byte, GreedyBytes),
        "formatfield" / FormatField("=","Q"),
        "bytesinteger" / BytesInteger(1),
        "varint" / VarInt,
        "text1" / PascalString(Byte, "utf8"),
        "text2" / CString("utf8"),
        "enum" / Enum(Byte, zero=0),
        "flagsenum" / FlagsEnum(Byte, zero=0),
        "array1" / Byte[5],
        # - uses this-expression
        # "array2" / Byte[this.count],
        "greedyrange" / Prefixed(Byte, GreedyRange(Byte)),
        # - its a macro around Switch, should reimplement
        # "if1" / IfThenElse(True, Byte, Byte),
        "padding" / Padding(1),
        "peek" / Peek(Byte),
        "tell" / Tell,
        # - unknown causes
        # "this1" / Byte[this.count],
        # "obj_1" / RepeatUntil(obj_ == 0, Byte),
        # "len_1" / Computed(len_(this.array1)),
    )
    data = b"\x00"*100

    du = pickle.loads(pickle.dumps(d))
    assert du.parse(data) == d.parse(data)

def test_exposing_members():
    d = Struct(
        "count" / Byte,
        "data" / Bytes(lambda this: this.count - this._subcons.count.sizeof()),
        Check(lambda this: this._subcons.count.sizeof() == 1),
    )
    common(d, b"\x05four", Container(count=5, data=b"four"))

    d = Sequence(
        "count" / Byte,
        "data" / Bytes(lambda this: this.count - this._subcons.count.sizeof()),
        Check(lambda this: this._subcons.count.sizeof() == 1),
    )
    common(d, b"\x05four", [5,b"four",None])

    d = Union(None,
        "count" / Byte,
        Check(lambda this: this._subcons.count.sizeof() == 1),
    )
    common(d, b"\x05", Container(count=5))

    d = FocusedSeq(0,
        "count" / Byte,
        Check(lambda this: this._subcons.count.sizeof() == 1),
    )
    common(d, b"\x05", 5, 1)
