import math
import sys

def error(err):
    print(err)
    sys.exit()

def isDigit(x):
    try:
        float(x)
        return True
    except ValueError:
        return False

def findOption(option, x):
    i = 0
    while (i < len(option)):
        if (option[i] == x):
            return True
        i += 1
    return False

def digitLen(s, i):
    while (i < len(s) and (isDigit(s[i]) or s[i] == '.')):
        i += 1
    return i

def fixData(data):
    i = 0
    while (i < len(data)):
        while (i < len(data) and not isDigit(data[i]) and data[i] != 'X'):
            i += 1
        if (i < len(data) and data[i] == 'X'):
            if (data[i - 2] != '*'):
                data = data[:i] + '1 * ' + data[i:]
                i += 4
            if (data[i + 1] != '^'):
                data = data[:i] + data[i] +  '^1' + data[i + 1:]
                i += 3
        i += 1
    return data

def cleanContent(equation):
    e = equation.replace(" ", "")
    i = 0
    while (i < len(e)):
        if(isDigit(e[i])):
            i = digitLen(e, i)
            e = e[:i] + ' ' + e[i:]
        elif (e[i] == '+' or e[i] == '*' or e[i] == '-' or e[i] == '='):
            i += 1
            e = e[:i] + ' ' + e[i:]
        elif (e[i] == 'X' and i + 1 < len(e) and e[i + 1] != '^'):
            i += 1
            e = e[:i] + ' ' + e[i:]
        i += 1
    return (e)

def toDigit(x):
	try:
		return int(x)
	except ValueError:
		return float(x)

def expoCheck(tab, x):
    i = 0
    while (i < len(tab)):
        if (tab[i] == x):
            return i
        i += 1
    return -1

def findDeg(reduced, x):
    i = 0
    while(i < len(reduced[1])):
        if (reduced[1][i] == x):
            return reduced[0][i]
        i += 1
    return 0

def parse(data):
    data = data.split(' ')
    new = []
    number = []
    expo = []
    i = 0
    while (i < len(data)):
        if (isDigit(data[i])):
            sign = 1
            if (i > 0 and data[i - 1] == '-'):
                sign = -1
            if (i + 2 < len(data)):
                n =expoCheck(expo, toDigit(data[i + 2][2:]))
                if (n == -1):
                    number.append(toDigit(data[i]) * sign)
                    expo.append(toDigit(data[i + 2][2:]))
                else:
                    number[n] += toDigit(data[i]) * sign
        i += 1
        # return(reduced)
    new.append(number)
    new.append(expo)
    i = 0
    while (i < len(new)):
        j = 0
        while (j < len(new[1])):
            new[i][j] = round(new[i][j], 6)
            j += 1
        i += 1
    return new

def reduceForm(before, after):
    tab = []
    number = []
    expo = []
    i = 0
    while (i < len(before[1])):
        n = expoCheck(after[1], before[1][i])
        if (n == -1):
            number.append(before[0][i])
        else:
            number.append(before[0][i] - after[0][n])
            del after[0][n]
            del after[1][n]
        expo.append(before[1][i])
        i += 1
    i = 0
    while (i < len(after[1])):
        number.append(-after[0][i])
        expo.append(after[1][i])
        i += 1
    tab.append(number)
    tab.append(expo)
    return (tab)

def sort(reduced):
    i = 0
    while (i < len(reduced[0])):
        j = i
        while (j < len(reduced[0])):
            if (reduced[1][i] > reduced[1][j]):
                tmp = reduced[0][i]
                reduced[0][i] = reduced[0][j]
                reduced[0][j] = tmp
                tmp = reduced[1][i]
                reduced[1][i] = reduced[1][j]
                reduced[1][j] = tmp
            j += 1
        i += 1
    return reduced

def removeEmpty(reduced):
    i = len(reduced[0]) - 1
    while (i > 0):
        if (reduced[0][i] == 0):
            del reduced[0][i]
            del reduced[1][i]
        else:
            return reduced
        i -= 1
    return reduced

def displayTwo(a, b, delta, sign):
	new = ''
	new += '-' + str(abs(b)) + ' ' + sign + ' i('
	new += str(abs(delta)) + ')'
	new += ' / 2 * ' + str(abs(a))
	print (new)

def solveZero(reduced):
    a = findDeg(reduced, 0)
    if (a == 0 and findOption(option, 'c') == True):
        print('Every number is a solution')
    elif (a == 0):
        print('Every real number is a solution')
    else:
        print('No solution')

def solveOne(reduced):
    a = findDeg(reduced, 1)
    b = findDeg(reduced, 0)
    print('the solution is: ')
    result = float(b * -1) / a
    print(result)

def solveTwo(reduced, option):
    a = findDeg(reduced, 2)
    b = findDeg(reduced, 1)
    c = findDeg(reduced, 0)
    delta = (b ** 2) - (4 * a * c)
    if (findOption(option, 'd') == True):
        print('Delta: ' + str(delta))
    if (delta > 0):
        print('Discriminant is strictly positive, the two solutions are:')
        print(round(((-b - math.sqrt(delta)) / (2 * a)), 6))
        print(round(((-b + math.sqrt(delta)) / (2 * a)), 6))
    elif (delta == 0):
        print('Discriminant is nul, the solution is:')
        print(round((float(-b) / (2 * a)), 6))
    elif (delta < 0 and findOption(option, 'c') == True):
        print ("Discriminant is stricly negatve, there are two solution in C:")
        displayTwo(a, b, delta, '-')
        displayTwo(a, b, delta, '+')
    else:
        print('Discriminant is strictly negative, no solution in R')

def resolveEquation(reduced, option):
    reducedEquation = 'Reduced form: '
    k = 0
    while (k in reduced[1]):
        if (reduced[0][k] >= 0 and k != 0):
            reducedEquation += '+ '
        elif(reduced[0][k] < 0):
            reducedEquation += '-'
            if (k != 0):
                reducedEquation += ' '
        reducedEquation += str(abs(reduced[0][k])) + ' * X^' + str(reduced[1][k]) + ' '
        k += 1
    reducedEquation += '= 0'
    print(reducedEquation)
    deg = len(reduced[1]) - 1
    print('Polynomial degree: {}'.format(reduced[1][deg]))
    if (deg == 0):
        solveZero(reduced, option)
    elif (deg == 1):
        solveOne(reduced)
    elif (deg == 2):
        solveTwo(reduced, option)
    elif (deg > 2):
        print('The polynomial degree is stricly greater than 2, I can\'t solve.')
    else:
        print('I can\'t solve.')

def check(equation):
    i = 1
    equal = 0
    while (i < len(equation)):
        if (equation[i] == '='):
            equal += 1
            i += 1
        elif (isDigit(equation[i]) or equation[i] == '+' or equation[i] == '-' or equation[i] == ' '
        or equation[i] == '.' or equation[i] == '^' or equation[i] == '*' or equation[i] == 'X'):
            i += 1
        else:
            return False
    if (equal != 1):
        return False
    else:
        return True

def optionCheck(option):
    if (len(option) > 2 or option[0] != '-'):
        error('Bad options')
    i = 1
    while (i < len(option)):
        if (option[i] == "c" or option[i] == "d"):
            i += 1
        else:
            error('Bad options')

data = None
if (len(sys.argv) == 2):
        data = sys.argv[1]
elif (len(sys.argv) == 3):
    option = list(sys.argv[1])
    optionCheck(option)
    data = sys.argv[2]
else:
    error('python main.py [-dc] [equation]')
if (check(data) == False):
    error('Unvalid equation')
cleanedData  = cleanContent(data)
before, after = cleanedData.split(" = ")
before = fixData(before)
after = fixData(after)
before = parse(before)
after = parse(after)
reduced = reduceForm(before, after)
reduced = removeEmpty(reduced)
reduced = sort(reduced)
reduced = resolveEquation(reduced, option)
# print(result)
# if (len(result) == 2):
#     print('Discriminantt is strictly positive, the two solutions are:\n {} \n {}'.format(result[0], result[1]))
# elif (result.length == 1):
#     print('The solution is: {}'.forrmat(result[0]))
# else:
#     print('something went wrong')
