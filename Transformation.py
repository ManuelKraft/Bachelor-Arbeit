from math import radians, cos, sin, sqrt, atan2
import time

def Distance(origin, destination):
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371  # km

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = (sin(dlat / 2) * sin(dlat / 2) +
         cos(radians(lat1)) * cos(radians(lat2)) *
         sin(dlon / 2) * sin(dlon / 2))
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    d = radius * c
    return d

def Create_Country_String():
    t = open("countrycodes.txt", 'r')
    CountryString=[]
    while True:
        a=t.readline()
        if not a:
            break
        CountryString.append(a)
    t.close()
    return CountryString

def Create_Attribute_Lists_From_Twin_Stations():  
    StationID = []; Latitude = []; Longitude = []; Elevation = []; Name = []; Country = []; RecentYear = [];  Years = []
    AttributeList = [StationID, Latitude, Longitude, Elevation, Name, Country, RecentYear, Years]
    u = open("double_keys_and_dates.csv", 'r')
    while True:
        a = u.readline()
        if not a:
            break
        x = 0; counter = 0
        l = 0
        while a[x+counter:].find(',') != -1:
            x += a[x+counter:].find(',') 
            counter += 1
            if counter == 1:
                StationID.append(str(a[1:x]))
                y = x
            elif counter == 2:
                Latitude.append(float(a[y + counter + 1:x + counter - 3]))   
                y = x  
            elif counter == 3:
                Longitude.append(float(a[y + counter + 1:x + counter - 3])) 
                y = x
            elif counter == 4:
                if a[y + counter + 1:x + counter - 3] != '':
                    Elevation.append(float(a[y + counter + 1:x + counter - 3]))
                    y = x
                else:
                    Elevation.append('-')
                    y = x
            elif counter == 5:
                if a[y + counter + 1:x + counter - 3] != '':
                    Name.append(a[y + counter + 1:x + counter - 3])
                    y = x
                else:
                    Name.append('-')
                    y = x
            elif counter == 6:
                if a[y + counter + 1:x + counter - 3] != '':
                    Country.append(a[y + counter + 1:x + counter - 3])
                else:
                    Country.append('-')
            elif counter == 7:
                y = x
            elif counter == 8:
                RecentYear.append(int(a[y + counter + 1:x + counter - 3]))
                y = x
            elif counter ==9:
                Years.append(int(a[y + counter + 1:x + counter - 3]))
            else:
                break
    u.close()
    return AttributeList

def Insert_Country_Column(Row):
    x = 0
    counter = 0
    while True:
        if Row[x+counter:].find(',') != -1:
            x = Row[x+counter:].find(',') + x
            counter += 1
        if counter == 5:
            z = x
        if counter == 6:
            y = x
        if counter == 7:
            break
    newString = Row[x + counter - 4:x + counter]
    newString2 = Row[z + counter - 3:y + counter - 1]
    if newString2.find(',",') != -1:
        Row = Row[:z + counter - 3] + ',"-","' + Row[y + counter:]
        return Row
    if newString2.find('",') != -1 or newString2.find(',,') != -1:
        Row = Row[:y + counter - 2] + ',"-"' + Row[y + counter - 2:]
    else:
        Row = Row[:y + counter - 2]+'","' + newString + Row[x + counter:]
    return Row

def Delete_Columns(Row):
    i = 0
    while i < 11:
        x = 0
        counter = 0
        while True:
            if Row[x + counter:].find(',') != -1:
                x += Row[x + counter:].find(',')
                counter += 1
            if counter == 8 + i:
                y = x
            if counter == 9 + i:
                break
        Row = Row[:y + counter] + Row[x + counter + 1:]
        i += 1
        if i == 6:
            i = 8
    return Row

def Convert_Units(Row):
    i = 0
    while i < 12:
        x = 0
        counter = 0
        while True:
            if Row[x + counter:].find(',') != -1:
                x = Row[x + counter:].find(',') + x
                counter += 1
            if counter == 7 + i:
                y = x
            if counter == 8 + i:
                a = float(Row[y + counter:x + counter - 2])
                if i >= 2 and i <= 3:
                    break
                elif i == 4:
                    if a != 999.9:
                        b = a * 1.609344
                        c = round(b, 3)
                    else:
                        c = "-"
                    Row = Row[:y + counter] + str(c) + Row[x + counter - 2:]
                    break
                elif i >= 5 and i <= 7:
                    if a != 999.9:
                        b = a * 1.852
                        c = round(b, 2)
                    else:
                        c = "-"
                    Row = Row[:y + counter] + str(c) + Row[x + counter - 2:]
                    break
                elif i == 10 or i == 11:
                    if a != 99.99 and a != 999.9:
                        b = a * 25.4
                        c = round(b, 2)
                    else:
                        c = "-"
                    Row = Row[:y + counter] + str(c) + Row[x + counter - 2:]
                    break
                else:
                    if a != 9999.9:
                        b = (a - 32) * (5 / 9)
                        c = round(b, 2)
                    else:
                        c = "-"
                    Row = Row[:y + counter] + str(c) + Row[x + counter - 2:]
                    break
        i += 1
    return Row

def Convert_Code_To_Country(Row, CountryString):
    x = 0
    counter = 0
    while True:
        if Row[x+counter:].find(',') != -1:
            x += Row[x+counter:].find(',')
            counter += 1
        if counter == 6:
            y = x
        if counter == 7:
            break
    newString = Row[y+counter:x+counter-2]
    for elem in CountryString:
        if elem[:2] == newString:
            x2 = 2
            while True:
                if elem[x2:x2 + 1].find(' ') != -1:
                    x2 += 1
                else:
                    break
            x3 = elem[x2:].find('  ')
            newString = elem[x2:x3 + x2]
            break
    return Row[:y+counter] + newString + Row[x+counter-2:]

def Edit_Chars(Row):
    x = 0
    counter = 0
    while True:
        if Row[x+counter:].find(',') != -1:
            x += Row[x+counter:].find(',')
            counter += 1
        if counter == 5:
            y = x
        if counter == 7:
            break
    Row = Row[:y + 5].replace(' ', '') + Row[y + 5:x + 7] + Row[x + 7:].replace(' ', '')
    Row=Row.replace('"', '')
    Row=Row.replace(',9999.9,', ',-,')
    Row=Row.replace(',999.9,', ',-,')
    Row=Row.replace(',99.99,', ',-,' )
    Row=Row.replace(',-999,', ',-,')
    Row=Row.replace(',*,', ',-,')
    Row=Row.replace(',,', ',-,')
    Row=Row.replace(',,', ',-,')
    Row=Row.replace('--', '-')
    return Row

def Edit_Wrong_Data(Row):
    x = 0
    counter = 0
    while True:
        if Row[x+counter:].find(',') != -1:
            x += Row[x+counter:].find(',')
            counter += 1
        if counter == 10:
            y = x
        if counter == 11:
            break
    if Row[y + 10:x + 10] != '-' and float(Row[y + 10:x + 10]) <= 100:
        Row = Row[:y + 10] + '1' + Row[y + 10:]
    return Row

def Delete_Useless_Data(Row):
    list1 = []
    i = 0
    while i <= 1:
        x = 0
        counter = 0
        while True:
            if Row[x + counter:].find(',') != -1:
                x = Row[x + counter:].find(',') + x
                counter += 1
            if counter == 2 + i:
                y = x
            if counter == 3 + i:
                newString = Row[y+counter-1:x+counter-1]
                if newString == '0.0':
                    list1.append(newString)
                elif newString == '-':
                    return True
                i += 1
                break
    if len(list1) == 2:
        return True
    else:
        return False

def Update_String(Row, List2, k):
    j = 0
    while j <= 4:
        x = 0
        y = 0
        counter = 0
        while Row[x + counter:].find(',') != -1:
            x += Row[x + counter:].find(',')
            counter += 1
            if counter == j + 2:
                y = x
            elif counter == j + 3:
                Row = Row[:y + counter - 1] + str(List2[k + 2*j]) + Row[x + counter - 1:]
                break
        j += 1
    return Row

def Get_Station_Attributes(Row):
    x2 = 0
    counter  = 0
    while Row[x2 + counter:].find(',') != -1:
        x2 += Row[x2 + counter:].find(',') 
        counter += 1
        if counter == 1:
            z = x2 + counter - 1
        elif counter == 2:
            y = x2 + counter - 1
        elif counter == 7:
            return Row[:z] + Row[y:x2 + counter]

def Edit_Double_IDs(Row, AttributeList):
    List2 = []
    x = Row.find(',')
    i = 1  
    while i < len(AttributeList[0]):    # gehe Attributliste der doppelten ID's durch
        if AttributeList[0][i - 1].find(Row[:x]) != -1:  # schaue ob sich ID des Tupels in Attributliste befindet
            j = 1
            while j <= 7:
                List2.append(AttributeList[j][i - 1])   
                List2.append(AttributeList[j][i]) 
                j += 1          
            break
        i += 1
    if len(List2) >= 14: 
        with open('Catched_Doubles.txt', 'a+') as f:
                exist = False
                f.seek(0)
                Doubles = f.readlines()
                Row_Station_Attributes = Get_Station_Attributes(Row)
                for elem in Doubles:
                    if elem.find(Row_Station_Attributes) != -1:
                        exist = True
                        break
                if exist == False: 
                    f.seek(0)
                    if len(f.read(20)) > 0:
                        f.write('\n')
                    f.write(Row_Station_Attributes)
        if  Distance((List2[0], List2[2]), (List2[1], List2[3])) > 5  or List2[4] != '-' and List2[5] != '-' and abs(List2[4] - List2[5]) > 50:
            with open('Doubles_Changed_Position.txt', 'a+') as f:
                f.seek(0)
                Doubles = f.readlines()
                Row_Station_Attributes = Get_Station_Attributes(Row)
                for elem in Doubles:
                    if elem.find(Row[:x]) != -1:
                        if elem.find(Row_Station_Attributes) != -1:
                            return Row
                        else:
                            return 'B' + Row
                f.seek(0) 
                if len(f.read(20)) > 0:
                    f.write('\n')
                f.write(Row_Station_Attributes)
                return Row
        else:
            if List2[10] > List2[11]:
                return Update_String(Row, List2, k = 0)
            elif List2[10] == List2[11]:
                if List2[12] >= List2[13]:
                    return Update_String(Row, List2, k = 0)
                else:
                    return Update_String(Row, List2, k = 1)
            else:
                return Update_String(Row, List2, k = 1)
    else:
        return Row

def main():
    AttributeList = Create_Attribute_Lists_From_Twin_Stations()
    CountryString = Create_Country_String()
    year = int(input('Start Year: '))
    end_year = int(input('End Year: '))
    counter = 0
    while year <= end_year:
        f = open('Data/' + str(year) + '.txt', 'r')
        x = f.tell()
        file_length = len(f.readlines())
        f.seek(x)
        filename = str(year) + '.txt'
        g=open('Data_Edited/' + filename, 'w')
        counter2 = 0
        start = time.time()
        while True:
            Row = f.readline()
            if not Row:
                break
            Row2 = Insert_Country_Column(Row)
            Row3 = Delete_Columns(Row2)
            Row4 = Convert_Units(Row3)
            Row5 = Convert_Code_To_Country(Row4, CountryString)
            Row6 = Edit_Chars(Row5)
            Row7 = Edit_Wrong_Data(Row6)
            Row8 = Edit_Double_IDs(Row7, AttributeList)
            if Delete_Useless_Data(Row8) == False:
                g.write(Row8)
            counter += 1
            counter2 += 1
            if counter2 % 1000 == 0:
                end = time.time()
                print(str(round((counter2/file_length) * 100, 1)) + ' % ' + 'of ' + str(year) + '  (' + str(int((end - start) * 100)) + ' sec/100k)')
                start = time.time()
        year += 1
        g.close()
        f.close()

if __name__ == '__main__':
  main()





