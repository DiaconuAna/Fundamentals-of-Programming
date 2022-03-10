#
# Implement the program to solve the problem statement from the third set here
# Exercise 15: largest perfect number smaller than a given natural number n
#
def perfectnumbercheck (number):

    s=0
    for div in range (1,int(number/2+1)):
        if (n%div)==0:
            s=s+div
    if (s==n): return 1
    else: return 0



if __name__ == '__main__':

 n=int(input("Enter your number here: "))
 copyofn=n

 while (n<0):
     n= int(input("Please enter a natural number:"))

 n=n-1

 '''
 the first perfect natural number is 6 so all natural numbers smaller than 6 are clearly not perfect numbers
 '''
 while n>=6 :
    if (perfectnumbercheck(n)):
        print("The biggest perfect number smaller than ",copyofn ,"is " ,n)
        break
    else: n-=1

 if n<6:
     print("A natural perfect number smaller than ", copyofn," does not exist")