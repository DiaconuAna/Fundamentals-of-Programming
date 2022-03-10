#
# Implement the program to solve the problem statement from the first set here
#Problem no. 2 Goldbach hypothesis
#

#checking whether a number >2 is prime
def prime_number_check (number):

    if (number%2)==0: return 0
    i=3

  #else for index in range (3, number//2+1, 2):
  #      if (number%index)==0: return False
  # return True

    while (i*i<=number):
       if (number%i==0): return 0
       i+=2
    return 1

def determine_p2 (n,p1):
    '''
    returns the number p2 in the Goldbach hypothesis in case p1 exists (the n number is even)
    '''
    return n-p1

def check_Goldbach_for_even_n (n):
    p1 = 3
    ok = 0
    if n<=4:
        return 0
    else:
        while (ok == 0):
            p2 = n - p1
            if (prime_number_check(p1) and prime_number_check(p2)):
                ok = 1
            else:
                p1 += 2

        return p1



def check_Goldbach_for_odd_n (n):
    '''
    The Goldbach hypothesis does not apply for very single odd number. The only case in which
    it is possible is when the n-2 number is prime and that is because an odd number must be
    the sum of an even and odd number and the only prime even number is 2
    '''
    if (n % 2) == 1:
        p1 = 2
        p2 = n - p1
        if (prime_number_check(p2)) == 1:
            return 1
        else:
            return 0


def Goldbach (n):
    """
    Checks whether the Goldbach hypothesis can be applied for a given n number and
    shows an appropriate message according to n's value
    """
    if n%2==1:
        if check_Goldbach_for_odd_n(n):
            print(2, end=" ")
            print(n-2)
        else: print("The Goldbach hypothesis does not apply for this odd number")
    else:
        p1=check_Goldbach_for_even_n(n)
        if (p1==0): print("The Goldbach hypothesis does not apply for this even number")
        else:
            p2=determine_p2(n,p1)
            print(p1, end=" ")
            print(p2)


if __name__ == '__main__':

 n= int(input("Enter value of n: "))
 Goldbach(n)

