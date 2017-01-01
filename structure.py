from random import Random

class Command :
    def execute(self, context) :
        raise NotImplementedError

class If(Command) :
    def __init__(self, cond, true, false) :
        self.cond = cond
        self.true = true
        self.false = false

    def execute(self, context) :
        if self.cond.evaluate(context) :
            return self.true.execute(context)
        else :
            return self.false.execute(context)

    def __str__(self) :
        return ("(if " + str(self.cond) + " " 
                       + str(self.true) + " "
                       + str(self.false) + ")")


class Buy(Command) :
    def __init__(self, amount) :
        self.amount = amount

    def execute(self, context) :
        amount = self.amount.evaluate(context)
        context['state'].buy(context['item'], 
                             amount,
                             context['matrix'])

    def __str__(self) :
        return "(buy " + str(self.amount) + ")" 

class Sell(Command) :
    def __init__(self, amount) :
        self.amount = amount

    def execute(self, context) :
        amount = self.amount.evaluate(context)
        context['state'].sell(context['item'], 
                              amount,
                              context['matrix'])

    def __str__(self) :
        return "(sell " + str(self.amount) + ")" 

class Condition :
    def evaluate(self, context) :
        raise NotImplementedError

class And(Condition) :
    def __init__(self, a, b) :
        self.a = a
        self.b = b

    def evaluate(self, context) :
        return self.a.evaluate(context) and self.b.evaluate(context)

    def __str__(self) :
        return "(" + str(self.a) + " /\ " + str(self.b) + ")"

class Or(Condition) :
    def __init__(self, a, b) :
        self.a = a
        self.b = b

    def evaluate(self, context) :
        return self.a.evaluate(context) or self.b.evaluate(context)

    def __str__(self) :
        return "(" + str(self.a) + " \/ " + str(self.b) + ")"

class Not(Condition) :
    def __init__(self, a) :
        self.a = a

    def evaluate(self, context) :
        return not self.a.evaluate(context)

    def __str__(self) :
        return "~" + str(self.a)

class LessThan(Condition) :
    def __init__(self, a, b) :
        self.a = a
        self.b = b

    def evaluate(self, context) :
        return self.a.evaluate(context) < self.b.evaluate(context)

    def __str__(self) :
        return "(" + str(self.a) + " < " + str(self.b) + ")"

class GreaterThan(Condition) :
    def __init__(self, a, b) :
        self.a = a
        self.b = b

    def evaluate(self, context) :
        return self.a.evaluate(context) > self.b.evaluate(context)

    def __str__(self) :
        return "(" + str(self.a) + " > " + str(self.b) + ")"

class Equal(Condition) :
    def __init__(self, a, b) :
        self.a = a
        self.b = b

    def evaluate(self, context) :
        return self.a.evaluate(context) == self.b.evaluate(context)

    def __str__(self) :
        return "(" + str(self.a) + " == " + str(self.b) + ")"

class Number :
    def evaluate(self, context) :
        raise NotImplementedError

class Plus(Number) :
    def __init__(self, a, b) :
        self.a = a
        self.b = b

    def evaluate(self, context) :
        return self.a.evaluate(context) + self.b.evaluate(context)

    def __str__(self) :
        return "(" + str(self.a) + " + " + str(self.b) + ")"

class Minus(Number) :
    def __init__(self, a, b) :
        self.a = a
        self.b = b

    def evaluate(self, context) :
        return self.a.evaluate(context) - self.b.evaluate(context)

    def __str__(self) :
        return "(" + str(self.a) + " - " + str(self.b) + ")"

class Multiply(Number) :
    def __init__(self, a, b) :
        self.a = a
        self.b = b

    def evaluate(self, context) :
        return self.a.evaluate(context) * self.b.evaluate(context)

    def __str__(self) :
        return "(" + str(self.a) + " * " + str(self.b) + ")"

class Divide(Number) :
    def __init__(self, a, b) :
        self.a = a
        self.b = b

    def evaluate(self, context) :
        return self.a.evaluate(context) / self.b.evaluate(context)

    def __str__(self) :
        return "(" + str(self.a) + " / " + str(self.b) + ")"

class Variable(Number) :
    def __init__(self, a) :
        self.a = a

    def evaluate(self, context) :
        return context[self.a]

    def __str__(self) :
        return str(self.a)

class Constant(Number) :
    def __init__(self, a) :
        self.a = a

    def evaluate(self, context) :
        return self.a

    def __str__(self) :
        return str(self.a)

def generateNumber(r, variables) :
    toprocess = [(0,0)]
    processed = []

    while len(toprocess) > 0 :
        processing,depth = toprocess.pop()
        if processing == 0 :
            k = 4 + (2 * depth)
            x = r.randint(1,k)
            if x < 5 :
                toprocess.append((x,depth))
                toprocess.append((0,depth+1))
                toprocess.append((0,depth+1))
            elif x < depth + 4 :
                processed.append(Variable(variables[r.randint(0,len(variables)-1)]))
            else :
                processed.append(Constant(r.randint(0,500)))
        else :
            b = processed.pop()
            a = processed.pop()
            if processing == 1 :
                processed.append(Plus(a,b)) 
            elif processing == 2 :
                processed.append(Minus(a,b)) 
            elif processing == 3 :
                processed.append(Multiply(a,b)) 
            elif processing == 4 :
                processed.append(Divide(a,b))
    return processed.pop()

def visitNumber(number, 
                fplus, 
                fminus,
                fmult,
                fdivide,
                fvar,
                fconst) :
    toprocess = [number]
    processed = []

    while len(toprocess) > 0 :
        n = toprocess.pop()
        if isinstance(n, Variable) :
            processed.append(fvar(n.a))
        elif isinstance(n, Constant) :
            processed.append(fconst(n.a))
        elif isinstance(n, Plus) :
            toprocess.append(1)
            toprocess.append(n.a)
            toprocess.append(n.b)
        elif isinstance(n, Minus) :
            toprocess.append(2)
            toprocess.append(n.a)
            toprocess.append(n.b)
        elif isinstance(n, Multiply) :
            toprocess.append(3)
            toprocess.append(n.a)
            toprocess.append(n.b)
        elif isinstance(n, Divide) :
            toprocess.append(4)
            toprocess.append(n.a)
            toprocess.append(n.b)
        elif isinstance(n, int) :
            b = processed.pop()
            a = processed.pop()
            if n == 1 :
                processed.append(fplus(a,b))
            elif n == 2 :
                processed.append(fminus(a,b))
            elif n == 3 :
                processed.append(fmult(a,b))
            elif n == 4 :
                processed.append(fdivide(a,b))
    return processed.pop()

def generateCondition(r, variables) :
    toprocess = [0]
    processed = []

    while len(toprocess) > 0 :
        processing = toprocess.pop()
        if processing == 0 :
            x = r.randint(1,6)
            if x < 3 :
                toprocess.append(x)
                toprocess.append(0)
                toprocess.append(0)
            elif x == 3 :
                toprocess.append(x)
                toprocess.append(0)
            else :
                a = generateNumber(r, variables)
                b = generateNumber(r, variables)
                if x == 4 :
                    processed.append(LessThan(a,b))
                elif x == 5 :
                    processed.append(GreaterThan(a,b))
                elif x == 6 :
                    processed.append(Equal(a,b))
        elif processing == 3 :
            a = processed.pop()
            processed.append(Not(a))
        else :
            b = processed.pop()
            a = processed.pop()
            if processing == 1 :
                processed.append(And(a,b))
            elif processing == 2 :
                processed.append(Or(a,b))
    return processed.pop()

def visitCondition(cond, 
                   fand, 
                   forr,
                   fnot,
                   flessthan,
                   fgreaterthan,
                   fequal,
                   fnumber) :
    toprocess = [cond]
    processed = []

    while len(toprocess) > 0 :
        n = toprocess.pop()
        if isinstance(n, LessThan) :
            a = fnumber(n.a)
            b = fnumber(n.b)
            processed.append(flessthan(a, b))
        elif isinstance(n, GreaterThan) :
            a = fnumber(n.a)
            b = fnumber(n.b)
            processed.append(fgreaterthan(a, b))
        elif isinstance(n, Equal) :
            a = fnumber(n.a)
            b = fnumber(n.b)
            processed.append(fequal(a, b))
        elif isinstance(n, And) :
            toprocess.append(1)
            toprocess.append(n.a)
            toprocess.append(n.b)
        elif isinstance(n, Or) :
            toprocess.append(2)
            toprocess.append(n.a)
            toprocess.append(n.b)
        elif isinstance(n, Not) :
            toprocess.append(3)
            toprocess.append(n.a)
        elif isinstance(n, int) :
            if n == 3 :
                a = processed.pop()
                processed.append(fnot(a))
            else :
                b = processed.pop()
                a = processed.pop()
                if n == 1 :
                    processed.append(fand(a,b))
                elif n == 2 :
                    processed.append(forr(a,b))
                else :
                    print "ERROR1"
        else :
            print "ERROR2: " + str(n)
    return processed.pop()

def generateCommand(r, variables) :
    toprocess = [0]
    processed = []

    while len(toprocess) > 0 :
        processing = toprocess.pop()
        if processing == 0 :
            x = r.randint(1,4)
            if x < 3 :
                toprocess.append(x)
                toprocess.append(0)
                toprocess.append(0)
            else :
                a = generateNumber(r, variables)
                if x == 3 :
                    processed.append(Buy(a))
                elif x == 4 :
                    processed.append(Sell(a))
        else :
            f = processed.pop()
            t = processed.pop()
            c = generateCondition(r, variables)
            processed.append(If(c, t,f))
    return processed.pop()

def visitCommand(cmd, 
                 fif, 
                 fbuy,
                 fsell,
                 fnumber,
                 fcond) :
    toprocess = [cmd]
    processed = []

    while len(toprocess) > 0 :
        n = toprocess.pop()
        if isinstance(n, Buy) :
            a = fnumber(n.amount)
            processed.append(fbuy(a))
        elif isinstance(n, Sell) :
            a = fnumber(n.amount)
            processed.append(fsell(a))
        elif isinstance(n, If) :
            toprocess.append(1)
            processed.append(fcond(n.cond))
            toprocess.append(n.true)
            toprocess.append(n.false)
        elif isinstance(n, int) :
            f = processed.pop()
            t = processed.pop()
            c = processed.pop()
            processed.append(fif(c,t,f))
    return processed.pop()

def strNumber(number) :
    return visitNumber(number,
                       lambda a, b: "(" + a + " + " + b + ")",
                       lambda a, b: "(" + a + " - " + b + ")",
                       lambda a, b: "(" + a + " * " + b + ")",
                       lambda a, b: "(" + a + " / " + b + ")",
                       lambda a: a,
                       lambda a: str(a)
                   )

def evalNumber(number, context) :
    return visitNumber(number,
                       lambda a, b: a + b,
                       lambda a, b: a - b,
                       lambda a, b: a * b,
                       lambda a, b: a / b,
                       lambda a: context[a],
                       lambda a: a
                   )

def strCondition(cond) :
    return visitCondition(cond,
                       lambda a, b: "(" + a + " /\ " + b + ")",
                       lambda a, b: "(" + a + " \/ " + b + ")",
                       lambda a: "!" + a,
                       lambda a, b: "(" + a + " < " + b + ")",
                       lambda a, b: "(" + a + " > " + b + ")",
                       lambda a, b: "(" + a + " = " + b + ")",
                       strNumber
                   )

def evalCondition(number, context) :
    return visitCondition(number,
                          lambda a, b: a and b,
                          lambda a, b: a or b,
                          lambda a: not a,
                          lambda a, b: a < b,
                          lambda a, b: a > b,
                          lambda a, b: a == b,
                          lambda n: evalNumber(n, context)
                      )

def strCommand(cmd) :
    return visitCommand(cmd,
                        lambda c, t, f: "if " + c + " then {\n\t" + t + "\n} else {\n\t" + f + "\n}",
                        lambda a: "buy(" + a + ")",
                        lambda a: "sell(" + a + ")",
                        strNumber,
                        strCondition
                    )

def execCommand(cmd, context) :
    return visitCommand(cmd,
                        lambda c, t, f: t if c else f,
                        lambda a: "buy " + str(a),
                        lambda a: "sell " + str(a),
                        lambda n: evalNumber(n,context),
                        lambda c: evalCondition(c,context)
                    )

def subtermsNumber(n) :
    return visitNumber(n,
                          lambda a, b: [Plus(a[0],b[0])] + a + b,
                          lambda a, b: [Minus(a[0],b[0])] + a + b,
                          lambda a, b: [Multiply(a[0],b[0])] + a + b,
                          lambda a, b: [Divide(a[0],b[0])] + a + b,
                          lambda a: [Variable(a)],
                          lambda a: [Constant(a)]
                      )

def subtermsCondition(cond) :
    f = lambda a, b, x: ([x] + a[0] + b[0] , a[1] + b[1])
    g = lambda a, x: ([x] + a[0] , a[1])
    h = lambda a, b, x: ([x] + a[0] + b[0] , a[1] + b[1])

    return visitCondition(cond,
                          lambda a, b: f(a,b,And(a[0][0],b[0][0])),
                          lambda a, b: f(a,b,Or(a[0][0],b[0][0])),
                          lambda a: g(a,Not(a[0][0])),
                          lambda a, b: h(a,b,LessThan(a[1][0],b[1][0])),
                          lambda a, b: h(a,b,GreaterThan(a[1][0],b[1][0])),
                          lambda a, b: h(a,b,Equal(a[1][0],b[1][0])),
                          lambda n: ([] , subtermsNumber(n))
                      )

def subtermsCommand(cmd) :
    h = lambda a, b, c, x: ([x] + a[0] + b[0] + c[0], a[1] + b[1] + c[1], a[2] + b[2] + c[2])
    g = lambda a, x: ([x] + a[0] , a[1] , a[2])

    return visitCommand(cmd,
                        lambda c, t, f: h(c,t,f,If(c[1][0],t[0][0],f[0][0])),
                        lambda a: g(a,Buy(a[2][0])),
                        lambda a: g(a,Sell(a[2][0])),
                        lambda n: ([] , [] , subtermsNumber(n)),
                        lambda c: (lambda x: ([], x[0], x[1]))(subtermsCondition(c))
                       )

def crossNumber(r, n1, n2 = None, numbers = None) :
    if (n2 != None) :
        numbers = subtermsNumber(n2)

    f = lambda x: x if r.random() < 0.9 else numbers[r.randint(0,len(numbers)-1)]

    return visitNumber(n1,
                       lambda a, b: f(Plus(a,b)),
                       lambda a, b: f(Minus(a,b)),
                       lambda a, b: f(Multiply(a,b)),
                       lambda a, b: f(Divide(a,b)),
                       lambda a: f(Variable(a)),
                       lambda a: f(Constant(a))
                   )

def crossCondition(r, c1, c2 = None, conditions = None, numbers = None) :
    if c2 != None :
        conditions,numbers = subtermsCondition(c2)

    if len(conditions) > 0 :
        g = lambda x: x if r.random() < 0.9 else conditions[r.randint(0,len(conditions)-1)]
    else :
        g = lambda x: x

    return visitCondition(c1,
                          lambda a, b: g(And(a,b)),
                          lambda a, b: g(Or(a,b)),
                          lambda a: g(Not(a)),
                          lambda a, b: g(LessThan(a,b)),
                          lambda a, b: g(GreaterThan(a,b)),
                          lambda a, b: g(Equal(a,b)),
                          lambda n: crossNumber(r,n,None,numbers)
                      )

def crossCommand(r, c1, c2) :
    commands,conditions,numbers = subtermsCommand(c2)

    g = lambda x: x if r.random() < 0.9 else commands[r.randint(0,len(commands)-1)]

    return visitCommand(c1,
                        lambda c, t, f: g(If(c,t,f)),
                        lambda a: g(Buy(a)),
                        lambda a: g(Sell(a)),
                        lambda n: crossNumber(r,n,None,numbers),
                        lambda c: crossCondition(r,c,None,conditions,numbers)
                      )


if __name__ == "__main__" :
    r = Random()
    ctx = { 'var1' : 33,
            'var2' : 9 }
    n1 = generateCommand(r, ctx.keys())
    n2 = generateCommand(r, ctx.keys())
    
    print strCommand(n1)
    print
    print strCommand(n2)
    print
    print strCommand(crossCommand(r,n1,n2))
