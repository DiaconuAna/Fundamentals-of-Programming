#
# Implement the program to solve the problem statement from the second set here
# Exercise 6: determine a proper calendar date
#

def input_year ():
    return int(input("Please input the year: "))


def input_day ():
    return int(input("Please input the day number: "))

def check_day (day, year):
    if (year % 4) == 0:
        while (day > 366 or day <= 0):
            day = int(input("Please input a day number smaller than 366 and bigger than 0: "))
    else:
        while (day > 365 or day <= 0):
            day = int(input("Please input a day number smaller than 365 and bigger than 0: "))
    return day

def check_leap_year (year):
    if year%4==0:
        return 1
    else: return 0

if __name__ == '__main__':

  months={1:'January',2:'February',3:'March',4:'April',5:'May',6:'June',7:'July',8:'August',9:'September',10:'October',11:'November',12:'December'}
  dayspermonth=[31,28,31,30,31,30,31,31,30,31,30,31]

  year = input_year()
  daynumber = input_day()
  daynumber = check_day(daynumber, year)

  #if the year's a leap year, February has 29 days
  dayspermonth[1]+=check_leap_year(year)

  daysofxmonths=0
  monthnumber=0

  #we look for the month number by summing the day numbers of the x months and seeing where the daynumber fits
  while (daynumber>daysofxmonths):
      daysofxmonths=daysofxmonths+dayspermonth[monthnumber]
      monthnumber+=1

  #daysofxmonths consists of the number of days of the months before the current month in which our daynumber exists
  daysofxmonths= daysofxmonths-dayspermonth[monthnumber-1]
  daynumber = daynumber - daysofxmonths

  print("The calendar date is: ", end=" ")
  print(year, end=" ")
  print(months[monthnumber], end=" ")
  print(daynumber)