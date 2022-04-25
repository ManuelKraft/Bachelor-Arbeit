
def calculate_trend_all(list_x, list_y, middle_value_x, middle_value_y):
    counter = 0
    sum1 = 0
    sum2 = 0
    while counter < len(list_x):
        sum1 += (list_x[counter] - middle_value_x) * (list_y[counter] - middle_value_y)
        sum2 += (list_x[counter] - middle_value_x) * (list_x[counter] - middle_value_x)
        counter += 1

    absolute_increase = sum1 / sum2
    y_axis = middle_value_y - absolute_increase*middle_value_x

    relative_increase = absolute_increase/middle_value_y
    return [absolute_increase, relative_increase, middle_value_y]

def create_recent_list(list_x, list_y):
    new_list_x = []
    for elem in list_x:
        if elem >= 2007:
            new_list_x.append(elem)
    new_list_y = list_y[-len(new_list_x):]
    return [new_list_x, new_list_y]

def enough_recent_data(list_x):
    new_list = []
    for elem in list_x:
        if elem >= 2007:
            new_list.append(elem)
    if len(new_list) >= 10:
        return True
    else:
        return False

def calculate_trend_recent(list_x, list_y, middle_value_y_all):
    new_list_x = []
    for elem in list_x:
        if elem >= 2007:
            new_list_x.append(elem)
    
    sum1 = 0
    for elem in new_list_x:
        sum1 += elem
    middle_value_x = sum1 / len(new_list_x)

    new_list_y = list_y[-len(new_list_x):]
    sum2 = 0
    for elem in new_list_y:
        sum2 += elem
    middle_value_y = sum2 / len(new_list_y)

    counter = 0
    sum3 = 0
    sum4 = 0
    while counter < len(new_list_x):
        sum3 += (new_list_x[counter] - middle_value_x) * (new_list_y[counter] - middle_value_y)
        sum4 += (new_list_x[counter] - middle_value_x) * (new_list_x[counter] - middle_value_x)
        counter += 1

    absolute_increase = sum3 / sum4
    y_axis = middle_value_y - absolute_increase*middle_value_x

    relative_increase = absolute_increase/middle_value_y_all
    return [absolute_increase, relative_increase]

def calculate_middle_value(list_):
    sum1 = 0
    for elem in list_:
        sum1 += elem
    middle_value = sum1 / len(list_)
    return middle_value

def getStation(row):
    return row[:row.find(';')]

def get_x(row):
    x = 0
    counter = 0
    while row[x + counter:].find(';') != -1:
        x += row[x + counter:].find(';') 
        counter += 1
        if counter == 1:
            y = x
        if counter == 2:
            return row[y + counter - 1:x + counter - 1:]

def get_y(row):
    x = 0
    counter = 0
    while row[x + counter:].find(';') != -1:
        x += row[x + counter:].find(';') 
        counter += 1
        if counter == 3:
            return row[x + counter:]
        
list_x = []
list_y = []
f = open("/mnt/c/Uni/Bachelor-Arbeit/prcp_Indices/World/R95p/r95p.csv", 'r')
t = open("/mnt/c/Uni/Bachelor-Arbeit/prcp_Indices/World/R95p/r95p_trend_all.csv", 'w')
t.write("stationid,absolute_increase_per_year, relative_increase_per_year_in_% (absolute_increase / middle_value)\n")
t2 = open("/mnt/c/Uni/Bachelor-Arbeit/prcp_Indices/World/R95p/r95p_trend_recent.csv", 'w')
t2.write("stationid,absolute_increase_per_year,relative_increase_per_year_in_% (absolute_increase / middle_value_from_all_years)\n")
t3 = open("/mnt/c/Uni/Bachelor-Arbeit/prcp_Indices/World/R95p/r95p_trend_comparison.csv", 'w')
t3.write("stationid,absolute_trend_change (trend_recent - trend_all),relative_trend_change_in_% (absolute_trend_change / middle_value)\n")

data_all = [[],[]]
data_recent = [[],[]]
row = f.readline() 
row = f.readline()
while row:
    stationid = getStation(row)
    while stationid == getStation(row):
        list_y.append(float(get_y(row)))
        list_x.append(int(get_x(row)))
        row = f.readline()
    middle_value_x = calculate_middle_value(list_x)
    middle_value_y = calculate_middle_value(list_y)
    if len(list_x) >= 24 and list_y.count(0) != len(list_y):
        data_all[0].append(stationid)
        list_trend = calculate_trend_all(list_x, list_y, middle_value_x, middle_value_y)
        data_all[1].append(list_trend)
        t.write(stationid + ',' + str(round(list_trend[0], 2)) + ',' + str(round(list_trend[1]*100, 2)) + '\n')
    if enough_recent_data(list_x) == True and create_recent_list(list_x, list_y)[1].count(0) != len(create_recent_list(list_x, list_y)[1]):
        data_recent[0].append(stationid)
        list_recent_trend = calculate_trend_recent(list_x, list_y, middle_value_y)
        data_recent[1].append(list_recent_trend)
        t2.write(stationid + ',' + str(round(list_recent_trend[0], 2)) + ',' + str(round(list_recent_trend[1]*100, 2)) + '\n')
    list_y = []
    list_x = []

i = 0
while i < len(data_all[0]):
    j = 0
    while j < len(data_recent[0]):
        if data_recent[0][j] == data_all[0][i]:
            t3.write(data_all[0][i] + ',' + str(round(data_recent[1][j][0] - data_all[1][i][0], 2)) + ',' + str(round((data_recent[1][j][0] - data_all[1][i][0])/data_all[1][i][2]*100, 2)) + '\n')
            break
        j += 1
    i += 1

f = open("/mnt/c/Uni/Bachelor-Arbeit/prcp_Indices/Germany/r95p/r95p_trend_all.csv", 'r')
f2 = open("/mnt/c/Uni/Bachelor-Arbeit/prcp_Indices/Germany/r95p/r95p_trend_recent.csv", 'r')
f3 = open("/mnt/c/Uni/Bachelor-Arbeit/prcp_Indices/Germany/r95p/r95p_trend_comparison.csv", 'r')
row = f.readline()
row2 = f2.readline()
row3 = f3.readline()
while row:
    row = f.readline()
    t.write(row)
    row2 = f2.readline()
    t2.write(row2)
    row3 = f3.readline()
    t3.write(row3)
