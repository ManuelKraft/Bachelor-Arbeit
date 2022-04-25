import re
import time
from urllib import request


def URLtoString(URL):
    a=request.urlopen(URL)
    b=a.read()
    c=b.decode("UTF-8")
    return c

def SMString_To_Exact_URLs(SubMainString, SubMainURL):
    StringList=[]
    x=0
    counter=0
    while True:
        if re.search('............csv', SubMainString[x:]):
            SmallString=re.search('............csv', SubMainString[x:]).group()
            if counter>=1 and SubMainURL+'/'+SmallString==StringList[counter-1]:
                x=x+re.search('............csv', SubMainString[x:]).end()
                continue
            else:
                StringList.append(SubMainURL+'/'+SmallString)
                counter+=1
                x=x+re.search('............csv', SubMainString[x:]).end()
        else:
            break
    return StringList

def Exact_URLs_To_String(Exact_URLs, year, f):
    counter=0
    for x in Exact_URLs:
        start = time.time()
        f.write(URLtoString(x)[309:])
        end = time.time()
        counter+=1
        if str(round(counter/len(Exact_URLs)*100, 2)) != str(round((counter - 1)/len(Exact_URLs)*100, 2)):
            print(str(round(counter/len(Exact_URLs)*100, 2)) + ' % ' + 'of '+ str(year) + ' (' + str(round(end - start, 1)) + ' sec/request)')

def main():
    MainURL = "https://www.ncei.noaa.gov/data/global-summary-of-the-day/access"
    year = int(input('Start Year: '))
    end_year = int(input('End Year: '))
    while year <= end_year:
        SubMainURL = MainURL+'/'+str(year)
        SubMainString = URLtoString(SubMainURL)
        Exact_URLs=SMString_To_Exact_URLs(SubMainString, SubMainURL)
        f=open('Data/' + str(year)+'.txt', 'w')
        Exact_URLs_To_String(Exact_URLs, year, f)
        f.close()
        year += 1

if __name__ == '__main__':
  main()
        




    
