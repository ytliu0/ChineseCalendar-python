import math
import numpy as np
from .names import *
from .date_and_time import getJDm, sexagenary_month_from_cyear_jian
from .era_names import era_name_lookup

def chunqiu_cmonth(cal, y):
    """
    Calculate all months in Chinese year y in the Chunqiu calendar.
    Input: 
      cal: the calendar object returned by the class calendar_conversion.
      y: Chinese year whose new year day is closest to Jan 1, y in Western calendar.
    Return: dictionary with keys 'cm', 'calendar', and (optional) 'regign/era', where 
      'cm': a list containing the information of all Chinese months in the form of [{'cm':m1, 'd':d1, 'jian':'jian1'}, {'cm':m2, 'd':d2, 'jian':'jian2'}, ...] with 'cm' indicating the Chinese month number (negative for a leap month), 'd' indicating the number of days from Dec 31, y-1 of the first day of the Chinese month, and 'jian' indicating the sexagenary month cycle associated with jian, which is 'NA' for the Chunqiu calendar. The list is sorted in ascending order in values in 'd'.

      'calendar' (str): version of the Chinese calendar, which is 'Chunqiu' here.

      'reign/era' (str, optional): reign and/or era name of the Chinese year.
    """
    lunar = 29.53067185978578;  # = 30328/1027
    yEpoch = -721;
    jdEpoch = 1457727.761054236; # Jan 16, 722 BC + 268/1027 days + 1e-4 days

    # Leap year pattern from -721 to -482
    leapYears = [0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0]
    # Accumulated leap years from -721 to -482
    accLeaps = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7, 7, 8, 8, 9, 9, 9, 9, 10, 10, 10, 11, 11, 12, 12, 12, 12, 13, 13, 13, 13, 13, 14, 15, 15, 16, 17, 17, 17, 18, 18, 18, 18, 19, 19, 19, 20, 20, 21, 21, 21, 22, 22, 22, 23, 24, 24, 24, 24, 24, 24, 25, 25, 26, 26, 27, 27, 28, 28, 28, 28, 29, 29, 30, 30, 30, 30, 31, 31, 32, 32, 32, 32, 32, 33, 33, 33, 34, 35, 35, 36, 36, 36, 37, 37, 37, 38, 38, 38, 39, 39, 39, 40, 40, 40, 41, 41, 41, 41, 42, 42, 43, 44, 44, 44, 45, 45, 45, 46, 46, 47, 47, 47, 47, 48, 48, 48, 49, 49, 49, 50, 50, 50, 51, 51, 52, 53, 53, 53, 53, 54, 54, 55, 55, 55, 56, 56, 56, 57, 57, 57, 58, 58, 59, 59, 59, 59, 60, 60, 60, 61, 62, 62, 62, 63, 63, 63, 63, 64, 65, 65, 65, 65, 66, 66, 67, 67, 67, 68, 68, 69, 69, 69, 70, 70, 70, 70, 71, 71, 72, 72, 73, 73, 74, 74, 74, 74, 75, 75, 75, 76, 77, 77, 77, 77, 77, 78, 78, 79, 79, 80, 80, 80, 80, 81, 81, 82, 82, 83, 83, 83, 84, 84, 84, 85, 85, 86, 86, 86, 87, 87, 87, 88, 88, 88]

    i = y - yEpoch
    leap = 0 if i < 0 else leapYears[i]
    accMonths = 12*i + (0 if i < 0  else accLeaps[i])
    m0 = jdEpoch + accMonths*lunar
    n = 12 + leap
    jd0 = getJDm(y-1, 12, 31)
    d = [int(math.floor(m0 + i*lunar - jd0)) for i in range(n+1)]
    cmonth = [{'cm':i+1, 'd':d[i], 'jian':'NA', 'n':d[i+1]-d[i]} for i in range(n)]
    if n==13: cmonth[12]['cm'] = -12
    if cal.lang=='Eng':
        cal_name = 'Chunqiu'
    elif cal.lang=='ChiT':
        cal_name = '春秋曆'
    else:
        cal_name = '春秋历'
    cyear = {'cm':cmonth, 'calendar':cal_name}
    cyear['reign/era'] = era_name_lookup(cal.lang, y, '', 'Chunqiu')
    return cyear

def guliuli_calendar_names(lang, li):
    guliuli = ['Zhou', 'Huangdi', 'Yin', 'Lu', 'Zhuanxu', 'Xia1', 'Xia2']
    if lang=='Eng':
        name = ['Zhou', 'Huangdi', 'Yin', 'Lu', 'Zhuanxu', 'Xia (Z11 version)', 'Xia (Z1 version)']
    elif lang=='ChiT':
        name = ['周曆', '黃帝曆', '殷曆', '魯曆', '顓頊曆', '夏曆 (冬至版)', '夏曆 (雨水版)']
    else:
        name =  ['周历', '黄帝历', '殷历', '鲁历', '颛顼历', '夏历 (冬至版)', '夏历 (雨水版)']
    ind = max([i if li==guliuli[i] else -1 for i in range(7)])
    if ind==-1:
        raise ValueError('Calendar '+li+' not supported!')
    return name[ind]

def guliuli_calendar_parameters(li):
    """
    Set up the calendar parameters for the ancient six calendars
    """
    solar = 365.25 # tropical year
    lunar = 29.0 + 499.0/940.0 # synodic month
    ziOffset=0
    if li=='Zhou':
        yEpoch = -104
        jdEpoch = 1683430.5001 # Dec 25, -104 + 1e-4 days
        jdEpoch_lunar = jdEpoch
    elif li=='Huangdi':
        yEpoch = 170
        jdEpoch = 1783510.5001 # jdEpoch = 1783510.5001
        jdEpoch_lunar = jdEpoch
    elif li=='Yin':
        ziOffset = 1 # first month of a year is the chou month
        yEpoch = -47
        jdEpoch = 1704250.5001 # Dec 26, -47 + 1e-4 days
        jdEpoch_lunar = jdEpoch
    elif li=='Lu':
        yEpoch = -481
        jdEpoch = 1545730.5001 # Dec 25, -481 + 1e-4 days
        jdEpoch_lunar = jdEpoch - lunar/19.0 # runyu = 1/19 *(29 + 499/940) days
    elif li=='Zhuanxu':
        ziOffset = -1 # first month of a year is the hai month
        yEpoch = 14
        jdEpoch_lunar = 1726575.5001 # Feb 9, 15 + 1e-4 days
        jdEpoch = jdEpoch_lunar - solar/8.0 # J1 -> Z11
    elif li=='Xia1':
        ziOffset = 2 # first month of a year is the yin month
        yEpoch = 444
        jdEpoch = 1883590.5001 # Dec 28, 444 + 1e-4 days
        jdEpoch_lunar = jdEpoch
    elif li=='Xia2':
        ziOffset = 2 # first month of a year is the yin month
        yEpoch = 444
        jdEpoch_lunar = 1883650.5001 # Feb 26, 445 + 1e-4 days
        jdEpoch = jdEpoch_lunar - solar/6.0 # Z1 -> Z11
    else:
        raise ValueError('Calendar '+li+' not supported!')
    return yEpoch, jdEpoch, jdEpoch_lunar, ziOffset

def guliuli_solar_terms(y, li):
    """
    Calculate the solar terms J12-Z11 in year y
    Return: numpy array containing the Julian dates at noon of J12-Z11
    """
    yEpoch, jdEpoch, jdEpoch_lunar, ziOffset = guliuli_calendar_parameters(li)
    solar = 365.25 # tropical year
    dqi = solar/24
    dy = y - yEpoch - 1 
    J12 = jdEpoch + dy*solar + dqi # J12 closest to Jan 1, y 
    return np.array([int(math.floor(J12 + i*dqi + 0.5)) for i in range(24)])

def guliuli_calendar_cmonth(cal, y, li):
    """
    Calculate all months in Chinese year y in the specified ancient six calendar.
    Input: 
      cal: the calendar object returned by the class calendar_conversion.
      y: Chinese year whose new year day is closest to Jan 1, y in Western calendar.
      li (str): calendar label ('Zhou', 'Huangdi', 'Yin', 'Lu', 'Zhuanxu', 'Xia1' or 'Xia2').
    Return: dictionary with keys 'cm', 'calendar', and (optional) 'regign/era', where 
      'cm': a list containing the information of all Chinese months in the form of 
      [{'cm':m1, 'd':d1, 'jian':'jian1', n:n1}, {'cm':m2, 'd':d2, 'jian':'jian2', n:n2}, ...] 
      with 'cm' indicating the Chinese month number (negative for a leap month), 'd' indicating the number of days from Dec 31, y-1 of the first day of the Chinese month, 'jian' indicating the sexagenary month cycle associated with jian ('jian'='1' for jia zi, '2' for yi chou, ... '60' for gui hai, 'NA' for leap month, 'NZ' for a month not containing a major solar term, and 'n' indicating the number of days in the Chinese month. The list is sorted in ascending order in values in 'd'.

      'calendar' (str): name of the calendar.

      'reign/era': reign name of the Chinese year.
    """
    yEpoch, jdEpoch, jdEpoch_lunar, ziOffset = guliuli_calendar_parameters(li)
    solar = 365.25 # tropical year
    lunar = 29.0 + 499.0/940.0 # synodic month
    dy = y - yEpoch - 1
    w0 = jdEpoch + dy*solar # winter solstice (pingqi) in year y-1
    w1 = w0 + solar # winter solstice (pingqi) in year y
    i = math.floor((math.floor(w0+1.5) - 0.5 - jdEpoch_lunar)/lunar)
    m0 = jdEpoch_lunar + i*lunar
    m1 = m0 + 13*lunar
    n = 13 if math.floor(m1+0.5) < math.floor(w1+0.5)+0.1 else 12 # number of months in y
    month_offset = ziOffset
    if ziOffset > 0:
        # The first month in Chinese year y is determined by an offset from 
        # the month containing the winter solstice in year y-1;
        # Number of months in y is determined by the number of months between 
        # winter solstices in y and y+1.
        # Move the beginning month to a month later if there is a leap month in y-1.
        month_offset += 1 if n==13 else 0 
        # now determine the number of months in year y
        m1 = m0 + (n+13)*lunar 
        w2 = w1 + solar # winter solstice (pingqi) in year y+1
        n = 13 if math.floor(m1+0.5) < math.floor(w2+0.5)+0.1 else 12
    m0 += month_offset*lunar
    jd0 = getJDm(y-1, 12, 31)
    dZqi = 30.4375  # number of days between two successive Zhongqi's
    cmonth = []
    for i in range(n):
        if li=='Zhuanxu':
            cm = -9 if i==12 else 1 + ((i+9) % 12)
        else:
            cm = -12 if i==12 else i+1
        m = m0 + i*lunar
        # number of days in the month
        d = int(math.floor(m - jd0))
        nm = int(math.floor(m + lunar - jd0)) - d
        k = math.floor((math.floor(m + 0.5) - 0.5 - w0)/dZqi) + 1
        jian = 'NA'
        if w0 + k*dZqi + 0.5 > math.floor(m + lunar + 0.5):
            # This is a no Zhongqi month.
            # Leap month is placed at the end of the year rather than the no Zhongqi month.
            # No Zhongqi month is indicated (by jian='NZ') for reference only
            jian = 'NZ'
        cmonth += [{'cm':cm, 'd':d, 'jian':jian, 'n':nm}]
    cyear = {'cm':cmonth, 'calendar':guliuli_calendar_names(cal.lang, li)}
    cyear['reign/era'] = era_name_lookup(cal.lang, y, '', li)
    return cyear

def QinEarlyHan_calendar_cmonth(cal, y):
    """
    Calculate all months in Chinese year y in Qin and Early Han period (-220 - -103) 
    based on Li Zhonglin's paper "Researches on Calendars from Qin to early Han (246 B.C. to 104 B.C.) 
    -- centering on excavated calendrical bamboo slips", in Zhong guo shi yan jiu (Studies in Chinese History), 
    issue no. 2, pp. 17-69 (2012).

    Input: 
      cal: the calendar object returned by the class calendar_conversion.
      y: Chinese year whose new year day is closest to Jan 1, y in Western calendar.
    Return: dictionary with keys 'cm', 'calendar', and (optional) 'regign/era', where 
      'cm': a list containing the information of all Chinese months in the form of 
      [{'cm':m1, 'd':d1, 'jian':'jian1', n:n1}, {'cm':m2, 'd':d2, 'jian':'jian2', n:n2}, ...]  
      with 'cm' indicating the Chinese month number (negative for a leap month), 'd' indicating the number of days from Dec 31, y-1 of the first day of the Chinese month, 'jian' indicating the sexagenary month cycle associated with jian, which is 'NA' for this calendar, and 'n' indicating the number of days in the Chinese month. The list is sorted in ascending order in values in 'd'.

      'calendar' (str): name of the calendar.

      'reign/era': reign name of the Chinese year.
    """
    lunar = 29 + 499.0/940
    # Calendar A data 
    jdEpoch = 1589523.5001
    accMonEpoch = 1670
    if y >= -162:
        # Calendar C data
        jdEpoch = 1646163.5001
        accMonEpoch = 321
    elif y >= -201:
        # Calendar B data
        jdEpoch = 1633701.5001
        accMonEpoch = 174
    yEpochLeap = -225 if y < -162 else -179
    leapCycle = [0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1]
    accMonCycle = [0, 12, 24, 37, 49, 61, 74, 86, 98, 111, 123, 136, 148, 160, 173, 185, 197, 210, 222]
    yInCycle = (y - yEpochLeap) % 19
    accMons = 235*int(math.floor(((y - yEpochLeap)/19.0))) + accMonCycle[yInCycle] + accMonEpoch
    leap = leapCycle[yInCycle]
    n = 12 + leap
    m0 = accMons*lunar + jdEpoch - getJDm(y-1, 12, 31) # first month in y
    d = [int(math.floor(m0 + i*lunar)) for i in range(n+1)]
    cmonth = [{'cm':1 + ((i+9)%12), 'd':d[i], 'jian':'NA', 'n':d[i+1]-d[i]} for i in range(n)]
    if n==13: cmonth[12]['cm'] = -9
    if cal.lang=='Eng':
        cal_name = 'Qin and Early Han'
    elif cal.lang=='ChiT':
        cal_name = '秦漢顓頊曆'
    else:
        cal_name = '秦汉颛顼历'
    cyear = {'cm':cmonth, 'calendar':cal_name}
    cyear['reign/era'] = era_name_lookup(cal.lang, y, 'default')
    return cyear

# Calendars after the Qin dynasty
def get_li_parameters(li):
    """
    Return calendar parameters for different calendars
    """
    lunar=0; solar=0; jd_epoch=0; JDw=0; dtc_round=0; dts_round=0;
    if li=='Sifen':
        lunar = 29 + 499.0/940
        solar = 365.25
        jd_epoch = 1662610.5
        JDw = 1721050.5
        dtc_round = 1e-3; dts_round = 1e-3
        name = {'Eng':'Sifen', 'ChiT':'四分曆', 'ChiS':'四分历'}
    elif li=='Qianxiang':
        lunar = 29 + 773.0/1457
        solar = 365 + 145.0/589;
        JDw = 1721050.5 + 210.0/589
        jd_epoch = 1796295.5 + 1067.0/1457
        dtc_round = 1e-4; dts_round = 1e-5
        name = {'Eng':'Qianxiang', 'ChiT':'乾象曆', 'ChiS':'乾象历'}
    elif li=='Jingchu':
        lunar = 29 + 2419.0/4559
        solar = 365 + 455.0/1843
        JDw = 1721050.5 + 220.0/1843
        jd_epoch = 1811120.5
        dtc_round = 1e-4; dts_round = 1e-5
        name = {'Eng':'Jingchu', 'ChiT':'景初曆', 'ChiS':'景初历'}
    elif li=='Sanji':
        lunar = 29 + 3217.0/6063.0
        solar = 365 + 605.0/2451.0
        JDw = 1721050.5 + 280.0/2451.0
        jd_epoch = 1861292.5 + 2826.0/6063.0
        dtc_round = 1e-4; dts_round = 1e-5
        name = {'Eng':'Sanji', 'ChiT':'三紀曆', 'ChiS':'三紀历'}
    elif li=='Xuanshi':
        lunar = 29.0 + 47251.0/89052.0
        solar = 365.0 + 1759.0/7200.0
        JDw = 1721048.5 + 1189.0/1200.0
        jd_epoch = 1871510.5 + 4995.0/89052.0
        dtc_round = 1e-6; dts_round = 1e-6
        name = {'Eng':'Xuanshi', 'ChiT':'玄始曆', 'ChiS':'玄始历'}
    elif li=='Zhengguang':
        # 正光
        lunar = 29.0 + 39769.0/74952.0
        solar = 365.0 + 1477.0/6060.0
        JDw = 1721048.5 + 569.0/1515.0
        jd_epoch = 1911671.5 + 6427.0/9369.0
        dtc_round = 1e-6; dts_round = 1e-6
        name = {'Eng':'Zhengguang', 'ChiT':'正光曆', 'ChiS':'正光历'}
    elif li=='fakeMingKeRang':
        # The parameters for this calendar were not prserved. The following parameters 
        # are tweaked from Zhengguang li according to p. 24 in Volume 6 of 《歷代長術輯要》 by 
        # 汪曰楨: 此術無考，劉氏長術仍借正光術推之，但依史文移置閏月。
        # 今從其例增節氣小餘十分之四，乃與當時置閏相符。
        lunar = 29.0 + 39769.0/74952.0
        solar = 365.0 + 1477.0/6060.0
        JDw = 1721048.5 + 569.0/1515.0 + 0.4
        jd_epoch = 1911671.5 + 6427.0/9369.0
        dtc_round = 1e-6; dts_round = 1e-6
        name = {'Eng':'Mingkerang', 'ChiT':'明克讓曆', 'ChiS':'明克让历'}
    elif li=='Xinghe':
        lunar = 29.0 + 110647.0/208530.0
        solar = 365.0 + 4117.0/16860.0
        JDw = 1721048.5 + 1118.0/4215.0
        jd_epoch = 1918286.5 + 111983.0/208530.0
        dtc_round = 1e-6; dts_round = 1e-6
        name = {'Eng':'Xinghe', 'ChiT':'興和曆', 'ChiS':'兴和历'}
    elif li=='Tianbao':
        lunar = 29.0 + 155272.0/292635.0
        solar = 365.0 + 5787.0/23660.0
        JDw = 1721049.5 + 193.0/5915.0
        jd_epoch = 1921918.5 + 231721.0/292635.0
        dtc_round = 1e-6; dts_round = 1e-6
        name = {'Eng':'Tianbao', 'ChiT':'天保曆', 'ChiS':'天保历'}
    elif li=='Tianhe':
        lunar = 29.0 + 153991.0/290160.0
        solar = 365.0 + 5731.0/23460.0
        JDw = 1721047.5 + 1331.0/3910.0
        jd_epoch = 1928976.5 + 246737.0/290160.0
        dtc_round = 1e-6; dts_round = 1e-6
        name = {'Eng':'Tianhe', 'ChiT':'天和曆', 'ChiS':'天和历'}
    elif li=='Daxiang':
        lunar = 29.0 + 28422.0/53563.0
        solar = 365.0 + 3167.0/12992.0
        JDw = 1721048.5 + 281.0/6496.0
        jd_epoch = 1932520.5 + 36950.0/53563.0
        dtc_round = 1e-5; dts_round = 1e-6
        name = {'Eng':'Daxiang', 'ChiT':'大象曆', 'ChiS':'大象历'}
    elif li=='Kaihuang':
        lunar = 29.0 + 96529.0/181920.0
        solar = 365.0 + 25063.0/102960.0
        JDw = 1721048.5 + 908.0/6435.0
        jd_epoch = 1934971.5 + 19841.0/36384.0
        dtc_round = 1e-6; dts_round = 1e-7
        name = {'Eng':'Kaihuang', 'ChiT':'開皇曆', 'ChiS':'开皇历'}
    elif li=='Xuanming':
        # Note: only for pinqi calculation
        solar = 365.0 + 137.0/560.0
        JDw = 1721047.5 + 93.0/140.0
        dts_round = 1e-5
        name = {'Eng':'Xuanming', 'ChiT':'宣明曆', 'ChiS':'宣明历'}
    elif li=='RevisedDaming':
        # Note: only for pinqi calculation
        solar = 365.0 + 637.0/2615.0
        JDw = 1721048.5 + 542.0/2615.0
        dts_round = 1e-5
        name = {'Eng':'Revised Daming', 'ChiT':'重修大明曆', 'ChiS':'重修大明历'}
    elif li=='Datong':
        # Note: only for pinqi calculation
        solar = 365.2425
        JDw = 1721049.9175
        dts_round = 1e-8
        name = {'Eng':'Datong', 'ChiT':'大統曆', 'ChiS':'大统历'}
    else:
        raise ValueError(li+' calendar is not supported.')
    jd_epoch += dtc_round; JDw += dts_round
    return {'li':li, 'lunar':lunar, 'solar':solar, 'jd_epoch':jd_epoch, 
            'JDw':JDw, 'dtc_round':dtc_round, 'dts_round':dts_round, 'name':name}

def compute_pingqi(y, li):
    """
    Compute the calendarical solar terms J12-Z11 in year y
    Input: 
      y (int): Western y
    Return: integer numpy array of size 24 containing pingqi's Julian date at noon from J12 closest to Jan 1, y to Z11.
    """
    para = get_li_parameters(li)
    dqi = para['solar']/24 # number of days between 2 successive pingqi's
    J12 = para['JDw'] + y*para['solar'] + dqi
    return np.array([int(math.floor(J12 + i*dqi + 0.5)) for i in range(24)])

def pingshou_noZhongqi_cmonth(cal, y, li, region):
    """
    Calculate all months in Chinese year y in Chinese calendar specified by li using the no Zhongqi rule.

    Input: 
      cal: the calendar object returned by the class calendar_conversion.
      y (int): Chinese year whose new year day is closest to Jan 1, y in Western calendar.
      li (str): label of the Chinese calendar.
      region (str): label of the region to look up the reign/era name.
    Return: dictionary with keys 'cm', 'calendar' and 'reign/era', where 
      'cm': a list containing the information of all Chinese months in the form of 
      [{'cm':m1, 'd':d1, 'jian':'jian1', n:n1}, {'cm':m2, 'd':d2, 'jian':'jian2', n:n2}, ...] 
      with 'cm' indicating the Chinese month number (negative for a leap month), 'd' indicating the number of days from Dec 31, y-1 of the first day of the Chinese month, and 'jian' indicating the sexagenary month cycle associated with jian ('NA' for leap months), and 'n' indicating the number of days in the Chinese month. The list is sorted in ascending order in values in 'd'.

      'calendar' (str): name of the calendar.

      'reign/era' (str): reign/era name of the Chinese year.
    """
    para = get_li_parameters(li)
    jd0 = getJDm(y-1, 12, 31)
    Z1 = para['JDw'] + (y + 1.0/6)*para['solar'] # JD of Z1 in year y
    # midnight after Z1 in y+1
    Z1b = math.floor(Z1 + para['solar'] + 0.5) + 0.5
    i1 = math.floor((math.floor(Z1 + 0.5) + 0.5 - para['jd_epoch'])/para['lunar'])
    m1 = para['jd_epoch'] + i1*para['lunar'] # JD of new year day in y
    # has a leap month?
    leap = 0 if m1 + 13*para['lunar'] > Z1b else 1
    n = 12 + leap # total number of months in year y
    jian = sexagenary_month_from_cyear_jian(y)
    m = 0
    findLeap = (leap==1) # need to find a leap month?
    if findLeap:
        dZqi = para['solar']/12 # number of days between two successive Zhongqi's
        # dates of Zhongqi's from Z11 in previous year to Z1 in the following years.
        Zqi = np.array([int(math.floor(Z1 + i*dZqi - jd0)) for i in range(-1, 13)])
    cmonth = []
    m1 -= jd0
    for i in range(n):
        m += 1
        mi = m1 + i*para['lunar']
        d = int(math.floor(mi))
        d1 = int(math.floor(mi + para['lunar']))
        if findLeap:
            k = np.searchsorted(Zqi, d, 'left')
            if Zqi[k] >= d1:
                # found the leap month
                m -= 1
                cmonth += [{'cm':-m, 'd':d, 'jian':'NA', 'n':d1-d}]
                findLeap = False
                continue
        cmonth += [{'cm':m, 'd':d, 'jian':jian[m-1], 'n':d1-d}]
    return {'cm':cmonth, 
            'calendar':para['name'][cal.lang], 
            'reign/era':era_name_lookup(cal.lang, y, region)}
    