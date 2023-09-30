class Number():
    def __init__(self):
        self.listofnumbers=[]
    def inputnumbers(self):
        while (inputnumber:=input("gimme da numbah ")).isnumeric():
            self.listofnumbers.append(int(inputnumber))
    def getrange(self):
        self.listofnumbers.sort()
        numbersrange=self.listofnumbers[-1]-self.listofnumbers[0]

        return numbersrange
n=Number()
n.inputnumbers()
print(n.getrange())