'''Extra Programm um Basisdaten zur Berechnung von Rx5day zu erhalten, weil mit SQL zu umfangreich.
Berechnet für jede Station die Summe aller 5-Tages-Zeiträume. Ergebnisse in Datei "basisdaten_rx5day.txt" gespeichert


import datetime
from datetime import date


def getStation(row):
    return row[:row.find(',')]

def getDate(row):  
    x = 0
    counter = 0
    while row[x + counter:].find(',') != -1:
        x += row[x + counter:].find(',') 
        counter += 1
        if counter == 1:
            y = x + counter - 1
        elif counter == 2:
            return row[y + 1:x + counter - 1]

def getRain(row):
    x = 0
    counter = 0
    while row[x + counter:].find(',') != -1:
        x += row[x + counter:].find(',') 
        counter += 1
        if counter == 17:
            y = x + counter - 1
        elif counter == 18:
            return row[y + 1:x + counter - 1]


f = open("/mnt/c/Uni/Bachelor-Arbeit/prcp_Indices/World/Rx5day/Rx5day.txt", 'w')
f2 = open("/mnt/c/Uni/Bachelor-Arbeit/Extracted_Stations/filter1/filter1_world.csv", 'r')

station_list = []
while True:
    row = f2.readline()
    if not row:
        break
    station_list.append(getStation(row)[1:-1])

station_id = " "
max_sum = 0.0
max_date = date.today()
counter_nodata = 0
year = 2004
while year <= 2021:
    a = 0
    counter = 0
    counter3 = 0
    nodata_list = []
    t = open("Data_Edited/" + str(year) + ".txt", 'r')  
    length = len(t.readlines())
    t.seek(0)
    print(length)
    rounds = 0
    while counter < length:
        date_list= []
        rain_list = []
        sum_list = []
        x = 0
        rounds += 1
        '''if rounds % 100 == 0:
            print(year, rounds, counter)'''
        while True:
            '''if counter2 < counter:
                counter2 += 1
                continue'''
            row = t.readline()
            if not row:
                break
            if x == 0:
                t.seek(a)
                station_id = getStation(row)
            if getStation(row) != station_id or counter == length:
                a = t.tell()
                break
            mydate = date.fromisoformat(getDate(row))
            date_list.append(mydate)
            myrain = getRain(row)
            rain_list.append(myrain)
            if x >= 4 and (date_list[x] - date_list[x-4]).days == 4 and rain_list[x] != '-' and rain_list[x-1] != '-'and rain_list[x-2] != '-' and rain_list[x-3] != '-' and rain_list[x-4] != '-':
                rain_sum = float(rain_list[x]) + float(rain_list[x-1]) + float(rain_list[x-2]) + float(rain_list[x-3]) + float(rain_list[x-4])
                sum_list.append(rain_sum)
            else:
                sum_list.append(0)
                
            x += 1
            counter += 1
        if len(sum_list) == 0:
            counter += 1
            counter_nodata += 1
            print("No Data!", counter_nodata)
            continue
            #nodata_list.append(station_id)
        else:
            max_sum = max(sum_list)
            h = 0
            for elem in sum_list:
                if elem == max(sum_list):
                    max_date = date_list[h]
                    break
                h += 1
            for elem in station_list:
                    if elem == station_id:
                        if counter3 % 10 == 0:
                            print(str(year) + ": " + str(counter3))
                        counter3 += 1
                        f.write(station_id + "," + str(year) + "," + str(round(max_sum, 1)) + "," + str(max_date - datetime.timedelta(days = 4)) + "," + str(max_date) + "\n")
                        break 
            counter += 1

    year += 1    
        