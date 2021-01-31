from datetime import date

areas =["aphazeti", "samegrelo","svaneti","guria","achara","imereti","racha-letkchumi", "samtske-javaxeti",
        "shida qartli","qvemo qartli","tbilisi","mcxeta-mtianeti","kaxeti"]

statuses =["recovered","dead","infected"]

def checkIfLeapYear(year):
    if (int(year) % 4) == 0:
        if (int(year) % 100) == 0:
            if (int(year) % 400) == 0:
                return True
            else:
                return False
        else:
            return True
    else:
        return False

def checkDay(day, month, year):
    if int(month) in [1,3,5,7,8,10,12]:
        if int(day) in range(1,32):
            return True
        else:
            return "In this month we only have 31 days"

    elif int(month) in [4,6,9,11]:
        if int(day) in range(1,31):
            return True
        else:
            return "In this month we only have 30 days"

    elif int(month) == 2:
        answer = checkIfLeapYear(year)
        if answer == True:
            if int(day) in range(1,30):
                return True
            else:
                return "In that year in february we only had 29 days"
        elif answer == False:
            if int(day) in range(1,29):
                return True
            else:
                return "In that year in februaly we only had 28 days"

def checkDate(d):
    today = date.today()
    year = today.strftime("%Y")

    if d.count("/") == 2:
        dateLst = d.split("/")
        if len(str(dateLst[2])) == 4:
            if int(dateLst[2]) <= int(year):
                if len(str(dateLst[1])) == 2:
                    if int(dateLst[1]) in range(1,13):
                        if len(str(dateLst[0])) == 2:
                            answer = checkDay(dateLst[0],dateLst[1],dateLst[2])
                            if answer == True:
                                return True
                            else:
                                return answer
                        else:
                            return "You should write day with 2 digit."
                    else:
                        return "Invalid month"
                else:
                    return "You should write month with 2 digit."
            else:
                return "This year does not come yet."
        else:
            return "You should write year with 4 digit."
    else:
        return "Use two / or check if the date is letter-free."

def check(n,su,d,id,a,st):
    if n != "" and su != "" and d != "" and id != "" and a != "" and st !="":
        if " " not in n and " " not in su and " " not in d and " " not in id and " " not in a and " " not in st:
            if len(n) > 1:
                answer = checkDate(d)
                if answer == True:
                    try:
                        id = int(id)
                        if len(str(id)) == 11:
                            if a in areas:
                                if st in statuses:
                                    return "successfully"
                                else:
                                    return "Invalid status"
                            else:
                                return "Invalid area, please choose correct one."
                        else:
                            return "length of the if must be 11"
                    except:
                        return "Invalid ID,please use numbers."
                else:
                    return answer
            else:
                return "Name is too short."
        else:
            return "You can't use space in this fields."
    else:
        return "Please fill all the graphs."