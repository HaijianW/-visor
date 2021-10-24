import math as m
## read files in crn file
def read_from_crn(r_file_name):
  try:
    file = open(r_file_name, "r")
    header = file.readline()
    title = file.readlines()
    file.close()
    return (header, title)
  except:
    print("file missing")

## return title dictionary
def crn_dic(r_file_name, w_file_name):
  dic = {}
  (header, title) = read_from_crn(r_file_name)
  dic["header"] = tuple(header.strip().split(","))
  for string in title:
    alist = string.strip().split(",")
    key = alist[0] + alist[1] + ",CRN" + alist[2]
    day = alist[4]
    if alist[4] in "MWF":
      day = str(1)
    else:
      day = str(2)
    duration = int(alist[6]) - int(alist[5])
    scale = 0
    try:
      scale = float(alist[7]) * m.sqrt(float(alist[9])) / float(alist[8])
    except:
      scale = float(alist[7]) * m.sqrt(float(alist[9])) / 5
    scale = round(scale, 2)
    dic[key] = day + "," + str(alist[5]) + "," + str(duration) + "," + str(scale)
  file = open(w_file_name, "w")
  for key in dic:
    if key == "header":
      continue
    file.write(key + "," + str(dic[key]) + "\n")
  file.close()
  return dic

## title files
def title_dic(r_file_name, w_file_name):
  (header, title) = read_from_crn(r_file_name)
  file = open(w_file_name, "w")
  dic = {}
  for string in title:
    alist = string.strip().split(",")
    key = alist[0].upper() + alist[1]
    prer = alist[-2]
    credit = alist[-1]
    dic[key] = key + "," + str(prer) + "," + str(credit) + "," + str(0) + "\n"
  for key in dic:
    file.write(dic[key])
  file.close()
  return dic

## required class
def required_class(r_file_name, w_file_name):
  alist = []
  file = open(r_file_name, "r")
  data = file.readline()
  data = file.readlines()
  for lines in data:
    string = lines.strip()
    string = string.split(",")
    for item in string:
      if item != "":
        alist.append(item)
  file = open(w_file_name, "w")
  for item in alist:
    file.write(item + "\n")
  file.close()
  return alist

## change weight
def core_title_weight(required_class, title_dic):
  alist = []
  file = open(required_class, "r")
  data = file.readlines()
  file.close()
  for item in data:
    alist.append(item.strip())
  file = open(title_dic, "r")
  data = file.readlines()
  file.close()
  blist = []
  for item in data:
    temp = item.split(",")
    if temp[1] != "0000":
      blist.append(temp[1])
  file = open(title_dic, "w")
  for lines in data:
    str_list = lines.strip().split(",")
    if str_list[0] in alist:
      str_list[-1] = int(str_list[-1]) + 1
    if str_list[0] in blist:
      str_list[-1] = int(str_list[-1]) + 1
    temp = ""
    for item in str_list:
      temp += str(item) + ","
    temp2 = temp[: -1] + "\n"
    file.write(temp2)

## return a priority list
def priority_list(student_file, title_dic):
  file = open(student_file, "r")
  file.readline()
  data = file.readlines()
  meet_pre = []
  for string in data:
    temp = string.strip().split(",")[0]
    meet_pre.append(temp)
  file.close()
  alist = []
  file = open(title_dic, "r")
  data = file.readlines()
  file.close()
  for priority in range(3, -1, -1):
    for item in data:
      temp_list = item.strip().split(",")
      if int(temp_list[-1]) == priority and temp_list[1] in meet_pre:
        alist.append(temp_list[0])
  return alist


def sortkey(e):
  return e["rate"]

def schedule(student_file, title_dic, crn_dic):
  regist_dic = {}
  check_list = priority_list(student_file, title_dic)
  file = open(crn_dic, "r")
  data = file.readlines()
  for string in data:
    temp = string.strip().split(",")
    if temp[0] not in check_list:
      continue
    stime = int(temp[2]) *10000 + int(temp[3])
    if int(temp[3]) < 0:
      stime = 0
    if temp[0] in regist_dic:
      regist_dic[temp[0]].append({"CRN":temp[1], "stime" : stime, "duration" : temp[4], "rate" : temp[-1]})
    else:
      regist_dic[temp[0]] = [{"CRN":temp[1], "stime" : stime, "duration" : temp[4], "rate" : temp[-1]}]
  for crn in regist_dic:
    regist_dic[crn].sort(reverse=True, key = sortkey)
  timeline = []
  worksheet = []
  for title in regist_dic:
    for crn in regist_dic[title]:
      stime = crn["stime"]
      etime = stime + int(crn["duration"])
      flag = True
      for timeinterval in timeline:
        if stime in timeinterval and etime in timeinterval:
          flag = False
          break
      if flag:
        worksheet.append(crn["CRN"])
        timeline.append(range(stime, etime))
        break
  return worksheet
  
  


  
## main
crn_dic = crn_dic("crn_data.csv", "crn_dic.csv")
title_dic = title_dic("crn_data.csv", "title_dic.csv")
required_class = required_class("core_requirements.csv", "CS_major.csv")
core_title_weight("CS_major.csv", "title_dic.csv")
print(schedule("student.csv", "title_dic.csv", "crn_dic.csv"))
