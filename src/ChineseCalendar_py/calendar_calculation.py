import numpy as np
from .names import *
from .date_and_time import *
from .ancient_calendars import chunqiu_cmonth, guliuli_calendar_cmonth, QinEarlyHan_calendar_cmonth, pingshou_noZhongqi_cmonth, guliuli_solar_terms, compute_pingqi
from .era_names import era_name_lookup
from .calendar_notes import monthly_calendarNotes, addYearInfo, addChineseYearNote
import math

def Western_date_sexagenary_date_week_from_JDN(cal, jdn):
    """
    Given Julian date at Noon jdn, calculate the sexagenary date and the day of week
    Input:
      cal: the object returned by the class calendar_conversion.
      jdn (int): Julian date at noon
    Return: tuple (wdate, wcal, sex_date, week)
      wdate (list of integers): [year, month, day] in the Western calendar
      wcal (str): Western calendar name
      sex_date (list): [sexagenary date string, sexagenary number]
      week (list): [day of week string, day of week number]
    """
    date = CalDat(jdn, 0)
    wdate = [date['yy'], date['mm'], date['dd']]
    wcal = 2
    if jdn < 2299161: wcal = 1
    if jdn < 1723980: wcal = 0
    wcal = cal.western_calendar_names[wcal] # Western calendar name
    week = (jdn + 1) % 7
    week = [cal.week[(jdn + 1) % 7], week] # date of week
    sex = (jdn - 11) % 60
    sex_date = [cal.stem[sex % 10] + cal.branch[sex % 12], sex+1] # sexagenary date, sexagenary number
    return wdate, wcal, sex_date, week

def chinese_to_western_date_lookup(cal, y, m, d, calendar, calendar_func):
    """
    Calculate the date in the Western claendar of the d-th day in month m in Chinese year y
    Input:
      cal: the object returned by the class calendar_conversion.
      y, m, d (int): year, month and day in the Chinese calendar (negative m indicates a leap month).
      calender (str): version of Chinese calendar. Only support the calendars listed in available_calendars() in calendar_conversion.py.
      calendar_func: python function that returns a dictionary with keys 'cm', 'calendar', and (optional) 'regign/era' (see the doc string of e.g. default_Chinese_year_data() for detail)
    Return:
      dictionary containing the information of the date in Chiense calendar.
    """
    cy = calendar_func(cal, y)
    cm = [x for x in cy['cm'] if x['cm']==m]
    if len(cm)==0:
      raise RuntimeError('The requested Chinese month does not exist in Chinese year '+str(y)+' in the '+calendar+' calendar.')
    match = sum([(1 if x['n'] >= d else 0) for x in cm])
    if match==0:
      raise RuntimeError('The requested Chinese date does not exist in the '+calendar+' calendar.')
    jd0 = int(math.floor(getJDm(y-1,12,31) + 0.6))
    wdate = []
    sex = (y + 3536) % 60
    sex_cyear = [cal.stem[sex % 10] + cal.branch[sex % 12], cal.branch_animal[sex % 12], sex+1]
    for cmd in cm:
        jdn = jd0 + cmd['d'] + d-1
        wd, wcal, sex_date, week = Western_date_sexagenary_date_week_from_JDN(cal, jdn)
        # Chinese date
        cymd = [y, m, d]
        cmonth = chinese_month_label(cal, y, m, calendar)
        if calendar=='default' and y==700 and cal.lang != 'Eng' and cmd['jian']=='25':
            # This is the second month 11 in 700
            cmonth = '十一月'
        if cmd['jian']=='NZ': 
            # add no Zhongqi label (for the ancient six and early Han calendars)
            cmonth += '(' + no_Zhongqi_label(cal.lang) + ')'
        cday = cal.cday[d-1]
        date = {'Chinese ymd':cymd, 'Western ymd':wd,
                'Western calendar':wcal, 'JDN':jdn, 'cyear':y, 'cdate':cmonth+cal.cmonth_sep+cday, 
                'sexagenary year':sex_cyear}
        if cmd['jian'] != 'NA' and cmd['jian'] != 'NZ':
            jian_num = int(cmd['jian'])
            jian_name = '建' if cal.lang=='ChiT' or cal.lang=='ChiS' else ''
            date['jian'] = [jian_name + cal.stem[(jian_num-1) % 10] + cal.branch[(jian_num-1) % 12], jian_num]
        date['Nday_cmonth'] = cmd['n']
        date['sexagenary date'] = sex_date
        date['Week'] = week
        date['period'] = cal.period[np.searchsorted(cal.period_byear, y, 'right') - 1]
        if cy['reign/era'] != 'NA': date['reign/era'] = cy['reign/era']
        date['Chinese calendar'] = cy['calendar']
        if calendar=='default':
            if y==-103 and jdn < 1683608: 
                calName = {'Eng':'Qin and Early Han', 'ChiT':'秦漢顓頊曆', 'ChiS':'秦汉颛顼历'}
                date['Chinese calendar'] = calName[cal.lang]
            if y==1913 and jdn > 2420133:
                calName = {'Eng':'Republic of China', 'ChiT':'中華民國曆', 'ChiS':'中华民国历'}
                date['Chinese calendar'] = calName[cal.lang]
        wdate += [date]
    return wdate[0] if len(wdate)==1 else wdate

def chinese_year_to_western_date_lookup(cal, y, m, calendar, calendar_func):
    """
    Given a Chinese year y, return the Western dates in all days in the year if m is None or Western dates in all days in month m in the Western calendar.
    Input:
      cal: the object returned by the class calendar_conversion.
      y (int): year in the Chinese calendar.
      m (int): None if request all days in year y. If 1 <= |m| <= 12, return dates in month m (negative denotes a leap month) in year y.
      calender (str): version of Chinese calendar. Only support the calendars listed in available_calendars() in calendar_conversion.py
    Return:
      a python list of dicts containing the information of the Western dates in the Chinese year/month.
    """
    cy = calendar_func(cal, y)
    if not (m is None):
        cm = [x for x in cy['cm'] if x['cm']==m]
        if len(cm)==0:
            raise RuntimeError('The requested Chinese month does not exist in Chinese year '+str(y)+' in the '+calendar+' calendar.')
        return chinese_month_to_western_date_lookup(cal, y, cm, calendar, cy['reign/era'], cy['calendar'])
    
    wdate = []
    for cm in cy['cm']:
        wdate += chinese_month_to_western_date_lookup(cal, y, [cm], calendar, cy['reign/era'], cy['calendar'])
    return wdate
        
def chinese_month_to_western_date_lookup(cal, y, cm, calendar, reign, chinese_calendar):
    """
    Given a Chinese year y and Chinese month m (contained in cm), return the Western dates in all days in the month by doing a batch date lookup.
    Input:
      cal: the object returned by the class calendar_conversion.
      y (int): year in the Chinese calendar.
      m (int): None if request all days in year y. If 1 <= |m| <= 12, return dates in month m (negative denotes a leap month) in year y.
      cm (list): [{'cm':m, 'd':d1, 'jian':'jian1', n:n1}, {'cm':m, 'd':d2, 'jian':'jian2', n:n2}] with 'cm' indicating the Chinese month number (negative for a leap month), 'd' indicating the number of days from Dec 31, y-1 of the first day of the Chinese month, 'jian' indicating the sexagenary month cycle associated with jian ('jian'='1' for jia zi, '2' for yi chou, ... '60' for gui hai, 'NA' for leap month, 'NZ' for a month not containing a major solar term (only for the ancient six calendars)), and 'n' indicating the number of days in the Chinese month. The list is sorted in ascending order in values in 'd'. For this input, len(cm)=1 or 2, if len(cm)==2, both months in cm must have the same Chinese month number, but their jian's are different.
      calender (str): version of Chinese calendar. Only support the calendars listed in available_calendars() in calendar_conversion.py
      reign (str): reign/era name of the Chinese year
      chinese_calendar (str): name of the Chinese calendar version
    Return:
      a python list of dicts containing the information of the Western dates in the Chinese month.
    """
    m = cm[0]['cm']
    jd0 = int(math.floor(getJDm(y-1,12,31) + 0.6))
    wdate = []
    sex = (y + 3536) % 60
    sex_cyear = [cal.stem[sex % 10] + cal.branch[sex % 12], cal.branch_animal[sex % 12], sex+1]
    history_period = cal.period[np.searchsorted(cal.period_byear, y, 'right') - 1]
    for cmd in cm:
        jdm = jd0 + cmd['d'] - 1 # Julian date at noon on the 0th day of the Chinese month
        # Chinese month
        cmonth = chinese_month_label(cal, y, m, calendar)
        if calendar=='default' and y==700 and cal.lang != 'Eng' and cmd['jian']=='25':
            # This is the second month 11 in 700
            cmonth = '十一月'
        if cmd['jian']=='NZ': 
            # add no Zhongqi label (for the ancient six and early Han calendars)
            cmonth += '(' + no_Zhongqi_label(cal.lang) + ')'
        jian = 'NA'
        if cmd['jian'] != 'NA' and cmd['jian'] != 'NZ':
            jian_num = int(cmd['jian'])
            jian_name = '建' if cal.lang=='ChiT' or cal.lang=='ChiS' else ''
            jian = [jian_name + cal.stem[(jian_num-1) % 10] + cal.branch[(jian_num-1) % 12], jian_num]

        # Now loop through all days in the Chinese month
        for d in range(1, cmd['n']+1):
            jdn = jdm + d
            wd, wcal, sex_date, week = Western_date_sexagenary_date_week_from_JDN(cal, jdn)
            # Chinese date
            cymd = [y, m, d]
            cday = cal.cday[d-1]
            date = {'Chinese ymd':cymd, 'Western ymd':wd,
                'Western calendar':wcal, 'JDN':jdn, 'cyear':y, 'cdate':cmonth+cal.cmonth_sep+cday, 
                'sexagenary year':sex_cyear}
            if jian != 'NA': date['jian'] = jian
            date['Nday_cmonth'] = cmd['n']
            date['sexagenary date'] = sex_date
            date['Week'] = week
            date['period'] = history_period
            if reign != 'NA': date['reign/era'] = reign
            date['Chinese calendar'] = chinese_calendar
            if calendar=='default':
                if y==-103 and jdn < 1683608: 
                    calName = {'Eng':'Qin and Early Han', 'ChiT':'秦漢顓頊曆', 'ChiS':'秦汉颛顼历'}
                    date['Chinese calendar'] = calName[cal.lang]
                if y==1913 and jdn > 2420133:
                    calName = {'Eng':'Republic of China', 'ChiT':'中華民國曆', 'ChiS':'中华民国历'}
                    date['Chinese calendar'] = calName[cal.lang]
            wdate += [date]

    return wdate

def western_to_chinese_date_lookup(cal, y, dd, jdn, calendar, calendar_func):
    """
    Calculate the date in the Chinese claendar in Western year y and on dd days from Dec 31, y-1.
    Input:
      cal: the object returned by the class calendar_conversion.
      y (int): Western year (int)
      dd (int): number of days from Dec 31, y-1.
      jdn (int): Julian date at noon 
      calendar (str): label of the Chinese calendar
      calendar_func: python function that returns a dictionary with keys 'cm', 'calendar', and (optional) 'regign/era' (see the doc string of e.g. default_Chinese_year_data() for detail)
    Return:
      dictionary containing the information of the date in Chiense calendar.
    """
    if calendar=='default':
        # Make these changes to be consistent with the transition of calendars on my Chinese calendar website
        if y==-480:
            calendar_func = chunqiu_cmonth
        elif y==-221:
            calendar_func = lambda cal, y: guliuli_calendar_cmonth(cal, y, 'Zhou')
    # load calendar data in years y-1, y and y+1
    cyearD1 = calendar_func(cal, y)
    cyearD2 = calendar_func(cal, y+1)
    # For the default calendar, use the Zhou calendar untill -220.
    if calendar=='default' and y==-221: cyearD2['reign/era'] = 'NA'
    cyear = y
    nd1 = NdaysGregJul(y) # number of days in Western year y
    if dd < cyearD1['cm'][0]['d']:
        cyear -= 1
        cyearD0 = calendar_func(cal, y-1)
        return chinese_date_from_table(cal, dd + NdaysGregJul(y-1), jdn, cyear, cyearD0, calendar)
    elif dd >= cyearD2['cm'][0]['d'] + nd1:
        cyear += 1
        return chinese_date_from_table(cal, dd - nd1, jdn, cyear, cyearD2, calendar)
    else:
        return chinese_date_from_table(cal, dd, jdn, cyear, cyearD1, calendar)
    
def western_to_chinese_date_lookup_batch(cal, jdn, calendar, calendar_func):
    """
    Calculate the dates in the Chinese claendar for given jdn (Julian date at noon).
    Input:
      cal: the object returned by the class calendar_conversion.
      jdn (numpy.int array): Julian date at noon
      calendar (str): label of the Chinese calendar
      calendar_func: python function that returns a dictionary with keys 'cm', 'calendar', and (optional) 'regign/era' (see the doc string of e.g. default_Chinese_year_data() for detail)
    Return:
      list of dictionary containing the information of the date in Chiense calendar.
    """
    jdn = jdn.astype(np.int32)
    jdn_min = int(math.floor((cal.ybeg + 4712)*365.25))-1
    jdn_max = int(math.floor(2451545 + (cal.yend - 1999)*365.2425)) + 1
    if calendar=='default' and (np.any(jdn < jdn_min) or np.any(jdn > jdn_max)):
        raise ValueError('All values in jdn must be in ['+str(jdn_min)+','+str(jdn_max)+']')
    # function to convert JDN to Western year
    jdn_to_wyear = lambda x: np.floor(np.where(x < 2299161, (x+0.5)/365.25 - 4712, (x - 2451544.5)/365.2425 + 2000)).astype(np.int32)
    # Find all the Western years 1 in jdn
    wyears = np.unique(jdn_to_wyear(jdn))
    # Load Chinese years with wyears +/- 1
    cyears = np.unique(np.concatenate([wyears, wyears-1, wyears+1]))
    if calendar=='default':
        cyears = np.unique(np.where(cyears < cal.ybeg-1, cal.ybeg-1, np.where(cyears > cal.yend+1, cal.yend+1, cyears)))
    jd0 = np.array([int(math.floor(getJDm(y-1, 12, 31) + 0.6)) for y in cyears])
    cyearD = [calendar_func(cal, y) for y in cyears]
    if calendar=='default':
        if sum([-480==x for x in cyears])==1: cyD_m479 = chunqiu_cmonth(cal, -479)
        if sum([-221==x for x in cyears])==1: 
            cyD_m220 = guliuli_calendar_cmonth(cal, -220, 'Zhou')
            cyD_m220['reign/era'] = 'NA'
    cdate = []
    for jd in jdn:
        i = np.searchsorted(jd0, jd, 'left') - 1
        dd = jd - jd0[i]
        nday = NdaysGregJul(cyears[i])
        if (cyears[i] > cyears[0]) and (dd < cyearD[i]['cm'][0]['d']):
            i -= 1
            dd = jd - jd0[i]
        elif cyears[i] < cyears[-1]: 
            if dd >= cyearD[i+1]['cm'][0]['d'] + nday:
                i += 1
                dd = jd - jd0[i]
                if calendar=='default':
                    if cyears[i]==-479:
                        if dd > -20:
                            cdate += [chinese_date_from_table(cal, dd, jd, cyears[i], cyD_m479, calendar)]
                        else:
                            cdate += [chinese_date_from_table(cal, dd + nday, jd, cyears[i-1], cyearD[i-1], calendar)]
                        continue             
                    elif cyears[i]==-220:
                        if dd < -32:
                            cdate += [chinese_date_from_table(cal, dd + nday, jd, cyears[i-1], cyearD[i-1], calendar)]
                        else:
                            cdate += [chinese_date_from_table(cal, dd, jd, cyears[i], cyD_m220, calendar)]
                        continue
        cdate += [chinese_date_from_table(cal, dd, jd, cyears[i], cyearD[i], calendar)]
    return cdate

def chinese_date_from_table(cal, dd, jdn, cyear, cyearData, calendar, calc_western_date=True):
    """
    This is an auxiliary function to western_to_chinese_date_lookup(). It carries out the calculations required to generate the dictionary containing the information of the date in Chiense calendar.
    Input: 
      cal: the object returned by the class calendar_conversion.
      dd (int): number of days from Dec 31, y-1.
      jdn (int): Julian date at noon.
      cyear (int): indicate the Chinese year whose new year day is closest to Jan 1, cyear in the Western calendar.
      cyearData (dict): dictionary returned by function calendar_func() specified in western_to_chinese_date_lookup(). See the doc string of e.g. default_Chinese_year_data() for detail
      calendar (str): label of the Chinese calendar.
      calc_western_date: if True, it calculates the date in the Western calendar from jdn and adds it to the output dictionary.
    Return: 
      dictionary containing the information of the date in Chiense calendar.
    """
    # First calculate the easy stuff 
    week = (jdn + 1) % 7
    week = [cal.week[(jdn + 1) % 7], week] # date of week
    sex = (jdn - 11) % 60
    sex_date = [cal.stem[sex % 10] + cal.branch[sex % 12], sex+1] # sexagenary date, sexagenary number
    # sexagenary year, zodiac, sexagenary year number
    sex = (cyear + 3536) % 60
    sex_cyear = [cal.stem[sex % 10] + cal.branch[sex % 12], cal.branch_animal[sex % 12], sex+1]
    # Calculate the date in the Western calendar 
    if calc_western_date:
        wd = CalDat(jdn, 0)
        wdate = [wd['yy'], wd['mm'], wd['dd']]
        wcal = 2 
        if jdn < 2299161: wcal = 1
        if jdn < 1723980: wcal = 0
        wcal = cal.western_calendar_names[wcal] # Western calendar name

    # Chinese month
    ind = -1
    for i, cm in enumerate(cyearData['cm']):
        if dd < cm['d']:
            ind = i-1
            break
    cm = cyearData['cm'][ind]['cm']
    cymd = [cyear, cm]
    if cm < 0:
        cmonth = cal.leap + cal.cmonth[-cm-1]
    else:
        cmonth = cal.cmonth[cm-1]
    jian = cyearData['cm'][ind]['jian']

    # Chinese day
    cday = dd - cyearData['cm'][ind]['d'] + 1
    ncm = cyearData['cm'][ind]['n'] # number of days in the Chinese month
    cymd += [cday]
    cday = cal.cday[cday-1]

    # change month label in special cases
    cmonth = change_chinese_month_label(cal, cmonth, cyear, cyearData, ind, calendar)

    if jian=='NZ': 
        # add no Zhongqi label (for the ancient six and early Han calendars)
        cmonth += '(' + no_Zhongqi_label(cal.lang) + ')'

    if calc_western_date:
        cdate = {'Western ymd':wdate, 'Western calendar':wcal, 'JDN':jdn, 'Chinese ymd':cymd, 'cyear':cyear, 'cdate':cmonth+cal.cmonth_sep+cday, 'sexagenary year':sex_cyear}
    else:
        cdate = {'JDN':jdn, 'Chinese ymd':cymd, 'cyear':cyear, 'cdate':cmonth+cal.cmonth_sep+cday, 'sexagenary year':sex_cyear}
    if jian != 'NA' and jian != 'NZ': 
        jian_num = int(jian)
        jian_name = '建' if cal.lang=='ChiT' or cal.lang=='ChiS' else ''
        cdate['jian'] = [jian_name + cal.stem[(jian_num-1) % 10] + cal.branch[(jian_num-1) % 12], jian_num]
    cdate['Nday_cmonth'] = ncm
    cdate['sexagenary date'] = sex_date
    cdate['Week'] = week
    cdate['period'] = cal.period[np.searchsorted(cal.period_byear, cyear, 'right') - 1]
    if cyearData['reign/era'] != 'NA': cdate['reign/era'] = cyearData['reign/era']
    cdate['Chinese calendar'] = cyearData['calendar']
    if calendar=='default':
        if cyear==-220 and jdn < 1640703:
            period = {'Eng':'Warring States (480 BCE - 222 BCE)', 'ChiT':'戰國 (前480 - 前222)', 'ChiS':'战国 (前480 - 前222)'}
            cdate['period'] = period[cal.lang]
        if cyear==-103 and jdn < 1683608: 
            calName = {'Eng':'Qin and Early Han', 'ChiT':'秦漢顓頊曆', 'ChiS':'秦汉颛顼历'}
            cdate['Chinese calendar'] = calName[cal.lang]
        if cyear==1913 and jdn > 2420133:
            calName = {'Eng':'Republic of China', 'ChiT':'中華民國曆', 'ChiS':'中华民国历'}
            cdate['Chinese calendar'] = calName[cal.lang]
    return cdate

def default_Chinese_year_data(cal, y):
    """
    Return the Chinese year data in the default Chinese calendar in Chinese year y
    cal: calendar object returned by calendar_conversion class
    y: integer, Chinese year whose new year day is closest to Jan 1, y in the Western calendar.

    Return: dictionary with keys 'cm', 'calendar', and (optional) 'regign/era', where 
      'cm': a list containing the information of all Chinese months in the form of 
      [{'cm':m1, 'd':d1, 'jian':'jian1', n:n1}, {'cm':m2, 'd':d2, 'jian':'jian2', n:n2}, ...] 
      with 'cm' indicating the Chinese month number (negative for a leap month), 'd' indicating the number of days from Dec 31, y-1 of the first day of the Chinese month, 'jian' indicating the sexagenary month cycle associated with jian ('jian'='1' for jia zi, '2' for yi chou, ... '60' for gui hai, 'NA' for leap month, 'NZ' for a month not containing a major solar term (only for the ancient six calendars)), and 'n' indicating the number of days in the Chinese month. The list is sorted in ascending order in values in 'd'.

      'calendar' (str): version of the Chinese calendar (e.g. 'Santong', 'Shixian').

      'reign/era' (str, optional): reign and/or era name of the Chinese year (only for calendars before 1912).
    """
    if y != math.floor(y):
        raise ValueError('y must be an integer')
    if y < cal.ybeg-1 or y > cal.yend+1:
        raise ValueError('y must be in ['+str(cal.ybeg-1)+','+str(cal.yend+1)+']')
    y = int(y)

    if y < -479: 
        # use Chunqiu calendar
        return chunqiu_cmonth(cal, y)
    if y < -220:
        # use Zhou calendar
        return guliuli_calendar_cmonth(cal, y, 'Zhou')
    if y < -103:
        # use Qin and Early Han calendar 
        return QinEarlyHan_calendar_cmonth(cal, y)

    cm = list(cal.calData[y - cal.ybeg_default + 1]) 
    jian = sexagenary_month_from_cyear_jian(y)
    nmonths = 12 + (0 if cm[13]==0 else 1)
    cmonth = [{'cm':i+1, 'd':cm[i], 'jian':jian[i]} for i in range(nmonths)] 
    # This is for the calculation of the number of days in the last Chinese months
    # The number 390 for y = cal.yend+1 shouldn't matter. It can be set to other numbers.
    cmonth += [390] if y==cal.yend+1 else [cal.calData[y - cal.ybeg_default + 2][0] + NdaysGregJul(y)] 
    if cm[13] != 0:
        cmonth[12]['cm'] = -cm[13]
    cmonth = default_Chinese_year_special_years(cal, y, cmonth)
    ccal_name = cal.dcal_names[np.searchsorted(cal.dcal_years, y, 'right') - 1]
    cyear = {'cm':cmonth, 'reign/era':'NA', 'calendar':ccal_name}
    if y < 1912:
        cyear['reign/era'] = era_name_lookup(cal.lang, y, 'default')
    return cyear

def default_Chinese_year_special_years(cal, y, cmonth):
    """
    handle special years in the default calendar
    """
    if y==-103:
        cm = cal.calData[y - cal.ybeg_default][9:12] - 366
        jian = sexagenary_month_from_cyear_jian(y-1)[9:12]
        cmonth = [{'cm':i+10, 'd':cm[i], 'jian':jian[i]} for i in range(3)]
        cm = cal.calData[-103 - cal.ybeg_default + 1][:12]
        jian = sexagenary_month_from_cyear_jian(y)
        cmonth += [{'cm':i+1, 'd':cm[i], 'jian':jian[i]} for i in range(12)] + [407]
    elif y==8:
        # skip the last month
        cmonth = [cmonth[i] for i in range(13) if i != 11] + [381]
    elif y > 8 and y < 24:
        # Xin dynasty, set jian chou as the first month
        cm = cal.calData[y - cal.ybeg_default][11] - NdaysGregJul(y-1)
        cm = np.append(cm, cal.calData[y - cal.ybeg_default + 1])
        jian = [sexagenary_month_from_cyear_jian(y-1)[11]] + sexagenary_month_from_cyear_jian(y)[:12] + ['NA']
        cm = np.delete(cm, 12)
        nmonths = 12 + (0 if cm[13]==0 else 1)
        if y==18: nmonths -= 1
        cmonth = [{'cm':i+1, 'd':cm[i], 'jian':jian[i]} for i in range(nmonths)]
        if y != 18 and cm[13] != 0:
            cmonth[12]['cm'] = -cm[13]-1
        if y==19: 
            cmonth += [{'cm':-1, 'd':25, 'jian':'NA'}]
        if y==23: 
            cmonth += [{'cm':12, 'd':365, 'jian':jian[12]}]
        # for the calculation of the number of days in the last Chinese month
        cm1 = [370, 389, 378, 367, 385, 375, 364, 383, 371, 361, 379, 369, 387, 376, 395]
        cmonth += [cm1[y-9]]
    elif y==237:
        # Wei Mingdi changed the month order according to the Yin standard
        # months 3-11 were relabelled as 4-12
        cm = list(cal.calData[y - cal.ybeg_default + 1])
        jian = sexagenary_month_from_cyear_jian(y)
        cmonth = [{'cm':i+1, 'd':cm[i], 'jian':jian[i]} for i in range(2)] + [{'cm':i+2, 'd':cm[i], 'jian':jian[i]} for i in range(2,11)] + [368]
    elif y==238:
        # set chou as the beginning month
        cm = cal.calData[y - cal.ybeg_default][11] - NdaysGregJul(y-1)
        cm = np.append(cm, cal.calData[y - cal.ybeg_default + 1])
        jian = [sexagenary_month_from_cyear_jian(y-1)[11]] + sexagenary_month_from_cyear_jian(y)[:12] + ['NA']
        cm = np.delete(cm, 12)
        cmonth = [{'cm':i+1, 'd':cm[i], 'jian':jian[i]} for i in range(13)] + [387]
        cmonth[12]['cm'] = -11
    elif y==239:
        # revert to the Xia standard
        cm = cal.calData[y - cal.ybeg_default][11] - NdaysGregJul(y-1)
        cm = np.append(cm, cal.calData[y - cal.ybeg_default + 1])
        jian = [sexagenary_month_from_cyear_jian(y-1)[11]] + sexagenary_month_from_cyear_jian(y)
        cmonth = [{'cm':i+1, 'd':cm[i], 'jian':jian[i]} for i in range(13)] + [406]
        cmonth[12]['cm'] = 12
    elif y==689:
        # Empress Consort Wu designated the zǐ month (month 11) as the first month of the following year. 
        # So we have to remove the last two months.
        cmonth = [cmonth[i] for i in range(13) if i != 10 and i != 11] + [352]
    elif y > 689 and y < 701:
        # set the zi month (month 11) as the first month; keep the month label; just change the starting month
        cm = cal.calData[y - cal.ybeg_default][10:12] - NdaysGregJul(y-1)
        jian = sexagenary_month_from_cyear_jian(y-1)[10:12]
        cmonth = [{'cm':i+11, 'd':cm[i], 'jian':jian[i]} for i in range(2)]
        cm = list(cal.calData[y - cal.ybeg_default + 1])
        jian = sexagenary_month_from_cyear_jian(y)
        ie = 12 if y==700 else 10
        cmonth += [{'cm':i+1, 'd':cm[i], 'jian':jian[i]} for i in range(ie)]
        if cm[13] != 0:
            cmonth += [{'cm':-cm[13], 'd':cm[12], 'jian':'NA'}]
        # for the calculation of the number of days in the last Chinese month
        cm1 = [340, 330, 349, 337, 327, 346, 335, 354, 342, 331, 410]
        cmonth += [cm1[y-690]]
    elif y==761:
        # Tang Suzhong designated the zǐ month as the first month in the following year, so need to 
        # remove the last two months
        cmonth = [cmonth[i] for i in range(10)] + [336]
    elif y==762:
        cm = cal.calData[y - cal.ybeg_default][10:12] - NdaysGregJul(y-1)
        jian = sexagenary_month_from_cyear_jian(y-1)[10:12]
        cmonth = [{'cm':i+1, 'd':cm[i], 'jian':jian[i]} for i in range(2)]
        cm = list(cal.calData[y - cal.ybeg_default + 1])
        jian = sexagenary_month_from_cyear_jian(y)
        cmonth += [{'cm':i+3, 'd':cm[i], 'jian':jian[i]} for i in range(3)] + [{'cm':i+1, 'd':cm[i], 'jian':jian[i]} for i in range(3, 12)] + [384]
    
    cmonth = sorted(cmonth[:-1], key=lambda k: k['d']) + [{'d':cmonth[-1]}]
    for i in range(len(cmonth)-1):
        cmonth[i]['n'] = cmonth[i+1]['d'] - cmonth[i]['d']
    return cmonth[:-1]

def add_additional_calendars(cal, y, dd, jdn, cdate):
    """
    Add additional calendars to the default calendar
    """
    cdate = [cdate]
    if y < -479:
        # add Zhou, Yin and Xia (Z1 version) calendars
        lis = ['Zhou', 'Yin', 'Xia2']
        for li in lis:
            cal_func = lambda cal, y: guliuli_calendar_cmonth(cal, y, li)
            cdate += [western_to_chinese_date_lookup(cal, y, dd, jdn, li, cal_func)]
        return cdate
        
    if y < -221:
        # add Lu, Huangdi, Yin, Xia (Z11 version) and Zhuanxu calendars
        lis = ['Lu', 'Huangdi', 'Yin', 'Xia1', 'Zhanxu']
        for li in lis:
            cal_func = lambda cal, y: guliuli_calendar_cmonth(cal, y, li)
            cdate += [western_to_chinese_date_lookup(cal, y, dd, jdn, li, cal_func)]
        return cdate
        
    if y >= 221 and y <= 263:
        # add Shu calendar
        cdate += [western_to_chinese_date_lookup(cal, y, dd, jdn, 'Shu', Shu_year_data)]
    
    if y >= 222 and y <= 280:
        # add Wu calendar
        cdate += [western_to_chinese_date_lookup(cal, y, dd, jdn, 'Wu', Wu_year_data)]

    if y >= 384 and y <= 417:
        # Later Qin
        cdate += [western_to_chinese_date_lookup(cal, y, dd, jdn, 'LaterQin', LaterQin_year_data)]

    if y >= 412 and y <= 439:
        # Northern Liang
        cdate += [western_to_chinese_date_lookup(cal, y, dd, jdn, 'NorthernLiang', NorthernLiang_year_data)]

    if y >= 398 and y <= 589:
        # Northern Wei, Western Wei, Northern Zhou and Sui
        cdate += [western_to_chinese_date_lookup(cal, y, dd, jdn, 'WeiZhouSui', WeiZhouSui_year_data)]

    if y >= 534 and y <= 577:
        # Eastern Wei and Northern Qi
        cdate += [western_to_chinese_date_lookup(cal, y, dd, jdn, 'WeiQi', WeiQi_year_data)]

    if y >= 947 and y <= 1279:
        # Liao, Jin and Mongol/Yuan
        cdate += [western_to_chinese_date_lookup(cal, y, dd, jdn, 'LiaoJinYuan', LiaoJinMongol_year_data)]

    if y >= 1645 and y <= 1683:
        # Southern Ming and Zheng
        cdate += [western_to_chinese_date_lookup(cal, y, dd, jdn, 'SouthernMing', SouthernMing_year_data)]

    return cdate

def Shu_year_data(cal, y):
    """
    Return the Chinese year data used in the Shu state in the Three Kingdoms period (221-263).
    cal: calendar object returned by calendar_conversion class
    y: integer, Chinese year whose new year day is closest to Jan 1, y in the Western calendar.

    Return: dictionary with keys 'cm', 'calendar', and 'regign/era', where 
      'cm': a list containing the information of all Chinese months in the form of [{'cm':m1, 'd':d1, 'jian':'jian1'}, {'cm':m2, 'd':d2, 'jian':'jian2'}, ...] with 'cm' indicating the Chinese month number (negative for a leap month), 'd' indicating the number of days from Dec 31, y-1 of the first day of the Chinese month, and 'jian' indicating the sexagenary month cycle associated with jian ('jian'='1' for jia zi, '2' for yi chou, ... '60' for gui hai, 'NA' for a leap month. The list is sorted in ascending order in values in 'd'.

      'calendar' (str): version of the Chinese calendar, which is 'Sifen' in this case.

      'reign/era' (str): reign and/or era name of the Chinese year.
    """
    return pingshou_noZhongqi_cmonth(cal, y, 'Sifen', 'Shu')

def Wu_year_data(cal, y):
    """
    Return the Chinese year data used in the Wu state in the Three Kingdoms period (222-280).
    cal: calendar object returned by calendar_conversion class
    y: integer, Chinese year whose new year day is closest to Jan 1, y in the Western calendar.

    Return: dictionary with keys 'cm', 'calendar', and 'regign/era', where 
      'cm': a list containing the information of all Chinese months in the form of [{'cm':m1, 'd':d1, 'jian':'jian1'}, {'cm':m2, 'd':d2, 'jian':'jian2'}, ...] with 'cm' indicating the Chinese month number (negative for a leap month), 'd' indicating the number of days from Dec 31, y-1 of the first day of the Chinese month, and 'jian' indicating the sexagenary month cycle associated with jian ('jian'='1' for jia zi, '2' for yi chou, ... '60' for gui hai, 'NA' for a leap month. The list is sorted in ascending order in values in 'd'.

      'calendar' (str): version of the Chinese calendar, which is 'Sifen' (y <= 222) or 'Qianxiang' (y > 222).

      'reign/era' (str): reign and/or era name of the Chinese year.
    """
    li = 'Sifen' if y < 222.5 else 'Qianxiang'
    cyear = pingshou_noZhongqi_cmonth(cal, y, li, 'Wu')
    # Manually correct the dates in N_{244} month 12 and N_{247} month 9
    # No problem in the transition years
    if y==244:
        cyear['cm'][12]['d'] += 1
        cyear['cm'][11]['n'] += 1
        cyear['cm'][12]['n'] -= 1
    elif y==247:
        cyear['cm'][8]['d'] -= 1
        cyear['cm'][7]['n'] -= 1
        cyear['cm'][8]['n'] += 1
    return cyear

def LaterQin_year_data(cal, y):
    """
    Return the Chinese year data used in the Later Qin state in 384-417.
    cal: calendar object returned by calendar_conversion class
    y: integer, Chinese year whose new year day is closest to Jan 1, y in the Western calendar.

    Return: dictionary with keys 'cm', 'calendar', and 'regign/era', where 
      'cm': a list containing the information of all Chinese months in the form of [{'cm':m1, 'd':d1, 'jian':'jian1'}, {'cm':m2, 'd':d2, 'jian':'jian2'}, ...] with 'cm' indicating the Chinese month number (negative for a leap month), 'd' indicating the number of days from Dec 31, y-1 of the first day of the Chinese month, and 'jian' indicating the sexagenary month cycle associated with jian ('jian'='1' for jia zi, '2' for yi chou, ... '60' for gui hai, 'NA' for a leap month. The list is sorted in ascending order in values in 'd'.

      'calendar' (str): version of the Chinese calendar, which is 'Sanji' in this case.

      'reign/era' (str): reign and/or era name of the Chinese year.
    """
    return pingshou_noZhongqi_cmonth(cal, y, 'Sanji', 'LaterQin')

def NorthernLiang_year_data(cal, y):
    """
    Return the Chinese year data used in the Later Northern Liang state in 411-439.
    cal: calendar object returned by calendar_conversion class
    y: integer, Chinese year whose new year day is closest to Jan 1, y in the Western calendar.

    Return: dictionary with keys 'cm', 'calendar', and 'regign/era', where 
      'cm': a list containing the information of all Chinese months in the form of [{'cm':m1, 'd':d1, 'jian':'jian1'}, {'cm':m2, 'd':d2, 'jian':'jian2'}, ...] with 'cm' indicating the Chinese month number (negative for a leap month), 'd' indicating the number of days from Dec 31, y-1 of the first day of the Chinese month, and 'jian' indicating the sexagenary month cycle associated with jian ('jian'='1' for jia zi, '2' for yi chou, ... '60' for gui hai, 'NA' for a leap month. The list is sorted in ascending order in values in 'd'.

      'calendar' (str): version of the Chinese calendar, which is 'Sanji' in this case.

      'reign/era' (str): reign and/or era name of the Chinese year.
    """
    cyear = pingshou_noZhongqi_cmonth(cal, y, 'Xuanshi', 'NorthernLiang')
    if y==430:
        # correct the data in month 2
        cyear['cm'][1]['d'] += 1
        cyear['cm'][0]['n'] += 1
        cyear['cm'][1]['n'] -= 1
    return cyear

def WeiZhouSui_year_data(cal, y):
    """
    Return the Chinese year data used in Northern Wei, Western Wei, Northern Zhou and Sui states in 386-590.
    cal: calendar object returned by calendar_conversion class
    y: integer, Chinese year whose new year day is closest to Jan 1, y in the Western calendar.

    Return: dictionary with keys 'cm', 'calendar', and 'regign/era', where 
      'cm': a list containing the information of all Chinese months in the form of [{'cm':m1, 'd':d1, 'jian':'jian1'}, {'cm':m2, 'd':d2, 'jian':'jian2'}, ...] with 'cm' indicating the Chinese month number (negative for a leap month), 'd' indicating the number of days from Dec 31, y-1 of the first day of the Chinese month, and 'jian' indicating the sexagenary month cycle associated with jian ('jian'='1' for jia zi, '2' for yi chou, ... '60' for gui hai, 'NA' for a leap month. The list is sorted in ascending order in values in 'd'.

      'calendar' (str): version of the Chinese calendar.

      'reign/era' (str): reign and/or era name of the Chinese year.
    """
    if y < 451.5:
        li = 'Jingchu'
    elif y < 522.5:
        li = 'Xuanshi'
    elif y < 558.5:
        li = 'Zhengguang'
    elif y < 565.5:
        li = 'fakeMingKeRang'
    elif y < 578.5:
        li = 'Tianhe'
    elif y < 583.5:
        li = 'Daxiang'
    else:
        li = 'Kaihuang'
    cyear = pingshou_noZhongqi_cmonth(cal, y, li, 'WeiZhouSui')
    if y==430:
        # correct the data in month 2
        cyear['cm'][1]['d'] += 1
        cyear['cm'][0]['n'] += 1
        cyear['cm'][1]['n'] -= 1
    # transition year
    if y==565:
        # Mingkerang -> Tianhe, the other transition years are fine
        cyear['cm'][-1]['n'] += 1
    return cyear

def WeiQi_year_data(cal, y):
    """
    Return the Chinese year data used in Eastern Wei, and Northern Qi states in 534-577.
    cal: calendar object returned by calendar_conversion class
    y: integer, Chinese year whose new year day is closest to Jan 1, y in the Western calendar.

    Return: dictionary with keys 'cm', 'calendar', and 'regign/era', where 
      'cm': a list containing the information of all Chinese months in the form of [{'cm':m1, 'd':d1, 'jian':'jian1'}, {'cm':m2, 'd':d2, 'jian':'jian2'}, ...] with 'cm' indicating the Chinese month number (negative for a leap month), 'd' indicating the number of days from Dec 31, y-1 of the first day of the Chinese month, and 'jian' indicating the sexagenary month cycle associated with jian ('jian'='1' for jia zi, '2' for yi chou, ... '60' for gui hai, 'NA' for a leap month. The list is sorted in ascending order in values in 'd'.

      'calendar' (str): version of the Chinese calendar.

      'reign/era' (str): reign and/or era name of the Chinese year.
    """
    # transition between calendars are fine, no need for adjustment
    if y < 539.5:
        li = 'Zhengguang'
    elif y < 550.5:
        li = 'Xinghe'
    else:
        li = 'Tianbao'
    return pingshou_noZhongqi_cmonth(cal, y, li, 'WeiQi')

def LiaoJinMongol_year_data(cal, y):
    """
    Return the Chinese year data used in Liao, Jin and Mongol/Yuan states in 947-1279.
    cal: calendar object returned by calendar_conversion class
    y: integer, Chinese year whose new year day is closest to Jan 1, y in the Western calendar.

    Return: dictionary with keys 'cm', 'calendar', and 'regign/era', where 
      'cm': a list containing the information of all Chinese months in the form of [{'cm':m1, 'd':d1, 'jian':'jian1'}, {'cm':m2, 'd':d2, 'jian':'jian2'}, ...] with 'cm' indicating the Chinese month number (negative for a leap month), 'd' indicating the number of days from Dec 31, y-1 of the first day of the Chinese month, and 'jian' indicating the sexagenary month cycle associated with jian ('jian'='1' for jia zi, '2' for yi chou, ... '60' for gui hai, 'NA' for a leap month. The list is sorted in ascending order in values in 'd'.

      'calendar' (str): version of the Chinese calendar.

      'reign/era' (str): reign and/or era name of the Chinese year.
    """
    # Correction for the Liao, Jun, Mongol/Yuan calendars in 947-1279. The default calendar data in
    # 'default_calendar_M105_2201.csv' are stored in a 2D array when loaded to cal.calData[][] 
    # with the first column removed. cal.calData[] is thus a 1D array of length 14 storing the 
    # calendar info in a particular Chinese year y. The array stores month 1 conjunction date, 
    # month 2 conjunction date, ..., month 12 conj. date, leap month conj. date, and leap month number. 
    # The variable corrections is a list of dictionaries with keys 'yxxxx' containing the correction 
    # to cal.calData[] in order to convert it to the calendar in Liao, Jin or Mongol/Yuan dynasty. 
    # Take the key 'y1270' as an example. It contains the array [11,319,13,349,14,11]. It means that 
    # in the Chinese year 1270, cal.calData[] needs to be modified according to 
    # cal.calData[k][10]=319, cdate[k][12]=349, and cdate[k][13]=11. Here k denotes the index 
    # in the array cal.calData[][] corresponding to the Chinese year 1270. The off by one index 
    # results from the fact that cal.calData[][] removes the first column in 'default_calendar_M105_2201.csv'. 
    # Also, column 16 of 'default_calendar_M105_2201.csv', which indicates the total number of days in the 
    # Chinese year, is not loaded to cal.calData[][], and so index 15 has been removed in the corrections 
    # variable.
    corrections = {'y949':[10,298], 'y955':[8,232], 'y958':[9,288], 'y959':[12,366], 'y961':[3,78], 'y964':[4,135,6,195,7,224], 'y965':[5,153], 'y973':[4,125], 'y985':[9,290,13,260,14,8], 'y986':[2,72,7,220], 'y994':[1,44], 'y999':[4,109,13,138,14,4], 'y1001':[1,27,10,292,12,381,13,352,14,11], 'y1012':[3,86], 'y1015':[7,200,13,229,14,7], 'y1020':[5,147], 'y1021':[12,370], 'y1024':[12,369], 'y1025':[7,209], 'y1029':[3,77,13,107,14,3], 'y1039':[6,176], 'y1040':[5,165,12,371], 'y1044':[11,328], 'y1045':[3,81], 'y1049':[12,361], 'y1053':[2,53], 'y1056':[6,198], 'y1059':[4,134,6,194,12,371], 'y1064':[6,170,13,199,14,6], 'y1070':[8,251], 'y1073':[5,160], 'y1075':[1,19], 'y1077':[13,382,14,12], 'y1078':[1,46,13,0,14,0], 'y1080':[9,290,13,260,14,8], 'y1094':[1,20], 'y1102':[10,317], 'y1103':[8,247], 'y1105':[3,77,13,107,14,3], 'y1113':[10,315], 'y1121':[9,287], 'y1129':[4,111], 'y1134':[12,352], 'y1145':[11,321], 'y1147':[3,93,7,211], 'y1152':[4,128], 'y1155':[9,272], 'y1163':[8,244], 'y1168':[10,307], 'y1176':[1,44], 'y1178':[10,315], 'y1184':[9,281], 'y1198':[11,335], 'y1207':[5,148,11,325], 'y1209':[1,38], 'y1239':[8,242], 'y1250':[4,123], 'y1251':[4,112,7,201,11,349], 'y1252':[1,42], 'y1253':[9,267], 'y1256':[7,205], 'y1258':[8,242,12,360], 'y1263':[2,71,10,307,11,337], 'y1270':[11,319,13,349,14,11], 'y1273':[6,167], 'y1276':[2,47]}
    cm = list(cal.calData[y - cal.ybeg_default + 1])
    k = 'y'+str(y)
    if k in corrections:
        corr_array = corrections[k]
        n = len(corr_array)
        for i in range(0, n, 2):
            cm[corr_array[i]-1] = corr_array[i+1]
    jian = sexagenary_month_from_cyear_jian(y)
    nmonths = 12 + (0 if cm[13]==0 else 1)
    cmonth = [{'cm':i+1, 'd':cm[i], 'jian':jian[i]} for i in range(nmonths)]
    if cm[13] != 0:
        cmonth[12]['cm'] = -cm[13]
    # for the calculation of the number of days in the last Chinese months
    cm1 = cal.calData[y - cal.ybeg_default + 2][0] + NdaysGregJul(y)
    if y==993 or y==1000 or y==1074 or y==1251:
        cm1 -= 1
    elif y==1077:
        cm1 = 411
    elif y==1093 or y==1175 or y==1208:
        cm1 += 1
    cmonth = sorted(cmonth, key=lambda k: k['d']) + [{'d':cm1}]
    for i in range(len(cmonth)-1):
        cmonth[i]['n'] = cmonth[i+1]['d'] - cmonth[i]['d']
    if y < 994:
        ccal_name = {'Eng':'Tiaoyuan', 'ChiT':'調元曆', 'ChiS':'调元历'}
    elif y < 1137:
        ccal_name = {'Eng':'Jiajun Daming', 'ChiT':'賈俊大明曆', 'ChiS':'贾俊大明历'}
    elif y < 1182:
        ccal_name = {'Eng':'Yangji Daming', 'ChiT':'楊級大明曆', 'ChiS':'杨级大明历'}
    elif y < 1281:
        ccal_name = {'Eng':'Revised Daming', 'ChiT':'重修大明曆', 'ChiS':'重修大明历'}
    elif y < 1368:
        ccal_name = {'Eng':'Shoushi', 'ChiT':'授時曆', 'ChiS':'授时历'}
    else:
        ccal_name = {'Eng':'NA', 'ChiT':'NA', 'ChiS':'NA'}
    return {'cm':cmonth[:-1], 
            'reign/era':era_name_lookup(cal.lang, y, 'LiaoJinYuan'), 
            'calendar':ccal_name[cal.lang]}

def SouthernMing_year_data(cal, y):
    """
    Return the Chinese year data used in the Southern Ming and Zheng dynasties in 1645-1683.
    cal: calendar object returned by calendar_conversion class
    y: integer, Chinese year whose new year day is closest to Jan 1, y in the Western calendar.

    Return: dictionary with keys 'cm', 'calendar', and 'regign/era', where 
      'cm': a list containing the information of all Chinese months in the form of [{'cm':m1, 'd':d1, 'jian':'jian1'}, {'cm':m2, 'd':d2, 'jian':'jian2'}, ...] with 'cm' indicating the Chinese month number (negative for a leap month), 'd' indicating the number of days from Dec 31, y-1 of the first day of the Chinese month, and 'jian' indicating the sexagenary month cycle associated with jian ('jian'='1' for jia zi, '2' for yi chou, ... '60' for gui hai, 'NA' for a leap month. The list is sorted in ascending order in values in 'd'.

      'calendar' (str): version of the Chinese calendar, which is Canming Datong in this case.

      'reign/era' (str): reign and/or era name of the Chinese year.
    """
    # calendar data for the Southern Ming and Zheng dynasties in 1644-1684
    calData = [[39, 69, 98, 127, 157, 186, 215, 245, 275, 304, 334, 364, 0, 0], [28, 57, 87, 116, 145, 175, 233, 263, 292, 322, 352, 382, 204, 6], [47, 76, 106, 135, 164, 194, 223, 252, 282, 311, 341, 371, 0, 0], [36, 65, 95, 125, 154, 183, 213, 242, 271, 301, 330, 360, 0, 0], [25, 54, 84, 143, 173, 202, 232, 261, 290, 320, 349, 379, 114, 3], [42, 72, 102, 131, 161, 191, 220, 250, 279, 308, 338, 367, 0, 0], [32, 61, 91, 121, 150, 180, 209, 239, 269, 298, 328, 386, 357, 11], [51, 80, 110, 139, 169, 198, 228, 258, 287, 317, 347, 376, 0, 0], [41, 70, 99, 129, 158, 188, 217, 247, 276, 306, 336, 366, 0, 0], [29, 59, 88, 117, 147, 176, 205, 264, 294, 324, 354, 384, 235, 7], [48, 78, 107, 136, 166, 195, 224, 254, 283, 313, 343, 373, 0, 0], [37, 67, 97, 126, 155, 185, 214, 243, 273, 302, 332, 362, 0, 0], [26, 56, 86, 115, 145, 204, 233, 262, 292, 321, 351, 380, 174, 5], [44, 74, 104, 133, 163, 192, 222, 251, 280, 310, 339, 369, 0, 0], [33, 63, 93, 122, 152, 182, 211, 241, 270, 299, 329, 358, 0, 0], [23, 82, 111, 141, 171, 200, 230, 259, 289, 318, 348, 377, 52, 1], [42, 71, 101, 130, 160, 189, 219, 249, 278, 308, 337, 367, 0, 0], [30, 60, 89, 119, 148, 177, 207, 237, 266, 296, 355, 385, 326, 10], [50, 79, 108, 138, 167, 196, 226, 255, 285, 315, 345, 374, 0, 0], [39, 69, 98, 127, 157, 186, 215, 245, 274, 304, 334, 363, 0, 0], [28, 58, 87, 117, 146, 176, 234, 264, 293, 323, 352, 382, 205, 6], [46, 76, 105, 135, 164, 194, 223, 252, 282, 311, 341, 370, 0, 0], [35, 65, 94, 124, 154, 183, 213, 242, 271, 301, 330, 360, 0, 0], [24, 54, 83, 113, 172, 202, 231, 261, 290, 320, 349, 379, 143, 4], [43, 73, 102, 132, 161, 191, 221, 250, 280, 309, 339, 368, 0, 0], [32, 61, 91, 120, 150, 179, 209, 238, 268, 298, 327, 357, 386, 12], [51, 80, 110, 139, 168, 198, 227, 257, 287, 317, 346, 376, 0, 0], [41, 70, 99, 129, 158, 187, 217, 246, 276, 306, 335, 365, 0, 0], [30, 59, 89, 118, 148, 177, 206, 236, 295, 324, 354, 384, 265, 8], [48, 77, 107, 136, 166, 195, 224, 254, 283, 313, 342, 372, 0, 0], [37, 66, 96, 126, 155, 184, 214, 243, 272, 302, 331, 361, 0, 0], [26, 55, 85, 115, 145, 174, 233, 262, 292, 321, 351, 380, 204, 6], [45, 74, 104, 134, 163, 193, 222, 252, 281, 311, 340, 370, 0, 0], [33, 63, 92, 122, 151, 181, 211, 240, 270, 299, 329, 358, 0, 0], [23, 52, 111, 140, 170, 200, 229, 259, 289, 318, 348, 377, 82, 2], [42, 71, 101, 130, 159, 189, 218, 248, 278, 307, 337, 367, 0, 0], [31, 61, 90, 120, 149, 178, 208, 237, 267, 296, 356, 386, 326, 10], [49, 79, 108, 138, 167, 196, 226, 255, 284, 314, 344, 374, 0, 0], [38, 68, 98, 127, 157, 186, 215, 245, 274, 303, 333, 363, 0, 0], [27, 57, 87, 117, 146, 176, 234, 264, 293, 322, 352, 382, 205, 6], [46, 76, 106, 135, 165, 194, 224, 253, 283, 312, 341, 371, 0, 0]]
    if y < 1644 or y > 1684:
        cm = list(cal.calData[y - cal.ybeg_default + 1])
        cm1 = cal.calData[y - cal.ybeg_default + 1][0] + NdaysGregJul(y)
    else:
        cm = calData[y - 1644]
        cm1 = 401 if y==1684 else calData[y-1643][0] + NdaysGregJul(y)
    jian = sexagenary_month_from_cyear_jian(y)
    nmonths = 12 + (0 if cm[13]==0 else 1)
    cmonth = [{'cm':i+1, 'd':cm[i], 'jian':jian[i]} for i in range(nmonths)]
    if cm[13] != 0:
        cmonth[12]['cm'] = -cm[13]
    cmonth = sorted(cmonth, key=lambda k: k['d']) + [{'d':cm1}]
    for i in range(len(cmonth)-1):
        cmonth[i]['n'] = cmonth[i+1]['d'] - cmonth[i]['d']
    ccal_name = {'Eng':'Canming Datong', 'ChiT':'殘明大統曆', 'ChiS':'残明大统历'}
    return {'cm':cmonth[:-1], 
            'reign/era':era_name_lookup(cal.lang, y, 'SouthernMing'), 
            'calendar':ccal_name[cal.lang]}

def GBT33661_2017_sui(cal, y, ephemeris, offset=0):
    """
    Computer the Chinese months in sui y for GB/T 33661-2017
    Input: 
      cal: calendar object returned by calendar_conversion class
      y: integer, Chinese year whose new year day is closest to Jan 1, y in the Western calendar.
      ephemeris (str): ephemeris for conjunctions and solar terms (either 'DE431' or 'DE441')
      offset (int): integer added to the number of days counted from Dec 31, y-1. This parameter allows user to change the reference date of which days are counted from.
    Return:
      list [{'cm':m1, 'd':d1, 'jian':'jian1', n:n1}, {'cm':m2, 'd':d2, 'jian':'jian2', n:n2}, ...] with 'cm' indicating the Chinese month number (negative for a leap month), 'd' indicating the number of days from Dec 31, y-1 of the first day of the Chinese month, 'jian' indicating the sexagenary month cycle associated with jian ('jian'='1' for jia zi, '2' for yi chou, ... '60' for gui hai, 'NA' for a leap month, and 'n' indicating the number of days in the Chinese month. The list is sorted in ascending order in values in 'd'.
    """
    ephemeris = cal.set_ephemeris(ephemeris)
    if y < cal.sm.ybeg-1 or y > cal.sm.yend+1:
        raise ValueError('Requested year out of range.')
    sc =  cal.sm.smData[int(y) - cal.sm.ybeg + 1]
    jd0 = sc[0]
    # extract the dates of middle solar terms (st) and conjunctions (cj)
    st = np.array([int(math.floor(x - get_dTT_UT(jd0 + x, cal.sm.dalpha))) for x in sc[range(1,26,2)]]) + int(offset)
    cj = np.array([int(math.floor(x - get_dTT_UT(jd0 + x, cal.sm.dalpha))) for x in sc[range(26,85,4)]]) + int(offset)
    ibeg = np.searchsorted(cj, st[0], 'right') - 1
    iend = np.searchsorted(cj, st[-1], 'right') - 1
    find_leap = (iend - ibeg == 13)
    m = 10
    cmonth = []
    cyear_stem = (y + 700005) % 10 # stem number of Chinese year y-1
    jian1 = (12*cyear_stem + 11) % 60 # jian - 1 of month 10 in y-1
    for i in range(ibeg, iend):
        if find_leap:
            qi = st[np.searchsorted(st, cj[i], 'left')]
            if qi >= cj[i+1]:
                find_leap = False
                cmonth += [{'cm':-m, 'd':cj[i], 'jian':'NA', 'n':cj[i+1]-cj[i]}]
                continue
        m += 1
        if m > 12: m -= 12
        jian1 = (jian1 + 1) % 60
        cmonth += [{'cm':m, 'd':cj[i], 'jian':str(jian1+1), 'n':cj[i+1]-cj[i]}]
    return cmonth

def GBT33661_2017_cmonth(cal, y, ephemeris):
    """
    Computer the Chinese months in Chinese year y for GB/T 33661-2017
    Input:
      cal: calendar object returned by calendar_conversion class
      y: integer, Chinese year whose new year day is closest to Jan 1, y in the Western calendar.
      ephemeris (str): ephemeris for conjunctions and solar terms (either 'DE431' or 'DE441')
    Return: dictionary with keys 'cm' and 'calendar', where 
      'cm': a list containing the information of all Chinese months in the form of 
      [{'cm':m1, 'd':d1, 'jian':'jian1', n:n1}, {'cm':m2, 'd':d2, 'jian':'jian2', n:n2}, ...] 
      with 'cm' indicating the Chinese month number (negative for a leap month), 'd' indicating the number of days from Dec 31, y-1 of the first day of the Chinese month, 'jian' indicating the sexagenary month cycle associated with jian ('jian'='1' for jia zi, '2' for yi chou, ... '60' for gui hai, 'NA' for leap month, 'NZ' for a month not containing a major solar term (only for the ancient six calendars)), and 'n' indicating the number of days in the Chinese month. The list is sorted in ascending order in values in 'd'.

      'calendar' (str): version of the Chinese calendar, which is 'GB/T 33661-2017'.
      'reign/era' (str): 'NA' for this calendar
    """
    cmonth1 = GBT33661_2017_sui(cal, y, ephemeris)
    cmonth2 = GBT33661_2017_sui(cal, y+1, ephemeris, NdaysGregJul(y))
    cmonth = [x for x in cmonth1 if abs(x['cm']) < 10.5] + [x for x in cmonth2 if abs(x['cm']) > 10.5]
    calendar = {'Eng':'Purple Mountain (GB/T 33661-2017)', 'ChiT':'紫金曆 (GB/T 33661-2017)', 'ChiS':'紫金历 (GB/T 33661-2017)'}
    return {'cm':cmonth, 'calendar':calendar[cal.lang], 'reign/era':'NA'}

def GBT33661_2017_solar_terms(cal, y, ephemeris):
    """
    Retrieve calendrical solar terms J12-Z11 in Western year y for GBT33661_2017_solar_terms.
    Input: 
      cal: calendar object returned by calendar_conversion class
      y (int): Western year
      ephemeris (str): Ephemeris for the solar terms; either 'DE431' or 'DE441'. If ephemeris=='None', the default ephemeris (set by cal.default_eph) will be used.
    Return: A numpy array containing the Julian date at noon of solar terms J12-Z11
    """
    ephemeris = cal.set_ephemeris(ephemeris)
    if y < cal.sm.ybeg-1 or y > cal.sm.yend+1:
        raise ValueError('Requested year out of range.')
    sterm = cal.sm.smData[int(y) - cal.sm.ybeg + 1][0:26]
    jd0 = sterm[0]
    st = np.array([int(jd0+1) + int(math.floor(x - get_dTT_UT(jd0 + x, cal.sm.dalpha))) for x in sterm[2:]])
    return st

def calendrical_solar_terms_default(cal, y):
    """
    Retrieve calendrical solar terms J12-Z11 in Western year y for the default calendar.
    Return: A numpy array containing the Julian date at noon of solar terms J12-Z11
    """
    if y > cal.ybeg_default - 1: 
        jd0 = int(math.floor(getJDm(y-1, 12, 31)+ 0.6))
        return cal.calSterm[y - cal.ybeg_default + 1] + jd0
    elif y > -480:
        return guliuli_solar_terms(y, 'Zhou')
    else:
        # No calendarical solar term for the Chunqiu calendar
        return np.array([-9999]*24)

def calendrical_solar_terms_Wu(y):
    """
    Calculate calendrical solar terms J12-Z11 in Western year y for the Wu dynasty.
    Return: A numpy array containing the Julian date at noon of solar terms J12-Z11
    """
    li = 'Sifen' if y < 222.5 else 'Qianxiang'
    st = compute_pingqi(y, li)
    if y==223:
        # pingqi before Z1 still used Sifen almanac because they were in N_{222}
        st2 = compute_pingqi(y, 'Sifen')
        st[0:3] = st2[0:3].copy()
    return st

def calendrical_solar_terms_WeiZhouSui(y):
    """
    Calculate calendrical solar terms J12-Z11 in Western year y for the Northern Wei, Western Wei, Northern Zhou, Sui states in the Southern and Northern dynasties period.
    Return: A numpy array containing the Julian date at noon of solar terms J12-Z11
    """
    if y < 451.5:
        li = 'Jingchu'
    elif y < 522.5:
        li = 'Xuanshi'
    elif y < 558.5:
        li = 'Zhengguang'
    elif y < 565.5:
        li = 'fakeMingKeRang'
    elif y < 578.5:
        li = 'Tianhe'
    elif y < 583.5:
        li = 'Daxiang'
    else:
        li = 'Kaihuang'
    st = compute_pingqi(y, li)
    # Deal with transition years
    if y==452:
        # change J12, Z12 and J1
        st2 = compute_pingqi(y, 'Jingchu')
        st[0:3] = st2[0:3].copy()
    elif y==523:
        # change J12 and Z12
        st2 = compute_pingqi(y, 'Xuanshi')
        st[0:2] = st2[0:2].copy()
    elif y==559:
        # change J12 and Z12
        st2 = compute_pingqi(y, 'Zhengguang')
        st[0:2] = st2[0:2].copy()
    elif y==566:
        # change J12, Z12 and J1
        st2 = compute_pingqi(y, 'fakeMingKeRang')
        st[0:3] = st2[0:3].copy()
    elif y==579:
        # change J12, Z12 and J1
        st2 = compute_pingqi(y, 'Tianhe')
        st[0:3] = st2[0:3].copy()
    elif y==584:
        # change J12, Z12 and J1
        st2 = compute_pingqi(y, 'Daxiang')
        st[0:3] = st2[0:3].copy()
    return st

def calendrical_solar_terms_WeiQi(y):
    """
    Calculate calendrical solar terms J12-Z11 in Western year y for the Eastern Wei and Northern Qi states in the Southern and Northern dynasties period.
    Return: A numpy array containing the Julian date at noon of solar terms J12-Z11
    """
    if y < 539.5:
        li = 'Zhengguang'
    elif y < 550.5:
        li = 'Xinghe'
    else:
        li = 'Tianbao'
    st = compute_pingqi(y, li)
    # Deal with transition years
    if y==540:
        # change J12 and Z12
        st2 = compute_pingqi(y, 'Zhengguang')
        st[0:2] = st2[0:2].copy()
    elif y==551:
        # change J12 and Z12
        st2 = compute_pingqi(y, 'Xinghe')
        st[0:2] = st2[0:2].copy()
    return st

def calendrical_solar_terms_LiaoJinYuan(y):
    """
    Calculate calendrical solar terms J12-Z11 in Western year y for the Liao, Jin and Mongol/Yuan dynasties in 947-1279.
    Return: A numpy array containing the Julian date at noon of solar terms J12-Z11
    """
    li = 'Xuanming' if y < 1085.5 else 'RevisedDaming'
    st = compute_pingqi(y, li)
    # Correction to pingqi
    if y==999: st[9] -= 1
    if y==1015: st[15] -= 1
    if y==1029: st[7] -= 1
    if y==1064: st[13] -= 1
    if y==1067: 
        st[5] -= 1
        st[7] -= 1
    return st

def calendrical_solar_terms_SouthernMing(y):
    """
    Calculate calendrical solar terms J12-Z11 in Western year y for the Southern Ming dynasty in 1645-1683.
    Return: A numpy array containing the Julian date at noon of solar terms J12-Z11
    """
    st = compute_pingqi(y, 'Datong')
    if y==1663: st[16] -= 1   # correction to J8 in 1663
    return st

def print_Western_date_range_Chinese_year(y, cal, cm):
    """
    Given a Chinese year y (whose New Year day is closest to Jan 1, y in Western calendar) and the Chinese month information, print the range of Western dates in the Chinese year. For example, the Chinese year 2025 is from Jan 29, 2025 to Feb 16, 2026. So the output (for lang='Eng') string is 'Western Dates (Gregorian): Jan 29, 2025 - Feb 16, 2026'.
    Input:
      y (int): Chinese year y whose New Year day is closest to Jan 1, y in Western calendar.
      lang (string): language, either 'Eng', 'ChiT' or 'ChiS'.
      cal: calendar object returned by calendar_conversion class
      cm: a list of Chinese months [{'cm':m1, 'JDN':JDN1, 'jian':'jian1', 'n':n1}, {'cm':m2, 'JDN':JDN2, 'jian':'jian2', 'n':n2}, ...] with 'cm' indicating the Chinese month number (negative for a leap month), 'JDN' indicating the Julian date at noon of the first day of the Chinese month, 'jian' indicating the sexagenary month cycle associated with jian ('jian'='1' for jia zi, '2' for yi chou, ... '60' for gui hai, 'NA' for leap month, 'NZ' for a month not containing a major solar term (only for the ancient six calendars)), and 'n' indicating the number of days in the Chinese month. The list is sorted in ascending order in values in 'd'.
    """
    if 'JDN' in cm[0]:
        jd0 = cm[0]['JDN']
        jd1 = cm[-1]['JDN'] + cm[-1]['n'] - 1
    else:
        jdy = int(getJDm(y-1, 12, 31) + 0.6)
        jd0 = jdy + cm[0]['d']
        jd1 = jdy + cm[-1]['d'] + cm[-1]['n'] - 1
    date0 = CalDat(jd0)
    date1 = CalDat(jd1)
    if cal.lang=='Eng':
        html = 'Western Dates '
        if y < 8:
            html += '(Proleptic Julian): '
        elif y < 1582:
            html += '(Julian): '
        elif y==1582:
            html += '(Julian/Gregorian): '
        else:
            html += '(Gregorian): '
        html += cal.wmonthName[date0['mm']-1] + ' ' + str(date0['dd']) + ', '
        html += (str(date0['yy']) if date0['yy'] > 0 else str(1 - date0['yy'])+' BCE') + ' &ndash; '
        html += cal.wmonthName[date1['mm']-1] + ' ' + str(date1['dd']) + ', '
        html += str(date1['yy']) if date1['yy'] > 0 else str(1 - date1['yy'])+' BCE'
    elif cal.lang=='ChiT':
        html = '公曆日期 '
        if y < 8:
            html += '(逆推儒略曆): '
        elif y < 1582:
            html += '(儒略曆): '
        elif y==1582:
            html += '(儒略曆/格里曆): '
        else:
            html += '(格里曆): '
        html += (str(date0['yy']) if date0['yy'] > 0 else '前'+str(1-date0['yy'])) + '年' + str(date0['mm']) + '月' + str(date0['dd']) + '日 &ndash; '
        html += (str(date1['yy']) if date1['yy'] > 0 else '前'+str(1-date1['yy'])) + '年' + str(date1['mm']) + '月' + str(date1['dd']) + '日'
    else:
        html = '公历日期 '
        if y < 8:
            html += '(逆推儒略历): '
        elif y < 1582:
            html += '(儒略历): '
        elif y==1582:
            html += '(儒略历/格里历): '
        else:
            html += '(格里历): '
        html += (str(date0['yy']) if date0['yy'] > 0 else '前'+str(1-date0['yy'])) + '年' + str(date0['mm']) + '月' + str(date0['dd']) + '日 &ndash; '
        html += (str(date1['yy']) if date1['yy'] > 0 else '前'+str(1-date1['yy'])) + '年' + str(date1['mm']) + '月' + str(date1['dd']) + '日'
    return html

def print_Chinese_year_html(cal, y, calendar, ephemeris):
    """
    Create an HTML table showing the Chinese year whose New Year Day is closest to Jan 1, y in the Western calendar.
    Input: 
        cal: calendar object returned by calendar_conversion class
        y (int): year in the Western calendar whose Jan 1 is closest to the Chinese New Year Day .
        calender (str): version of Chinese calendar. Only support the calendars listed in available_calendars() below.
        ephemeris: ephemeris used to compute the moon phases and solar term. It's either 'DE431' or 'DE441'.
    Return: String that can be displayed nicely using HTML(string)
    """
    def add_cal_solar_term(kst, nst, st, jd0, jd1):
        """
        Helper function that adds calendrical solar terms to a column in a Chinese month
        Input:
          kst: starting index of a solar term
          nst: number of solar terms in the Chinese year
          st: list of tuples [(lab1, jdn1), (lab2, jdn2), ...] where lab1, lab2, ... are the lables of the calendrical solar terms (e.g. 'J1', 'Z4') and jdn1, jdn2, ... are the Julian dates at noon of the solar terms.
          jd0, jd1: Julian date range. Only solar terms with jd0 <= jd < jd1 will be included.
        Return: a tuple (html, k) with html being the HTML string for the solar term column and k being the first index of the solar term not included in the month.
        """
        k = kst
        jd = st[k][1]
        ist = 0 # count the number of solar terms in the Chinese month
        bstyle = ' style="border:1px solid black;border-collapse:collapse;text-align:center;">'
        html = '<td' + bstyle
        while jd >= jd0 and jd < jd1:
            ist += 1
            if ist > 1: html += '<br />'
            d = jd - jd0 + 1
            date = CalDat(jd)
            html += cal.stermName[st[k][0]] + ': '
            if cal.lang=='Eng':
                html += str(d) + ' (' + cal.wmonthName[date['mm']-1] + ' ' + str(date['dd']) + ')'
            else:
                html += cal.cday[d-1] + ' (' + str(date['mm']) + '月' + str(date['dd']) + '日' + ')'
            k += 1
            if k==nst: 
                k -= 1
                break
            jd = st[k][1]
        html += '</td>'
        return html, k
    
    def add_DE_solar_term(kst, nst, st, jd0, jd1):
        """
        Helper function that adds DE solar terms to a column in a Chinese month
        Input:
          kst: starting index of a solar term
          nst: number of solar terms in the Chinese year
          st: a list [[lab1, info1], [lab2, info2], ...] containing all solar terms in Chinese year y, where lab1, lab2, ... are the labels of the solar terms (e.g. 'J8', 'Z3') and info1, info2, ... are dictionaries containing the date and time information of the solar terms.
          jd0, jd1: Julian date range. Only solar terms with jd0 <= jdn < jd1 (jdn = Julian date at noon of the solar term) will be included.
        Return: a tuple (html, k) with html being the HTML string for the solar term column and k being the first index of the solar term not included in the month.
        """
        f5o6 = 5.0/6
        k = kst
        jdn = math.floor(st[k][1]['jd0_ut'] + st[k][1]['jd1_ut'] + f5o6)
        ist = 0 # count the number of solar terms in the Chinese month
        bstyle = ' style="border:1px solid black;border-collapse:collapse;text-align:center;">'
        html = '<td' + bstyle
        while jdn >= jd0 and jdn < jd1:
            ist += 1
            if ist > 1: html += '<br />'
            d = jdn - jd0 + 1
            html += st[k][1]['event'] + ': ' 
            if cal.lang=='Eng':
                html += str(d)
            else:
                html += cal.cday[d-1]
            html += ' (' + st[k][1]['dateString'] + ') ' + st[k][1]['timeString']
            k += 1
            if k==nst: 
                k -= 1
                break
            jdn = math.floor(st[k][1]['jd0_ut'] + st[k][1]['jd1_ut'] + f5o6)
        html += '</td>'
        return html, k
    
    # Gather the information of this Chinese year
    cy = cal.chinese_year_info(y, calendar, ephemeris)

    # Print Chinese year
    html = '<h1>'
    if cal.lang=='Eng':
        html += 'Chinese Year: '+ cal.stem[(y + 3506) % 10] + ' '+cal.branch[(y + 3512) % 12]+' ('+cal.branch_animal[(y + 3512) % 12]+') '
    elif cal.lang=='ChiT':
        html += '中曆年: '+cal.stem[(y + 3506) % 10]+cal.branch[(y + 3512) % 12]+'('+cal.branch_animal[(y + 3512) % 12]+')'
    else:
        html += '中历年: '+cal.stem[(y + 3506) % 10]+cal.branch[(y + 3512) % 12]+'('+cal.branch_animal[(y + 3512) % 12]+')'
    if cy['reign/era'] != 'NA':
        html += ' (' + cy['reign/era'] + ')'
    html += '</h1>'

    # Print Western dates
    html += '<h2>' + print_Western_date_range_Chinese_year(y, cal, cy['cm']) + '</h2>'

    # Add year info
    yinfo = addYearInfo(y, cal.lang, calendar)
    if len(yinfo) > 0 and not (calendar=='default' and y==1670) and not (calendar=='default' and y==240):
        html += '<h3 style="color:brown;line-height:130%;">' + yinfo + '</h3>'

    # Create table of all Chinese months in the year
    bstyle = ' style="border:1px solid black;border-collapse:collapse;text-align:center;">'
    html += '<br /><table' + bstyle + '<tr><th' + bstyle
    if cal.lang=='Eng':
        html += 'Chinese<br />Month</th><th' + bstyle + 'Conjunction<br />Day</th>'
        if calendar=='default' and y > 1666 and y < 1670:
            html += '<th' + bstyle + 'Xinfa Solar Term</th><th' + bstyle
            html += 'Datong Solar Term</th>'
        elif len(cy['calst']) > 0:
            html += '<th' + bstyle + 'Calendrical Solar Terms</th>'
        html += '<th' + bstyle + cal.ephemeris + ' Solar Term (UT+8)</th></tr>'
    elif cal.lang=='ChiT':
        html += '中曆月</th><th' + bstyle + '朔日</th>'
        if calendar=='default' and y > 1666 and y < 1670:
            html += '<th' + bstyle + '新法節氣</th><th' + bstyle
            html += '大統曆節氣</th>'
        elif len(cy['calst']) > 0:
            html += '<th' + bstyle + '曆書節氣</th>'
        html += '<th' + bstyle + cal.ephemeris + '節氣 (UT+8)</th>'
    else:
        html += '中历月</th><th' + bstyle + '朔日</th>'
        if calendar=='default' and y > 1666 and y < 1670:
            html += '<th' + bstyle + '新法节气</th><th' + bstyle
            html += '大统历节气</th>'
        elif len(cy['calst']) > 0:
            html += '<th' + bstyle + '历书节气</th>'
        html += '<th' + bstyle + cal.ephemeris + '节气 (UT+8)</th>'
    html += '</tr>'
    # set counter to keep track of the solar term indices
    kcalst = 0; kdatongst = 0; kst = 0;
    ncalst = len(cy['calst']); ndatongst = len(cy['datongST']); nsterm = len(cy['sterm']);
    for cm in cy['cm']:
        jd0 = cm['JDN']; jd1 = jd0 + cm['n'];
        date = CalDat(jd0)
        jian_num = 0
        if cm['jian'] != 'NA' and cm['jian'] != 'NZ':
            jian_num = int(cm['jian'])
        # Chinese month column
        cm_label = chinese_month_label(cal, y, cm['cm'], calendar)
        if y==700 and cal.lang != 'Eng' and cm['jian']=='25':
            # This is the second month 11 in 700
            cm_label = '十一月'
        html += '<tr><td' + bstyle + cm_label
        if cal.lang=='Eng':
            html += ' (' + ('L' if cm['n'] > 29 else 'S') + ')'
            if jian_num > 0:
                html += '<br />Jian: ' + cal.stem[(jian_num-1) % 10] + ' ' + cal.branch[(jian_num-1) % 12]
            elif cm['jian']=='NZ':
                html += '<br />(no Zhongqi)'
        else:
            html += '大' if cm['n'] > 29 else '小'
            if jian_num > 0:
                html += '<br />建' + cal.stem[(jian_num-1) % 10] + cal.branch[(jian_num-1) % 12]
            elif cm['jian']=='NZ':
                html += '<br />(' + ('無中氣' if cal.lang=='ChiT' else '无中气') + ')'
        html += '</td>'

        # Conjunction date column
        html += '<td' + bstyle
        if cal.lang=='Eng':
            html += cal.stem[(jd0-1) % 10] + ' ' + cal.branch[(jd0+1) % 12] + '<br />'
            html += str(cal.wmonthName[date['mm']-1]) + ' ' + str(date['dd'])
        else:
            html += cal.stem[(jd0-1) % 10] + cal.branch[(jd0+1) % 12] + '<br />'
            html += str(date['mm']) + '月' + str(date['dd']) + '日'
        html += '</td>'

        # Calendrical solar term column
        if ncalst > 0:
            csthtml, kcalst = add_cal_solar_term(kcalst, ncalst, cy['calst'], jd0, jd1)
            html += csthtml
        if calendar=='default' and y > 1666 and y < 1670:
            # Datong solar term
            csthtml, kdatongst = add_cal_solar_term(kdatongst, ndatongst, cy['datongST'], jd0, jd1)
            html += csthtml

        # DE solar term column column
        shtml, kst = add_DE_solar_term(kst, nsterm, cy['sterm'], jd0, jd1)
        html += shtml

    html += '</table>'

    # Print calendar note, if any.
    note = addChineseYearNote(y, cal.lang, calendar)
    if len(note) > 0: html += note

    # Print Chinese calendar version
    if cal.lang=='Eng':
        html += '<p style="font-weight:bold;">Chinese calendar: ' + cy['calendar'] + '</p>'
    elif cal.lang=='ChiT':
        html += '<p style="font-weight:bold;">中曆: ' + cy['calendar'] + '</p>'
    else:
        html += '<p style="font-weight:bold;">中历: ' + cy['calendar'] + '</p>'

    return html

def conjunction_date_html(cal, date, inp):
    """
    Display the conjunction lunar date in a Western calendar table.
    For most of the case, it's just [Chinese month number]-01 for English or 某月 in Chinese. 
    The string will be bold and in brown or red (if it's the Chinese New Year).
    """
    calendar = inp['calendar']
    cyear = date['Chinese ymd'][0]
    cm = date['Chinese ymd'][1]
    cdate = date['cdate'] if cal.lang=='Eng' else chinese_month_label(cal, cyear, cm, calendar)
    firstMonth = 1
    if calendar=='Zhuanxu' or (calendar=='default' and cyear > -221 and cyear < -103):
        firstMonth = 10
    if calendar=='default' and cyear > 689 and cyear < 701:
        firstMonth = 11
    return '<span style="color:' + ('red' if cm==firstMonth else 'brown') + ';font-weight:bold;">' + cdate + '</span>'

def print_date_Western_month_table_html(cal, date, inp): 
    """
    return the html text of one date in the month table of a Western calendar
    """
    html = '<h3>' + str(date['Western ymd'][2]) + '</h3>'
    cstyle =' style="text-align:center;">'
    cdate = date['cdate'] if cal.lang=='Eng' else cal.cday[date['Chinese ymd'][2]-1]
    if date['Chinese ymd'][2]==1: cdate = conjunction_date_html(cal, date, inp)
    if cal.lang=='Eng':
        html += '<p' + cstyle + cdate + '</p>'
    else:
        html += '<p' + cstyle + cdate + '</p>'
    html += '<p' + cstyle + date['sexagenary date'][0] + '</p>'
    if inp['showJDN']:
        html += '<p' + cstyle + str(date['JDN']) + '</p>'
    return html

def print_Western_year_html(cal, inp):
    """
    Create HTML text that displays a Western year with Chinese dates, moon phases and solar terms.
    Input: 
      cal: calendar object returned by calendar_conversion class
      inp (dict): dictionary of input parameters with the following keys.
        'calendar': Chinese calendar version (one of the keys in available_calendars()).
        'y': Western year
        'dates': list of dict containing the information of all dates in the year. Each dict in the list contains the same key-value pairs as in the output of western_to_chinese_date_lookup().
        'showJDN' (bool): whether or not to show the Julian day at noon.
        'st': solar term data calculated by DE431/DE441
        'mp': moon phase data calculated by DE431/DE441
        'calst' (optional): calendrical solar term information
        'datongST' (optional): Datong solar term information (only for the Qing dynasty in 1667-1669).
    Return: HTML text that displays a Western month with Chinese dates, moon phases and solar terms.
    """
    y = inp['y']; dates = inp['dates']; lang = cal.lang;
    # Print Western year
    Gregorian = {'Eng':'Gregorian', 'ChiT':'格里曆', 'ChiS':'格里历'}
    Julian = {'Eng':'Julian', 'ChiT':'儒略曆', 'ChiS':'儒略历'}
    ProlepticJulian = {'Eng':'Proleptic Julian', 'ChiT':'逆推儒略曆', 'ChiS':'逆推儒略历'}
    gcal = Gregorian[lang] if y > 1582 else (Julian[lang] if y > 7 else ProlepticJulian[lang])
    if y==1582: gcal = Julian[lang] + '/' + Gregorian[lang]
    html = '<h2>'
    if lang=='Eng':
        html += gcal + ' Year: ' + str(y)
        if y <= 0: html += ' (' + str(1-y) + ' BCE)'
    else:
        html += ('公曆年(' if lang=='ChiT' else '公历年(') + gcal + '): ' + str(y)
        if y <= 0: html += ' (前' + str(1-y) + ')'
    html += '</h2>'
    # Print Chinese year
    html += add_chinese_year_info(cal, dates, '<h2>', '</h2>') + '<br />'
    # Add year info
    yinfo = addYearInfo(y, cal.lang, inp['calendar'])
    if len(yinfo) > 0:
        html += '<h3 style="color:brown;line-height:130%;">' + yinfo + '</h3><br />'
    # Print Western months
    inpm = {'calendar':inp['calendar'], 'y':y, 'showJDN':inp['showJDN'], 
             'show_chinese_year_info':False, 'show_chinese_calendar_info':False}
    for m in range(1, 13):
        inpm['m'] = m
        inpm['dates'] = [x for x in dates if x['Western ymd'][1]==m]
        inpm['mp'] = [x for x in inp['mp'] if x[1]['month']==m]
        inpm['st'] = [x for x in inp['st'] if x[1]['month']==m]
        if 'calst' in inp:
            inpm['calst'] = [x for x in inp['calst'] if x[1][1]==m]
            if 'datongST' in inp:
                inpm['datongST'] = [x for x in inp['datongST'] if x[1][1]==m]
        html += print_Western_month_html(cal, inpm) + '<br />'
    if inp['show_chinese_calendar_info']:
        html += '<h4>' + add_chinese_calendar_info(cal, dates) + '</h4>'
    return html

def print_Western_month_html(cal, inp):
    """
    Create HTML text that displays a Western month with Chinese dates, moon phases and solar terms.
    Input: 
      cal: calendar object returned by calendar_conversion class
      inp (dict): dictionary of input parameters with the following keys.
        'calendar': Chinese calendar version (one of the keys in available_calendars()).
        'y': Western year, 'm': Western month, 
        'dates': list of dict containing the information of all dates in the month. Each dict in the list contains the same key-value pairs as in the output of western_to_chinese_date_lookup().
        'showJDN' (bool): whether or not to show the Julian day at noon.
        'st': solar term data calculated by DE431/DE441
        'mp': moon phase data calculated by DE431/DE441
        'show_chinese_year_info' (bool): whether to display all Chinese years in 'dates'
        'show_chinese_calendar_info' (bool): whether to display all Chinese calendar versions in 'dates'
        'calst' (optional): calendrical solar term information
        'datongST' (optional): Datong solar term information (only for the Qing dynasty in 1667-1669).
    Return: HTML text that displays a Western month with Chinese dates, moon phases and solar terms.
    """
    # unpack parameter and data
    calendar = inp['calendar']; y = inp['y']; m = inp['m']; dates = inp['dates'];
    # Western year and month
    if y > 0:
        wy = str(y) + ('' if cal.lang=='Eng' else '年')
    else:
        wy = ('' if cal.lang=='Eng' else '前') + str(1-y) + (' BCE' if cal.lang=='Eng' else '年')
    wm = cal.wmonthName[m-1]
    # gather all Chinese months in dates
    cm_list = [x['Chinese ymd'][1] for x in dates]
    cmonth = list(dict.fromkeys(cm_list))
    ind = [cm_list.index(x) for x in cmonth] # indices of first occurance of cmonth
    cmLength = [{'Eng':'S', 'ChiT':'小', 'ChiS':'小'}, {'Eng':'L', 'ChiT':'大', 'ChiS':'大'}]
    cym = []
    for j, i in enumerate(ind):
        cyear = dates[i]['Chinese ymd'][0]
        cmLong = cmLength[1][cal.lang] if dates[i]['Nday_cmonth']==30 else cmLength[0][cal.lang]
        sex_year = dates[i]['sexagenary year'][0]
        jian = dates[i]['jian'][0] if 'jian' in dates[i] else ''
        if cal.lang=='Eng':
            cymi = 'Year: ' + sex_year + ', Month: '+ chinese_month_label(cal, cyear, cmonth[j], calendar) 
            cymi += ' (' + cmLong
            if len(jian) > 0:
                cymi += ', '+jian
            if 'no Zhongqi' in dates[i]['cdate']:
                cymi += ', no Zhongqi'
            cymi += ')'
        else:
            cymi = sex_year + '年 ' + chinese_month_label(cal, cyear, cmonth[j], calendar) + cmLong
            if len(jian) > 0:
                cymi += ' (' + jian + ')'
            if '無中氣' in dates[i]['cdate'] or '无中气' in dates[i]['cdate']:
                cymi += ' (' + ('無中氣' if cal.lang=='ChiT' else '无中气') + ')'
        cym += [cymi]
    n_cmonth = len(cmonth)
    # create html text
    bstyle = ' style="border:1px solid black;border-collapse:collapse;text-align:center;">'
    wstyle = ' style="font-size:120%;border:1px solid black;border-collapse:collapse;text-align:center;">'
    html = '<table' + bstyle
    if n_cmonth==1:
        html += '<tr><th colspan="2"' + bstyle + '<h2 style="line-height:130%;">' + wy + '<br />' + wm + '</h2>'
        html += '</th><th colspan="5"' + bstyle
        html += '<h3>' + cym[0] + '</h3></th></tr>'
    else:
        html += '<tr><th colspan="2" rowspan="' + str(n_cmonth) + '"' + bstyle + '<h2 style="line-height:130%;">' + wy + '<br />' + wm
        html += '</h2></th><th colspan="5"' + bstyle + '<h3>' + cym[0] + '</h3></th></tr>'
        for i in range(1, n_cmonth):
            html += '<tr><th colspan="5"' + bstyle + '<h3>' + cym[i] + '</h3></th></tr>'
    # Week row
    html += '<tr>'
    for i in range(7):
        html += '<th' + wstyle + cal.week[i] + '</th>'
    html += '</tr>'
    # calendar table
    w1 = dates[0]['Week'][1] # day of week of the first day in the month
    html += '<tr>'
    if w1 > 0:
        html += ('<td' if w1==1 else '<td colspan="' + str(w1) + '"') + bstyle + '</td>'
    # now go through all dates in the month
    for date in dates:
        if date['Week'][1]==0 and date['Western ymd'][2] != 1: html += '<tr>'
        html += '<td' + bstyle + print_date_Western_month_table_html(cal, date, inp) + '</td>'
        if date['Week'][1]==6: html += '</tr>'
    w1 = dates[-1]['Week'][1] # day of week of the last day in the month
    if w1 != 6:
        html += ('<td' if w1==5 else '<td colspan="' + str(6-w1) + '"') + bstyle + '</td></tr>'
    html += '</table>'
    html += addMoonPhases(cal, inp)
    html += addSolarTerms(cal, inp)
    if 'calst' in inp:
        html += addCalendricalSolarTerms(cal, inp)
    note = monthly_calendarNotes(y, m, cal.lang, calendar)
    if len(note) > 0:
        html += '<p style="color:red;">' + note + '</p>'
    if inp['show_chinese_year_info']:
        html += add_chinese_year_info(cal, dates, '<p>', '</p>')
    if inp['show_chinese_calendar_info']:
        html += '<p>' + add_chinese_calendar_info(cal, dates) + '</p>'
    return html

def addMoonPhases(cal, inp):
    mpName = {'Eng':'Moon phases ('+cal.ephemeris+')', 'ChiT':'月相 ('+cal.ephemeris+')', 'ChiS':'月相 ('+cal.ephemeris+')'}
    html = '<p><b>' + mpName[cal.lang] + ':</b>'
    for mp in inp['mp']:
        html += ' [' + mp[1]['event'] + '] '+str(mp[1]['date']) 
        html += ('d ' if cal.lang=='Eng' else '日 ') + mp[1]['timeString']
        if 'eclipse' in mp[1]:
            html += ' (<a href="' + mp[1]['eclipse url'] + '" target="_blank">' + mp[1]['eclipse'] + '</a>)'
        html += '&nbsp;&nbsp;'
    html += '</p>'
    return html

def addSolarTerms(cal, inp):
    stName = {'Eng':'24 solar terms ('+cal.ephemeris+')', 'ChiT':'二十四節氣 ('+cal.ephemeris+')', 'ChiS':'二十四节气 ('+cal.ephemeris+')'}
    html = '<p><b>' + stName[cal.lang] + ':</b>'
    for st in inp['st']:
        html += ' [' + st[1]['event'] + '] '+str(st[1]['date'])
        html += ('d ' if cal.lang=='Eng' else '日 ') + st[1]['timeString'] + '&nbsp;&nbsp;'
    html += '</p>'
    return html

def addCalendricalSolarTerms(cal, inp):
    y = inp['y']; m = inp['m']; calendar = inp['calendar']
    if calendar=='GBT' or (calendar=='default' and (y > 1645 or (y==1645 and m > 1))):
        stName = {'Eng':'Calendrical solar terms (dingqi)', 'ChiT':'曆書節氣(定氣)', 'ChiS':'历书节气(定气)'}
    else:
        stName = {'Eng':'Calendrical solar terms (pingqi)', 'ChiT':'曆書節氣(平氣)', 'ChiS':'历书节气(平气)'}
    # deal with 1667-1670 in Qing dynasty
    if calendar=='default':
        if (y==1667 and m > 1) or y==1668 or y==1669 or (y==1670 and m < 3):
            stName = {'Eng':'Xinfa solar terms (dingqi)', 'ChiT':'新法節氣(定氣)', 'ChiS':'新法节气(定气)'}
    html = '<p><b>' + stName[cal.lang] + ':</b>'
    for st in inp['calst']:
        html += ' [' + st[0] + '] ' + str(st[1][2]) + ('d&nbsp;&nbsp;' if cal.lang=='Eng' else '日&nbsp;&nbsp;')
    html += '</p>'
    # add Datong solar terms in 1667-1670 Feb in Qing dynasty
    if calendar=='default':
        if (y==1667 and m > 1) or y==1668 or y==1669 or (y==1670 and m < 3):
            stName = {'Eng':'Datong solar terms (pingqi)', 'ChiT':'大統曆節氣(平氣)', 'ChiS':'大统历节气(平气)'}
            html += '<p><b>' + stName[cal.lang] + ':</b>'
            for st in inp['datongST']:
                html += ' [' + st[0] + '] ' + str(st[1][2]) + ('d&nbsp;&nbsp;' if cal.lang=='Eng' else '日&nbsp;&nbsp;')
            html += '</p>'
    return html

def add_chinese_year_info(cal, dates, hst, hend):
    """
    Add Chinese year information in the dates in dates. 
    Input:
      cal: calendar object returned by calendar_conversion class.
      dates: list of dict containing the information of all dates in the month. Each dict in the list contains the same key-value pairs as in the output of western_to_chinese_date_lookup().
      hst (str), hend (str): Beginning and end of the html tag (e.g. (<p>, </p>), (<h3>, </h3>))
    Return: html text for displaying all Chinese years in dates.
    """
    #hst = '<h3>'; hend = '</h3>';
    html = hst
    if cal.lang=='Eng':
        html += 'Chinese year:'
    elif cal.lang=='ChiT':
        html += '中曆年:'
    else:
        html += '中历年:'
    html += hend
    cyearInfo = extractChineseYear_CalendarInfo(cal, dates)
    cyear = cyearInfo['cyear']; cyear_range = cyearInfo['cyear_range'];
    if len(cyear)==1:
        html += hst + cyear[0] + hend
    else:
        for i in range(len(cyear)):
            if cal.lang=='Eng':
                html += hst + cyear[i] + ' ' + cyear_range[i] + hend
            else:
                html += hst + cyear_range[i] + ': ' + cyear[i] + hend
    return html

def add_chinese_calendar_info(cal, dates):
    """
    Add Chinese year information in the dates in dates. 
    Input:
      cal: calendar object returned by calendar_conversion class.
      dates: list of dict containing the information of all dates in the month. Each dict in the list contains the same key-value pairs as in the output of western_to_chinese_date_lookup().
    Return: html text for displaying all Chinese calendars in dates.
    """
    if cal.lang=='Eng':
        html = 'Chinese calendar: '
    elif cal.lang=='ChiT':
        html = '中曆: '
    else:
        html = '中历: '
    ccalInfo = extractChineseCalendarInfo(cal, dates)
    ccal = ccalInfo['ccal']; ccal_range = ccalInfo['ccal_range'];
    ncal = len(ccal)
    if ncal==1:
        html += ccal[0]
    else:
        for i in range(ncal):
            html += ccal[i] + ' (' + ccal_range[i] + ')'
            if i != ncal-1: html += ', '
    return html

def extractChineseYear_CalendarInfo(cal, dates):
    cy_list = [x['sexagenary year'][0] + ' ('+ x['sexagenary year'][1] + ')' for x in dates]
    cyear = list(dict.fromkeys(cy_list))
    ind = [cy_list.index(x) for x in cyear] # indices of first occurance of cyear
    cyear_start_date = []
    for j,i in enumerate(ind):
        cyear_start_date += [cal.wmonthName[dates[i]['Western ymd'][1]-1] + cal.wdayName[dates[i]['Western ymd'][2]-1]]
        if 'reign/era' in dates[i]:
            cyear[j] += ' (' + dates[i]['reign/era'] + ')'
    cyear_range = []
    ncyear = len(cyear)
    if ncyear > 1:
        for i in range(ncyear):
            if i==0:
                rge = {'Eng':'before ' + cyear_start_date[1], 'ChiT':cyear_start_date[1] + '前', 'ChiS':cyear_start_date[1] + '前'}
            elif i==ncyear-1:
                rge = {'Eng':'on and after ' + cyear_start_date[-1], 'ChiT':cyear_start_date[-1] + '及以後', 'ChiS':cyear_start_date[-1] + '及以后'}
            else:
                k = ind[i+1] - 1
                end_date = cal.wmonthName[dates[k]['Western ymd'][1]-1] + cal.wdayName[dates[k]['Western ymd'][2]-1]
                rge = {'Eng':'between ' + cyear_start_date[i] + ' and ' + end_date,
                         'ChiT':cyear_start_date[i] + '至' + end_date,
                         'ChiS':cyear_start_date[i] + '至' + end_date}
            cyear_range += [rge[cal.lang]]
    return {'cyear':cyear, 'cyear_start_date':cyear_start_date, 'cyear_range':cyear_range}

def extractChineseCalendarInfo(cal, dates):
    ccal_list = [x['Chinese calendar'] for x in dates]
    ccal = list(dict.fromkeys(ccal_list))
    ind = [ccal_list.index(x) for x in ccal] # indices of first occurance of ccal
    ccal_start_date = []
    for i in ind:
        ccal_start_date += [cal.wmonthName[dates[i]['Western ymd'][1]-1] + cal.wdayName[dates[i]['Western ymd'][2]-1]]
    ccal_range = []
    nccal = len(ccal)
    if nccal > 1:
        for i in range(nccal):
            if i==0:
                rge = {'Eng':'before ' + ccal_start_date[1], 'ChiT':ccal_start_date[1] + '前', 'ChiS':ccal_start_date[1] + '前'}
            elif i==nccal-1:
                rge = {'Eng':'on and after ' + ccal_start_date[-1], 'ChiT':ccal_start_date[-1] + '及以後', 'ChiS':ccal_start_date[-1] + '及以后'}
            else:
                k = ind[i+1] - 1
                end_date = cal.wmonthName[dates[k]['Western ymd'][1]-1] + cal.wdayName[dates[k]['Western ymd'][2]-1]
                rge = {'Eng':'between ' + ccal_start_date[i] + ' and ' + end_date,
                         'ChiT':ccal_start_date[i] + '至' + end_date,
                         'ChiS':ccal_start_date[i] + '至' + end_date}
            ccal_range += [rge[cal.lang]]
    return {'ccal':ccal, 'ccal_start_date':ccal_start_date, 'ccal_range':ccal_range}

def reformat_calendrical_solar_term_tuples(cal, calst):
    """
    [(solar term label, JDN), ...] -> [(solar term name, [y, m, d]), ...] where y,m,d are Western year, month and date.
    """
    calst_new = []
    for x in calst:
        date = CalDat(x[1])
        calst_new += [(cal.stermName[x[0]], [int(date['yy']), int(date['mm']), int(date['dd'])])]
    return calst_new

def print_Chinese_yearly_calendar_html(cal, inp):
    """
    Create HTML text that displays a Chinese year with Western dates, moon phases and solar terms.
    Input: 
      cal: calendar object returned by calendar_conversion class
      inp (dict): dictionary of input parameters with the following keys.
        'calendar': Chinese calendar version (one of the keys in available_calendars()).
        'y': Chinese year (whose new year date is closest to Jan 1 in Western year y).
        'cy': dictionary with keys 'cm', 'calendar', and (optional) 'regign/era', where 
      'cm': a list containing the information of all Chinese months in Chinese year y in the form of [{'cm':m1, 'd':d1, 'jian':'jian1', n:n1}, {'cm':m2, 'd':d2, 'jian':'jian2', n:n2}, ...] with 'cm' indicating the Chinese month number (negative for a leap month), 'd' indicating the number of days from Dec 31, y-1 of the first day of the Chinese month, 'jian' indicating the sexagenary month cycle associated with jian ('jian'='1' for jia zi, '2' for yi chou, ... '60' for gui hai, 'NA' for leap month, 'NZ' for a month not containing a major solar term (only for the ancient six calendars)), and 'n' indicating the number of days in the Chinese month. The list is sorted in ascending order in values in 'd'. 'calendar' (str): version of the Chinese calendar (e.g. 'Santong', 'Shixian'). 'reign/era' (str, optional): reign and/or era name of the Chinese year (only for calendars before 1912).
        'showJDN' (bool): whether or not to show the Julian day at noon.
        'st': solar term data calculated by DE431/DE441
        'mp': moon phase data calculated by DE431/DE441
        'calst' (optional): calendrical solar term information
        'datongST' (optional): Datong solar term information (only for the Qing dynasty in 1667-1669).
    Return: HTML text that displays a Chinese month with Western dates, moon phases and solar terms.
    """
    # unpack parameter and data
    calendar = inp['calendar']; y = inp['y']; cy = inp['cy'];
    # Print Chinese year
    html = '<h1>'
    if cal.lang=='Eng':
        html += 'Chinese Year: '+ cal.stem[(y + 3506) % 10] + ' '+cal.branch[(y + 3512) % 12]+' ('+cal.branch_animal[(y + 3512) % 12]+') '
    elif cal.lang=='ChiT':
        html += '中曆年: '+cal.stem[(y + 3506) % 10]+cal.branch[(y + 3512) % 12]+'('+cal.branch_animal[(y + 3512) % 12]+')'
    else:
        html += '中历年: '+cal.stem[(y + 3506) % 10]+cal.branch[(y + 3512) % 12]+'('+cal.branch_animal[(y + 3512) % 12]+')'
    if cy['reign/era'] != 'NA':
        html += ' (' + cy['reign/era'] + ')'
    html += '</h1>'

    # Print Western dates
    html += '<h2>' + print_Western_date_range_Chinese_year(y, cal, cy['cm']) + '</h2>'

    # Add year info
    yinfo = addYearInfo(y, cal.lang, calendar)
    if len(yinfo) > 0 and not (calendar=='default' and y==1670) and not (calendar=='default' and y==240):
        html += '<h3 style="color:brown;line-height:130%;">' + yinfo + '</h3>'

    # Add all Chinese months in the Chinese year
    for cm in cy['cm']:
        html += print_one_Chinese_month(cal, inp, cm) + '<br />'
    if inp['show_chinese_calendar_info']:
        html += print_Chinese_calendar_version(cal, inp['cy'])
    return html

def print_Chinese_monthly_calendar_html(cal, inp):
    """
    Create HTML text that displays a Chinese month with Western dates, moon phases and solar terms.
    Input: 
      cal: calendar object returned by calendar_conversion class
      inp (dict): dictionary of input parameters with the following keys.
        'calendar': Chinese calendar version (one of the keys in available_calendars()).
        'y': Chinese year, 'm': Chinese month, 
        'cy': dictionary with keys 'cm', 'calendar', and (optional) 'regign/era', where 
        'cm': a list containing the information of all Chinese months in Chinese year y in the form of [{'cm':m1, 'd':d1, 'jian':'jian1', n:n1}, {'cm':m2, 'd':d2, 'jian':'jian2', n:n2}, ...] with 'cm' indicating the Chinese month number (negative for a leap month), 'd' indicating the number of days from Dec 31, y-1 of the first day of the Chinese month, 'jian' indicating the sexagenary month cycle associated with jian ('jian'='1' for jia zi, '2' for yi chou, ... '60' for gui hai, 'NA' for leap month, 'NZ' for a month not containing a major solar term (only for the ancient six calendars)), and 'n' indicating the number of days in the Chinese month. The list is sorted in ascending order in values in 'd'. 'calendar' (str): version of the Chinese calendar (e.g. 'Santong', 'Shixian'). 'reign/era' (str, optional): reign and/or era name of the Chinese year (only for calendars before 1912).
        'jdy' (int): Julian date at noon on December 31, y-1 in Western calendar
        'showJDN' (bool): whether or not to show the Julian day at noon.
        'st': solar term data calculated by DE431/DE441
        'mp': moon phase data calculated by DE431/DE441
        'show_chinese_year_info' (bool): whether to display the Chinese year
        'show_chinese_calendar_info' (bool): whether to display all Chinese calendar versions
        'calst' (optional): calendrical solar term information
        'datongST' (optional): Datong solar term information (only for the Qing dynasty in 1667-1669).
    Return: HTML text that displays a chinese month with Western dates, moon phases and solar terms.
    """
    cm = [x for x in inp['cy']['cm'] if x['cm']==inp['m']]
    html = ''
    # Loop over the Chinese months in cm[]
    for cmd in cm: 
        html += print_one_Chinese_month(cal, inp, cmd) + '<br />'
    if inp['show_chinese_year_info']:
        html += add_chinese_year_info_Chinese_month(cal, inp['y'], inp['cy'], '<p>', '</p>')
    if inp['show_chinese_calendar_info']:
        html += print_Chinese_calendar_version(cal, inp['cy'])
    return html

def print_one_Chinese_month(cal, inp, cmd):
    def add_western_year_month_row(wy, wm, cspan, bstyle):
        row = '<th colspan="' + cspan + '"' + bstyle + '<h3>'
        wyear = str(wy) if wy > 0 else (str(1-wy)+' BCE' if cal.lang=='Eng' else '前' + str(1-wy)) 
        wmonth = cal.wmonthName[wm-1]
        if cal.lang=='Eng':
            wms = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
            row += wms[wm-1] + ' ' + wyear 
        else:
            row += wyear + '年' + wmonth
        row += '</h3></th>'
        return row
    
    # unpack parameter and data
    calendar = inp['calendar']; y = inp['y']; m = cmd['cm']; 
    bstyle = ' style="border:1px solid black;border-collapse:collapse;text-align:center;">'
    wstyle = ' style="font-size:120%;border:1px solid black;border-collapse:collapse;text-align:center;">'

    # Sexagenary year 
    if cal.lang=='Eng':
        cyear = cal.stem[(y + 3506) % 10] + ' ' + cal.branch[(y + 3512) % 12] + ' (' + cal.branch_animal[(y + 3512) % 12] + ')'
    else:
        cyear = cal.stem[(y + 3506) % 10] + cal.branch[(y + 3512) % 12] + '年 (' + cal.branch_animal[(y + 3512) % 12] + ')'
        
    # Chinese month
    cmonth = chinese_month_label(cal, y, m, calendar)
    if calendar=='default' and y==700 and cal.lang != 'Eng' and cmd['jian']=='25':
        # This is the second month 11 in 700
        cmonth = '十一月'
    if cal.lang=='Eng':
        cmonth += ' (' + ('S' if cmd['n'] < 30 else 'L') + ')'
    else:
        cmonth += '小' if cmd['n'] < 30 else '大'
    if cmd['jian']=='NZ': 
        # add no Zhongqi label (for the ancient six and early Han calendars)
        cmonth += '<br />' + '(' + no_Zhongqi_label(cal.lang) + ')'
    # add jian
    if cmd['jian'] != 'NA' and cmd['jian'] != 'NZ':
        jian_num = int(cmd['jian'])
        jian_name = '(建' if cal.lang=='ChiT' or cal.lang=='ChiS' else '(Jian: '
        cmonth += '<br />' + jian_name + cal.stem[(jian_num-1) % 10] + cal.branch[(jian_num-1) % 12] + ')'

    jd1 = inp['jdy'] + cmd['d']
    jd2 = jd1 + cmd['n'] - 1
    date1 = CalDat(jd1, 0)
    date2 = CalDat(jd2, 0)
    y1 = date1['yy']; m1 = date1['mm'];
    y2 = date2['yy']; m2 = date2['mm'];
    # nwm: Number of Western months in this Chinese month
    nwm = m2 - m1 + 1
    if nwm < 0: nwm += 12
    # print header
    cspan1 = 3; cspan2 = 7-cspan1; cspan1 = str(cspan1); cspan2 = str(cspan2);
    html = '<table' + bstyle
    html += '<tr><th colspan="' + cspan1 +'" rowspan="' + str(nwm) + '"' + bstyle 
    html += '<h2 style="line-height:130%;">' + cyear + '<br />' + ('Month ' if cal.lang=='Eng' else '') + cmonth + '</h2></th>'
    html += add_western_year_month_row(y1, m1, cspan2, bstyle) + '</tr>'
    if nwm==2:
        html += '<tr>' + add_western_year_month_row(y2, m2, cspan2, bstyle) + '</tr>'
    elif nwm==3:
        html += '<tr>' + add_western_year_month_row(y2, m2-1, cspan2, bstyle) + '</tr>'
        html += '<tr>' + add_western_year_month_row(y2, m2, cspan2, bstyle) + '</tr>'
    # Week row
    html += '<tr>'
    for i in range(7):
        html += '<th' + wstyle + cal.week[i] + '</th>'
    html += '</tr>'
    # calendar table
    cstyle =' style="text-align:center;">'
    week1 = (jd1 + 1) % 7
    if week1 != 0:
        if week1 > 1:
            html += '<tr><td colspan="'+str(week1)+'"></td>'
        else:
            html += '<tr><td></td>'
    for d in range(1, cmd['n']+1):
        jdn = jd1 + d-1
        wd, wcal, sex_date, week = Western_date_sexagenary_date_week_from_JDN(cal, jdn)
        if week[1]==0: html += '<tr>'
        html += '<td' + bstyle + '<h3>'
        html += (str(d) if cal.lang=='Eng' else cal.cday[d-1]) + '</h3>' 
        html += '<p' + cstyle + sex_date[0] + '</p>'
        if wd[2]==1:
            html += '<p style="color:' + ('red' if wd[1]==1 else 'brown') + ';text-align:center;">'
        else:
            html += '<p' + cstyle
        html += cal.wmonthName[wd[1]-1] + (' ' if cal.lang=='Eng' else '') + cal.wdayName[wd[2]-1] + '</p>'
        if inp['showJDN']: html += '<p' + cstyle + str(jdn) + '</p>'
        html += '</td>'
        if week[1]==6: html += '</tr>'
    week1 = (jd1 + cmd['n']) % 7
    if week1 != 6:
        if week1==5:
            html += '<td></td></tr>'
        else:
            html += '<td colspan="' + str(6-week1) + '"></td></tr>'
    html += '</table>'
    # add month phases and solar terms
    html += addMoonPhases_Chinese_month(cal, inp['mp'], jd1, jd2)
    html += addSolarTerms_Chinese_month(cal, inp, jd1, jd2)
    # add calendrical solar terms
    if 'calst' in inp:
        html += addCalendricalSolarTerms_Chinese_month(cal, inp, jd1, jd2)
    # add calendar note
    note = monthly_calendarNotes(y, -9999, cal.lang, calendar, m)
    if len(note) > 0:
        html += '<p style="color:red;">' + note + '</p>'
    return html

def addMoonPhases_Chinese_month(cal, mp, jd1, jd2):
    mpName = {'Eng':'Moon phases ('+cal.ephemeris+')', 'ChiT':'月相 ('+cal.ephemeris+')', 'ChiS':'月相 ('+cal.ephemeris+')'}
    html = '<p><b>' + mpName[cal.lang] + ':</b>'
    f5o6 = 5.0/6
    for mpi in mp:
        jdn = int(mpi[1]['jd0_ut'] + mpi[1]['jd1_ut'] + f5o6)
        if jdn < jd1 or jdn > jd2: continue
        html += ' [' + mpi[1]['event'] + '] '
        d = jdn - jd1 + 1
        date = str(d) + 'd ' if cal.lang=='Eng' else cal.cday[d-1]+' '
        html += date + mpi[1]['timeString']
        if 'eclipse' in mpi[1]:
            html += ' (<a href="' + mpi[1]['eclipse url'] + '" target="_blank">' + mpi[1]['eclipse'] + '</a>)'
        html += '&nbsp;&nbsp;'
    html += '</p>'
    return html

def addSolarTerms_Chinese_month(cal, inp, jd1, jd2):
    stName = {'Eng':'24 solar terms ('+cal.ephemeris+')', 'ChiT':'二十四節氣 ('+cal.ephemeris+')', 'ChiS':'二十四节气 ('+cal.ephemeris+')'}
    html = '<p><b>' + stName[cal.lang] + ':</b>'
    f5o6 = 5.0/6
    for st in inp['st']:
        jdn = int(st[1]['jd0_ut'] + st[1]['jd1_ut'] + f5o6)
        if jdn < jd1 or jdn > jd2: continue
        html += ' [' + st[1]['event'] + '] '
        d = jdn - jd1 + 1
        date = str(d) + 'd ' if cal.lang=='Eng' else cal.cday[d-1]+' '
        html += date + st[1]['timeString'] + '&nbsp;&nbsp;'
    html += '</p>'
    return html

def addCalendricalSolarTerms_Chinese_month(cal, inp, jd1, jd2):
    y = inp['y']; calendar = inp['calendar']
    if (calendar=='default' and y > 1644) or calendar=='GBT':
        stName = {'Eng':'Calendrical solar terms (dingqi)', 'ChiT':'曆書節氣(定氣)', 'ChiS':'历书节气(定气)'}
    else:
        stName = {'Eng':'Calendrical solar terms (pingqi)', 'ChiT':'曆書節氣(平氣)', 'ChiS':'历书节气(平气)'}
    # deal with 1667-1669 in Qing dynasty
    if calendar=='default':
        if y > 1666 and y < 1670:
            stName = {'Eng':'Xinfa solar terms (dingqi)', 'ChiT':'新法節氣(定氣)', 'ChiS':'新法节气(定气)'}
    html = '<p><b>' + stName[cal.lang] + ':</b>'
    for st in inp['calst']:
        if st[1] < jd1 or st[1] > jd2: continue
        d = st[1] - jd1 + 1
        date = str(d) + 'd ' if cal.lang=='Eng' else cal.cday[d-1]+' '
        html += ' [' + cal.stermName[st[0]] + '] ' + date + '&nbsp;&nbsp;'
    html += '</p>'
    # add Datong solar terms in 1667-1669 in Qing dynasty
    if calendar=='default':
        if y > 1666 and y < 1670:
            stName = {'Eng':'Datong solar terms (pingqi)', 'ChiT':'大統曆節氣(平氣)', 'ChiS':'大统历节气(平气)'}
            html += '<p><b>' + stName[cal.lang] + ':</b>'
            for st in inp['datongST']:
                if st[1] < jd1 or st[1] > jd2: continue
                d = st[1] - jd1 + 1
                date = str(d) + 'd ' if cal.lang=='Eng' else cal.cday[d-1]+' '
                html += ' [' + cal.stermName[st[0]] + '] ' + date + '&nbsp;&nbsp;'
            html += '</p>'
    return html

def add_chinese_year_info_Chinese_month(cal, y, cy, hst, hend):
    """
    Add Chinese year information in cy
    Input:
      cal: calendar object returned by calendar_conversion class.
      y (int): Chinese year
      cy: dictionary with keys 'cm', 'calendar', and (optional) 'regign/era'
      hst (str), hend (str): Beginning and end of the html tag (e.g. (<p>, </p>), (<h3>, </h3>))
    Return: html text for displaying all Chinese years in dates.
    """
    html = hst
    if cal.lang=='Eng':
        html += 'Chinese Year: '+ cal.stem[(y + 3506) % 10] + ' '+cal.branch[(y + 3512) % 12]+' ('+cal.branch_animal[(y + 3512) % 12]+') '
    elif cal.lang=='ChiT':
        html += '中曆年: '+cal.stem[(y + 3506) % 10]+cal.branch[(y + 3512) % 12]+'('+cal.branch_animal[(y + 3512) % 12]+')'
    else:
        html += '中历年: '+cal.stem[(y + 3506) % 10]+cal.branch[(y + 3512) % 12]+'('+cal.branch_animal[(y + 3512) % 12]+')'
    if cy['reign/era'] != 'NA':
        html += ' (' + cy['reign/era'] + ')'
    html += hend
    return html

def add_chinese_calendar_info_Chinese_month(cal, dates):
    """
    Add Chinese year information in the dates in dates. 
    Input:
      cal: calendar object returned by calendar_conversion class.
      dates: list of dict containing the information of all dates in the month. Each dict in the list contains the same key-value pairs as in the output of western_to_chinese_date_lookup().
    Return: html text for displaying all Chinese calendars in dates.
    """
    if cal.lang=='Eng':
        html = 'Chinese calendar: '
    elif cal.lang=='ChiT':
        html = '中曆: '
    else:
        html = '中历: '
    ccalInfo = extractChineseCalendarInfo(cal, dates)
    ccal = ccalInfo['ccal']; ccal_range = ccalInfo['ccal_range'];
    ncal = len(ccal)
    if ncal==1:
        html += ccal[0]
    else:
        for i in range(ncal):
            html += ccal[i] + ' (' + ccal_range[i] + ')'
            if i != ncal-1: html += ', '
    return html

def print_Chinese_calendar_version(cal, cy):
    if cal.lang=='Eng':
        return '<p>Chinese calendar: ' + cy['calendar'] + '</p>'
    elif cal.lang=='ChiT':
        return '<p>中曆: ' + cy['calendar'] + '</p>'
    else:
        return '<p>中历: ' + cy['calendar'] + '</p>'