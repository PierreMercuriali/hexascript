import matplotlib.pyplot as plt
import random 
import math

#source: http://www.mieliestronk.com/wordlist.html
with open("corncob_lowercase.txt", "r") as f:
    data = f.read()
words = [e for e in data.split("\n") if not e==""]

LEX = words
for x in ";.:,?!\'\"0123456789s()":
    LEX.append(x)
testSentence = "The parrot's beak that she cleans, even though it is neat." #Pascal's

def wordToIndex(w, lexicon):
    w0 = w.lower()
    if w0 in lexicon:
        return lexicon.index(w0)
    else:
        return 0 #TODO: something clever with word distances

def splitClean(s):
    res = ""
    for c in s:
        if c in ';.:,?!\'\"()':
            res+=" "+c+" "
        else:
            res+=c
    return [x for x in res.split(" ") if not x==""]

def englishToCodeNumber(s, lexicon):
    #sentence in English to corresponding code
    return [wordToIndex(w, lexicon) for w in splitClean(s)]

def numberToBase(n, b):
    if n == 0:
        return [0]
    digits = []
    while n:
        digits.append(int(n % b))
        n //= b
    return digits[::-1] 
    
def leadingZeros(s, maxN):
    if len(s)==maxN:
        return s
    else:
        res = s
        res.reverse()
        for i in range(maxN-len(s)):
            res.append(0)
        res.reverse()
        return res
        
def codeNumberToCodeSymbol(codeNumber):
    return numberToBase(codeNumber, 5)

def englishToCodeSymbol(s, lexicon):
    #sentence in English to corresponding code symbols 
    return [leadingZeros(codeNumberToCodeSymbol(c), 7) for c in englishToCodeNumber(s, lexicon)]

LW = 1.5
LS = '-'
CL = 'black'
AL = 1
MA = 'o'
RAC = math.sqrt(2)/2
colors = [
            (  1,  0,  0),
            (  1,  0,  1),
            (  1,  1,  0),
            (  1,  .5,  0),
            (  1,  0,  .5)
        ]
def displaySymbol(codeSymbol, x, y):
    coordinates = [
                    (x, y),
                    (x+1, y),
                    (x+.5, y+RAC),
                    (x-.5, y+RAC),
                    (x-1, y),
                    (x-.5, y-RAC),
                    (x+.5, y-RAC)
                    ]
    X, Y = zip(*coordinates)
    plt.plot(X, Y, linewidth=LW, linestyle=LS, color=CL, alpha=.4, marker=MA)
    for i in range(len(codeSymbol)):
        plt.plot(*coordinates[i], linewidth=LW, linestyle=LS, color=colors[codeSymbol[i]], alpha=AL, marker=MA)
    

def displaySentence(s, x, y, lexicon, linelength):
    codes = englishToCodeSymbol(testSentence, lexicon)
    x0 = x
    y0 = y
    e = 3
    f = 2
    counter = 0
    visited = [(x0, y0)]
    for code in codes:
        displaySymbol(code, x0, y0)
        x0+= e
        counter+=1
        if counter == linelength:
            y0-= f
            x0 = x
            counter = 0
        visited.append((x0, y0))
    X, Y = zip(*visited)
    plt.plot(X, Y, linewidth=LW, linestyle='--', color=CL, alpha=.2, marker=MA)
        
displaySentence(testSentence, 0, 0, LEX, 5)

plt.title(".\n".join(testSentence.split(".")))
plt.savefig("".join([str(random.choice("azertyuiopqsdfghjklmwxcvbn")) for i in range(32)])+".png")
plt.show()    
