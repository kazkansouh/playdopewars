
class State :
    def __init__(self) :
        self.money = 50
        self.bagmax = 20
        self.bag = {}
        self.daymax = 30
        self.day = 0
        

    def capacity(self) :
        acc = 0
        for item in self.bag :
            acc += self.bag[item]['amount']
        return self.bagmax - acc
    

    def buy(self, item, count, matrix) :
        amount = min(count, self.capacity())
        cost = amount * matrix[item]
        if cost <= self.money and self.day < self.daymax and amount > 0 :
            self.money -= cost
            if self.bag.has_key(item) :
                self.bag[item]['value'] = (self.bag[item]['value'] * self.bag[item]['amount'] + matrix[item] * amount) / (self.bag[item]['amount'] + float(amount))
                self.bag[item]['amount'] += amount
            else :
                self.bag[item] = {}
                self.bag[item]['amount'] = amount
                self.bag[item]['value'] = float(matrix[item]) 
            print "Purchased " + str(amount) + " of item " + str(item)
            return True
        return False

    def sell(self, item, count, matrix) :
        if self.bag.has_key(item) and self.day < self.daymax and count > 0:
            amount = min(count, self.bag[item]['amount'])
            self.bag[item]['amount'] -= amount
            self.money += amount * matrix[item]
            print "Sold " + str(amount) + " of item " + str(item)
            return True
        return False

    def endday(self) :
        self.day += 1

    def finished(self) :
        return self.day >= self.daymax

    def showinventory(self) :
        print "money: " + str(self.money)
        print "inventory:"
        for item in self.bag :
            if self.bag[item]['amount'] > 0 :
                print str(item) + "*" + str(self.bag[item]['amount']) + " @" + str(self.bag[item]['value'])
