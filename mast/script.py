from itertools import *
import crypto
import collections
def setG(n,v):
    globals()[n] = v
names = lambda name, bot, top, offset=0: map(lambda num: setG(name%(num-offset), num), xrange(bot, top+1))
OP_0 = OP_FALSE  =0
names("OP_NA%d", 1, 75, 0)
OP_PUSHDATA1    =76
OP_PUSHDATA2    =77
OP_PUSHDATA4    =78
OP_1NEGATE  =79
OP_RESERVED = 80
OP_1= OP_TRUE   =81
names("OP_%d", 82, 96, 80)
OP_NOP  =97
OP_VER = 98
OP_IF   =99
OP_NOTIF    =100
OP_VERIF = 101
OP_VERNOTIF = 102
OP_ELSE =103
OP_ENDIF    =104
OP_VERIFY   =105
OP_RETURN   =106
OP_TOALTSTACK   =107
OP_FROMALTSTACK =108
OP_2DROP    =109
OP_2DUP =110
OP_3DUP =111
OP_2OVER    =112
OP_2ROT =113
OP_2SWAP    =114
OP_IFDUP    =115
OP_DEPTH    =116
OP_DROP =117
OP_DUP  =118
OP_NIP  =119
OP_OVER =120
OP_PICK =121
OP_ROLL =122
OP_ROT  =123
OP_SWAP =124
OP_TUCK =125
OP_CAT  =126
OP_SUBSTR   =127
OP_LEFT =128
OP_RIGHT    =129
OP_SIZE =130
OP_INVERT   =131
OP_AND  =132
OP_OR   =133
OP_XOR  =134
OP_EQUAL    =135
OP_EQUALVERIFY  =136
OP_RESERVED1    =137
OP_RESERVED2    =138
OP_1ADD =139
OP_1SUB =140
OP_2MUL =141
OP_2DIV =142
OP_NEGATE   =143
OP_ABS  =144
OP_NOT  =145
OP_0NOTEQUAL    =146
OP_ADD  =147
OP_SUB  =148
OP_MUL  =149
OP_DIV  =150
OP_MOD  =151
OP_LSHIFT   =152
OP_RSHIFT   =153
OP_BOOLAND  =154
OP_BOOLOR   =155
OP_NUMEQUAL =156
OP_NUMEQUALVERIFY   =157
OP_NUMNOTEQUAL  =158
OP_LESSTHAN =159
OP_GREATERTHAN  =160
OP_LESSTHANOREQUAL  =161
OP_GREATERTHANOREQUAL   =162
OP_MIN  =163
OP_MAX  =164
OP_WITHIN   =165
OP_RIPEMD160    =166
OP_SHA1 =167
OP_SHA256   =168
OP_HASH160  =169
OP_HASH256  =170
OP_CODESEPARATOR    =171
OP_CHECKSIG =172
OP_CHECKSIGVERIFY   =173
OP_CHECKMULTISIG    =174
OP_CHECKMULTISIGVERIFY  =175
names("OP_NOP%d", 176, 186)
# handler: op, stack -> Iterable inst -> 
class incrementer():
    def __init__(self):
        self.count = 0
        self.last = collections.deque()
    def up(self):
        self.count+=1
    def down(self):
        self.count-=1
    def st(self):
        return self.count
class InvalidOpcode(Exception):
    @classmethod
    def rz(cls, m):
        raise InvalidOpcode(m)
def verify(stack, inst):
    import sys
    if stack[-1] == 0:
        sys.exit()
genHandler = lambda h, bot, top: map(lambda num: (num, h(num)), xrange(bot, top+1))
genHandlers = lambda invalidate, stack, inst: dict(chain(
[(OP_0,lambda:(stack.append(bytes(0)),inst.next()))
,(OP_PUSHDATA1,lambda:(stack.append("".join([chr(inst.next()) for x in range(inst.next())])),inst.next())) #TODO
,(OP_PUSHDATA2,lambda:(inst.next()))#TODO
,(OP_PUSHDATA4,lambda:(inst.next())) #TODO
,(OP_1NEGATE,lambda:(stack.append(-1),inst.next()))
,(OP_1,lambda:(stack.append(1),inst.next()))
,(OP_NOP,lambda:(inst.next(),))
,(OP_IF,lambda:( (ifexec(True),inst.next())[-1] if stack.pop() != 0
                else (ifexec(False),dropwhile( lambda x: x not in [OP_ELSE, OP_ENDIF],inst).next())[-1],))
,(OP_NOTIF,lambda:( (ifexec(True),inst.next())[-1] if stack.pop() == 0
                else (ifexec(False), dropwhile(lambda x: x not in [OP_ELSE, OP_ENDIF],inst).next())[-1],))
,(OP_ELSE,lambda:( (ifexec(True),inst.next())[-1] if stack.pop() == 0
                else (ifexec(False), dropwhile( lambda x: (not didifexec()) and (x != OP_ELSE or x!= OP_ENDIF),inst).next())[-1],))
,(OP_ENDIF,lambda:(endif(),inst.next()))
,(OP_VERIFY,lambda:(verify(stack,inst), invalidate() if stack[-1] == 0 else (invalidate() if stack[-1] != 1 else 0) ,inst.next()))
,(OP_RETURN,lambda:(invalidate(),inst.next()))
,(OP_TOALTSTACK,lambda:(stack.pop(),inst.next())) # TODO
,(OP_FROMALTSTACK,lambda:(0,inst.next())) # TODO
,(OP_2DROP,lambda:(stack.pop(), stack.pop(),inst.next()))
,(OP_2DUP,lambda:(stack.append(stack[-2]), stack.append(stack[-2]),inst.next()))
,(OP_3DUP,lambda:(stack.append(stack[-3]), stack.append(stack[-3]), stack.append(stack[-3]),inst.next()))
,(OP_2OVER,lambda:(stack.append(stack[-4]), stack.append(stack[-4]),inst.next()))
,(OP_2ROT,lambda:(stack.extend(chain([stack.pop(),stack.pop(),stack.pop(),stack.pop()][::-1],[stack.pop(), stack.pop()][::-1]))     ,inst.next()))
,(OP_2SWAP,lambda:(stack.extend(chain( [stack.pop(),stack.pop()][::-1], [stack.pop(),stack.pop()][::-1]  )),inst.next()))
,(OP_IFDUP,lambda:(stack.append(stack[-1]) if stack[-1] != 0 else None,inst.next()))
,(OP_DEPTH,lambda:(stack.append(len(stack)),inst.next()))
,(OP_DROP,lambda:(stack.pop(),inst.next()))
,(OP_DUP,lambda:(stack.append(stack[-1]),inst.next()))
,(OP_NIP,lambda:(stack.append((stack.pop(), stack.pop())[0]),inst.next()))
,(OP_OVER,lambda:(stack.append(stack[-2]),inst.next()))
,(OP_PICK,lambda:(stack.append(stack[-stack.pop()]),inst.next()))
,(OP_ROLL,lambda:(stack.extend(chain([stack.pop() for x in xrange(stack.pop())][::-1], [stack.pop()])),inst.next()))
,(OP_ROT,lambda:( stack.extend(chain([stack.pop(), stack.pop()][::-1], [stack.pop()])) ,inst.next()))
,(OP_SWAP,lambda:(stack.extend([stack.pop(),stack.pop()]),inst.next()))
,(OP_TUCK,lambda:( stack.extend(chain([stack[-2]], [stack.pop(), stack.pop()][::-1]))  ,inst.next()))
,(OP_CAT,lambda:(stack.append(reduce(lambda x,y: x+y, [stack.pop(),stack.pop()][::-1])),inst.next()))
,(OP_SUBSTR,lambda:(InvalidOpcode.rz("OP_SUBSTR"),inst.next()))
,(OP_LEFT,lambda:(InvalidOpcode.rz("OP_LEFT"),inst.next()))
,(OP_RIGHT,lambda:(InvalidOpcode.rz("OP_RIGHT"),inst.next()))
,(OP_SIZE,lambda:(stack.append(len(stack[-1]),inst.next())))
,(OP_INVERT,lambda:(InvalidOpcode.rz("OP_INVERT"),inst.next()))
,(OP_AND,lambda:(InvalidOpcode.rz("OP_AND"),inst.next()))
,(OP_OR,lambda:(InvalidOpcode.rz("OP_OR"),inst.next()))
,(OP_XOR,lambda:(InvalidOpcode.rz("OP_XOR"),inst.next()))
,(OP_EQUAL,lambda:(stack.append(int(stack.pop() == stack.pop())),inst.next()))
,(OP_EQUALVERIFY,lambda:(stack.append(int(stack.pop() == stack.pop())),OP_VERIFY))
,(OP_RESERVED1,lambda:(invalidate(),inst.next()))
,(OP_RESERVED2,lambda:(invalidate(),inst.next()))
,(OP_RESERVED,lambda:(invalidate(),inst.next()))
,(OP_VERIF,lambda:(invalidate(),inst.next()))
,(OP_VERNOTIF,lambda:(invalidate(),inst.next()))
,(OP_VER,lambda:(invalidate(),inst.next()))
,(OP_1ADD,lambda:(stack.append(stack.pop()+1) ,inst.next()))
,(OP_1SUB,lambda:(stack.append(stack.pop()-1),inst.next()))
,(OP_2MUL,lambda:(InvalidOpcode.rz("OP_2MUL"), stack.__setitem__(-1, stack[-1]*2),inst.next()))
,(OP_2DIV,lambda:(InvalidOpcode.rz("OP_2DIV"),inst.next()))
,(OP_NEGATE,lambda:(stack.append(-stack.pop()),inst.next()))
,(OP_ABS,lambda:(stack.append(abs(stack.pop())),inst.next()))
,(OP_NOT,lambda:(stack.append((1,0)[stack.pop()] if stack[-1] in[0,1] else stack.pop()),inst.next()))
,(OP_0NOTEQUAL,lambda:(stack.append(0 if stack[-1] == 0 else 1) ,inst.next()))
,(OP_ADD,lambda:(stack.append(stack.pop()+stack.pop()),inst.next()))
,(OP_SUB,lambda:(stack.append(-stack.pop()+stack.pop()),inst.next()))
,(OP_MUL,lambda:(InvalidOpcode.rz("OP_MUL"),inst.next()))
,(OP_DIV,lambda:(InvalidOpcode.rz("OP_DIV"),inst.next()))
,(OP_MOD,lambda:(InvalidOpcode.rz("OP_MOD"),inst.next()))
,(OP_LSHIFT,lambda:(InvalidOpcode.rz("OP_LSHIFT"),inst.next()))
,(OP_RSHIFT,lambda:(InvalidOpcode.rz("OP_RSHIFT"),inst.next()))
,(OP_BOOLAND,lambda:(stack.append(1 if stack.pop() != 0 and stack.pop() != 0 else 0),inst.next()))
,(OP_BOOLOR,lambda:(stack.append(0 if stack.pop() == 0 and stack.pop() == 0 else 1),inst.next()))
,(OP_NUMEQUAL,lambda:(stack.append(1 if stack.pop() == stack.pop() else 0,inst.next())))
,(OP_NUMEQUALVERIFY,lambda:(stack.append(1 if stack.pop() == stack.pop() else 0),OP_VERIFY))
,(OP_NUMNOTEQUAL,lambda:(stack.append(0 if stack.pop() == stack.pop() else 1),inst.next()))
,(OP_LESSTHAN,lambda:(stack.append( 1 if stack.pop() > stack.pop() else 0),inst.next()))
,(OP_GREATERTHAN,lambda:(stack.append(1 if stack.pop() < stack.pop() else 0),inst.next()))
,(OP_LESSTHANOREQUAL,lambda:(stack.append(1 if stack.pop() >= stack.pop() else 0),inst.next()))
,(OP_GREATERTHANOREQUAL,lambda:(stack.append( 1 if stack.pop() <= stack.pop() else 0),inst.next()))
,(OP_MIN,lambda:(stack.append(min(stack.pop(), stack.pop())),inst.next()))
,(OP_MAX,lambda:(stack.append(min(stack.pop(), stack.pop()),inst.next())))
,(OP_WITHIN,lambda:(stack.append( 1 if stack[-2] <= stackstack[-1] < stack[-3] else 0   ), stack.pop(), stack.pop(), stack.pop(),inst.next()))
,(OP_RIPEMD160,lambda:(stack.append(crypto.ripemd160(stack.pop())),inst.next()))
,(OP_SHA1,lambda:(stack.append(crypto.sha1(stack.pop())),inst.next()))
,(OP_SHA256,lambda:(stack.append(crypto.hash(stack.pop())),inst.next()))
,(OP_HASH160,lambda:(stack.append(crypto.ripemd160(crypto.sha256(stack.pop()))),inst.next()))
,(OP_HASH256,lambda:(stack.append(crypto.hash(crypto.hash(stack.pop()))),inst.next()))
,(OP_CODESEPARATOR,lambda:(InvalidOpcode.rz("Implement this plz",inst.next()))) #TODO what does this do?
,(OP_CHECKSIG,lambda:( stack.append(1 if  signed(stack.pop(),stack.pop()) else 0),inst.next()))
,(OP_CHECKSIGVERIFY,lambda:( stack.append(1 if  signed(stack.pop(),stack.pop()) else 0),OP_VERIFY))
,(OP_CHECKMULTISIG,lambda:(None,inst.next())) #TODO
,(OP_CHECKMULTISIGVERIFY,lambda:(None,inst.next())) #TODO
]
# OP_NA
,genHandler(lambda num: lambda: (stack.append("".join([chr(inst.next()) for _ in xrange(num)])), inst.next()), 1, 75)
# OP_int
,genHandler(lambda num: lambda: (stack.append(num-80), inst.next()), 82, 96)
# OP_NOP
,genHandler(lambda _: lambda: (inst.next(),) , 176, 186)))

DISABLED_OPS = set([ OP_SUBSTR, OP_LEFT, OP_RIGHT, OP_INVERT, OP_XOR,
OP_OR, OP_AND, OP_2MUL, OP_2DIV, OP_MUL, OP_DIV, OP_LSHIFT, OP_RSHIFT])
def run(s):
    inst = toInst(s)
    if_state = incrementer()
    invalid = chain(iter([1]), repeat(0))
    def invalidate():
        invalid.next()
    ifexec = lambda b: if_state.last.append(b)
    didifexec = lambda: if_state.last.pop
    endif = if_state.last.pop
    stack = collections.deque()
    iinst = iter(inst)
    handlers = genHandlers(invalidate, stack, iinst)
    try:
        handle(handlers, iinst.next(),stack)
    except StopIteration:
        print invalid.next() 
        print invalid.next() 
def handle(h, op, s):
    import base64
    print "OPCODE", op, "STACK"
    for i, elem in list(enumerate(s))[::-1]:
        print "-",i, '%r'%base64.b64encode(str(elem)) if isinstance(elem, str) and  len(elem) in [64,32] else elem
    print
    op = h[op]()[-1]
    handle(h, op,s)
def script(*opcodes):
   return "".join(map(chr, opcodes))
def toInst(s):
   return map(ord, s)
def putStr(s):
    l = len(s)
    if l <= 75:
        return [l]+map(ord,s)
    if l < (1<<8):
        return [OP_PUSHDATA1, l]+ map(ord, s)
    if l < (1<<16):
        return [OP_PUSHDATA2, l>>8, l & 0x0ff]+ map(ord, s)
    if l < (1<<32):
        return [OP_PUSHDATA4, l>>24, (l>>16) & 0x0ff, (l>>8) & 0x0ff, l & 0x0ff]+ map(ord, s)
    else:
        raise ValueError("Unhandled for now?")
    
if __name__ == "__main__":
    
    inst = script(OP_1, OP_1, OP_EQUALVERIFY)
    stack = collections.deque()
    run(inst)
