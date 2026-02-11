from .calendar_calculation import *
from . import sunMoon
import importlib_resources

class calendar_conversion:
  """
  Conversion between Western and Chinese calendars
  """
  def __init__(self, lang):
    supported_lang = ['Eng', 'ChiT', 'ChiS']
    match = sum([1 if lang==x else 0 for x in supported_lang])
    if match==0:
      raise ValueError('Language '+lang+' not supported!')

    self.lang = lang
    self.ybeg = -3500
    self.default_eph = 'DE441'

    # set names
    self.wmonthName, self.wdayName = western_months_days(lang)
    self.stem, self.branch, self.branch_animal = stem_branch_names(lang)
    self.cmonth, self.leap, self.cmonth_sep = chinese_month_names(lang)
    self.week = week_names(lang)
    self.cday = chinese_day_names(lang)
    self.cyearNum = chinese_year_num_names(lang)
    self.stermName = solar_terms_names(lang)
    self.period_byear, self.period = historical_periods(lang)
    self.period_byear = np.array(self.period_byear)
    self.western_year_month_labels = western_year_month_labels(lang)
    self.western_calendar_names = western_calendar_names(lang)
    self.dcal_years, self.dcal_names = default_calendars_names(lang)
    self.dcal_years = np.array(self.dcal_years) 

    # read the default calendar data and set up the data array
    defaule_cal_file = importlib_resources.files().joinpath('default_calendar_M105_2202.csv')
    calData = np.loadtxt(defaule_cal_file, delimiter=',', skiprows=1, dtype='i')
    self.ybeg_default = calData[0, 0] + 1
    self.yend = calData[-1, 0] -1
    self.calData = calData[:,1:15] # default Chinese calendar data
    self.calSterm = calData[:,15:] # default calendrical solar term data
    self.ephemeris = 'None' # No default ephemeris

  def set_ephemeris(self, ephemeris):
    ep = ephemeris
    if ephemeris=='None' and self.ephemeris=='None':
      ep = self.default_eph
    if ep !='None' and ep != self.ephemeris:
      self.ephemeris = ep
      self.sm = sunMoon.sunMoon(self.lang, ep)
    return ep

  def chinese_year_info(self, y, calendar='default', ephemeris='None'):
    """
    Given a Chinese year whose New Year day is closest to Jan 1, y in the Western calendar, this function returns a list containing the first days in Chinese months, calendrical solar terms and solar terms computed by a DE ephemeris in the Chinese year.
    Input: 
        y (int): year in the Western calendar whose Jan 1 is closest to the Chinese New Year Day .
        calender (str): version of Chinese calendar. Only support the calendars listed in available_calendars() below.
        ephemeris: ephemeris used to compute the moon phases and solar term. It's either 'DE431' or 'DE441'.
    Return: a python list containing the following keys.
            'cm': a list containing the information of all Chinese months in the form of [{'cm':m1, 'JDN':JDN1, 'jian':'jian1', 'n':n1}, {'cm':m2, 'JDN':JDN2, 'jian':'jian2', 'n':n2}, ...] with 'cm' indicating the Chinese month number (negative for a leap month), 'JDN' indicating the Julian date at noon of the first day of the Chinese month, 'jian' indicating the sexagenary month cycle associated with jian ('jian'='1' for jia zi, '2' for yi chou, ... '60' for gui hai, 'NA' for leap month, 'NZ' for a month not containing a major solar term (only for the ancient six calendars)), and 'n' indicating the number of days in the Chinese month. The list is sorted in ascending order in the values in 'd'.
            'calendar' (str): version of the Chinese calendar (e.g. 'Santong', 'Shixian').
            'reign/era' (str, optional): reign and/or era name of the Chinese year (only for calendars before 1912).
            'calst': list of tuples [(lab1, jdn1), (lab2, jdn2), ...] where lab1, lab2, ... are the lables of the calendrical solar terms (e.g. 'J1', 'Z4') and jdn1, jdn2, ... are the Julian dates at noon of the solar terms.
            'datongST' (str, optional):  list of tuples [(lab1, jdn1), (lab2, jdn2), ...] of all the Datong solar terms in the Chinese year. This is only present for calendar='default' and 1667 <= y <= 1669.
            'sterm': a list [[lab1, info1], [lab2, info2], ...] containing all solar terms in Chinese year y, where lab1, lab2, ... are the labels of the solar terms (e.g. 'J8', 'Z3') and info1, info2, ... are dictionaries containing the Western date and time information of the solar terms.
            'mphase': a list [[lab1, info1], [lab2, info2], ...] containing all moon phases in year y, where lab1, lab2, ... are the labels of the moon phases (e.g. 'Q0', 'Q3') and info1, info2, ... are dictionaries containing the Western date and time information of the moon phases.
    """
    if y != math.floor(y):
      raise ValueError('y must be an integer')
    calendar_func = calendar_function_lookup(calendar, ephemeris)
    cy = calendar_func(self, y)
    jd0 = int(math.floor(getJDm(y-1,12,31) + 0.6))
    cm = [{'cm':x['cm'], 'JDN':jd0+x['d'], 'jian':x['jian'], 'n':x['n']} for x in cy['cm']]
    jd1 = cm[0]['JDN'] - 0.5 # UT+8 Julian date at midnight of the New Year day
    jd2 = cm[-1]['JDN'] + cm[-1]['n'] - 0.5 # UT+8 Julian date at midnight of the next New Year day
    if calendar=='Chunqiu' or (calendar=='default' and y < -479):
      calst = []
    else:
      calst = self.get_calendrical_solar_terms(calendar, jd1, jd2)
    datongST = []
    if calendar=='default':
        if y > 1666 and y < 1671:
          # calculate Datong solar terms
          datongST = self.get_calendrical_solar_terms('Datong', jd1, jd2)
    # get moon phases and solar terms
    f1o3 = 1.0/3
    ephemeris = self.set_ephemeris(ephemeris)
    sterm, mphase = self.sm.st_mp_jd(jd1 - f1o3, jd2 - f1o3)
    return {'cm':cm, 'calendar':cy['calendar'], 'reign/era':cy['reign/era'], 'calst':calst, 'datongST':datongST, 'sterm':sterm, 'mphase':mphase}
  
  def chinese_year_html(self, y, calendar='default', ephemeris='None'):
    """
    Create an HTML table showing the Chinese year whose New Year Day is closest to Jan 1, y in the Western calendar.
    Input: 
        y (int): year in the Western calendar whose Jan 1 is closest to the Chinese New Year Day .
        calender (str): version of Chinese calendar. Only support the calendars listed in available_calendars() below.
        ephemeris: ephemeris used to compute the moon phases and solar term. It's either 'DE431' or 'DE441'.
    Return: String that can be displayed nicely using HTML(string)
    """
    return print_Chinese_year_html(self, y, calendar, ephemeris)
  
  def chinese_to_western_date(self, y, m, d, calendar='default', ephemeris='None'):
    """
    Given a Chinese date (year = y, month = m, date = d), convert to the date in the Western calendar
    Input:
      y, m, d (int): year, month and day in the Chinese calendar (negative m indicates a leap month).
      calender (str): version of Chinese calendar. Only support the calendars listed in available_calendars() below.
      ephemeris: ephemeris used to compute the moon phases and solar term. It's either 'DE431' or 'DE441'.
    Return:
      a dict or a python list of dicts (if the Chinese date corresponds to more than one dates) containing the information of the Western date.
    """
    # sanity check
    if y != math.floor(y):
      raise ValueError('y must be an integer')
    if m != math.floor(m):
      raise ValueError('m must be an integer')
    if d != math.floor(d):
      raise ValueError('d must be an integer')
    if calendar=='default' and (y < self.ybeg or y > self.yend):
      raise ValueError('y must be in ['+str(self.ybeg)+','+str(self.yend)+']')
    if abs(m) < 1 or abs(m) > 12:
      raise ValueError('|m| must be in [1, 12]')
    if d < 1 or d > 30:
      raise ValueError('d must be in [1, 30]')
    calendar_func = calendar_function_lookup(calendar, ephemeris)
    return chinese_to_western_date_lookup(self, y, m, d, calendar, calendar_func)
  
  def chinese_to_western_year(self, y, m=None, calendar='default', ephemeris='None'):
      """
      Given a Chinese year y, return the Western dates in all days in the year if m is None or Western dates in all days in month m in the Western calendar.
      Input: 
        y (int): year in the Chinese calendar.
        m (int): None if request all days in year y. If 1 <= |m| <= 12, return dates in month m (negative denotes a leap month) in year y.
        calender (str): version of Chinese calendar. Only support the calendars listed in available_calendars() below.
      Return:
        a python list of dicts containing the information of the Western dates in the Chinese year/month.
      """
      if y != math.floor(y):
        raise ValueError('y must be an integer')
      if calendar=='default' and (y < self.ybeg or y > self.yend):
        raise ValueError('y must be in ['+str(self.ybeg)+','+str(self.yend)+']')
      y = int(y)
      if m is not None:
        if abs(m) != math.floor(abs(m)):
          raise ValueError('|m| must be an integer between 1 and 12.')
        if abs(m) < 1 or abs(m) > 12:
          raise ValueError('|m| must be an integer between 1 and 12.')
      calendar_func = calendar_function_lookup(calendar, ephemeris)
      return chinese_year_to_western_date_lookup(self, y, m, calendar, calendar_func)
  
  def chinese_to_western_year_html(self, y, m = None, calendar='default', 
                                   showJDN=False, ephemeris='None', 
                                   show_chinese_year_info=True,
                                   show_chinese_calendar_info=True):
    """
    Same as chinese_to_western_year() but return an HTML text.
    """
    if y != math.floor(y):
        raise ValueError('y must be an integer')
    if calendar=='default' and (y < self.ybeg or y > self.yend):
        raise ValueError('y must be in ['+str(self.ybeg)+','+str(self.yend)+']')
    y = int(y)
    if m is not None:
      if abs(m) != math.floor(abs(m)):
        raise ValueError('|m| must be an integer between 1 and 12.')
      if abs(m) < 1 or abs(m) > 12:
        raise ValueError('|m| must be an integer between 1 and 12.')
      
    calendar_func = calendar_function_lookup(calendar, ephemeris)
    cy = calendar_func(self, y)
    jd0 = getJDm(y-1, 12, 31)
    if m is None:
      jd1 = jd0 + cy['cm'][0]['d']
      jd2 = jd0 + cy['cm'][-1]['d'] + cy['cm'][-1]['n']
    else:
      cm = [x for x in cy['cm'] if x['cm']==m]
      if len(cm)==0:
        raise ValueError('The required Chinese month does not exist in the '+calendar+' calendar.')
      jd1 = jd0 + cm[0]['d']
      jd2 = jd0 + cm[-1]['d'] + cm[-1]['n']
    f1o3 = 1.0/3 # time difference between UT+8 and UT in days
    # get moon phases and solar terms
    ephemeris = self.set_ephemeris(ephemeris)
    st, mp = self.sm.st_mp_jd(jd1 - f1o3, jd2 - f1o3)
    # get calendrical solar terms
    calst = []
    datongST = []
    if y < 1734 or calendar != 'default':
      # calst: [(st_label, jdn), ...] 
      calst = self.get_calendrical_solar_terms(calendar, jd1, jd2)
      if calendar=='default':
        if y > 1666 and y < 1671:
          # calculate Datong solar terms
          datongST = self.get_calendrical_solar_terms('Datong', jd1, jd2)

    inp = {'calendar':calendar, 'y':y, 'm':m, 'cy':cy, 'jdy':int(jd0+0.6), 'showJDN':showJDN, 
             'st':st, 'mp':mp, 'show_chinese_year_info':show_chinese_year_info, 
             'show_chinese_calendar_info':show_chinese_calendar_info}
    if len(calst) > 0: inp['calst'] = calst
    if len(datongST) > 0: inp['datongST'] = datongST

    if m is None:
      del inp['m']
      return print_Chinese_yearly_calendar_html(self, inp)
    else:
      return print_Chinese_monthly_calendar_html(self, inp)

  def western_to_chinese_date(self, y, m, d, calendar='default', multiple_calendars=False, ephemeris='None'):
    """
    Given a Western date (year = y, month = m, date = d), convert to the date in Chinese calendar
    Input: 
      y, m, d (int): year, month and day in the Western calendar.
      calender (str): version of Chinese calendar. Only support the calendars listed in available_calendars() below.
      multiple_calendars (bool): This is only relevant if calendar=='default'. If True, return Chinese dates in all versions of Chinese calendars available at the given Western date.
    Return:
      a dict or a python list of dicts (if calendar is 'default' and multiple_calendars is True) containing the information of the Chinese date.
    """
    if y != math.floor(y):
      raise ValueError('y must be an integer')
    if m != math.floor(m):
      raise ValueError('m must be an integer')
    if d != math.floor(d):
      raise ValueError('d must be an integer')
    if calendar=='default' and (y < self.ybeg or y > self.yend):
      raise ValueError('y must be in ['+str(self.ybeg)+','+str(self.yend)+']')
    if m < 1 or m > 12:
      raise ValueError('m must be in [1, 12]')
    if d < 1 or d > 31:
      raise ValueError('d must be in [1, 31]')
    if y==1582 and m==10 and d > 4 and d < 15:
      raise ValueError("Date cannot be between Oct 5, 1582 and Oct 14, 1582. Use Julian date on and before Oct 4, 1582 and Gregorian date on and after Oct 15, 1582.")
    y = int(y); m = int(m); d = int(d);
    # Calculate the Julian date at noon
    jdn = int(math.floor(getJDm(y,m,d) + 0.6))
    # Calculate the Julian date at noon on Dec 31, y-1
    jd0 = int(math.floor(getJDm(y-1,12,31) + 0.6))
    dd = jdn - jd0 # Number of days from Jan 0, y

    if calendar=='default':
      cdate = western_to_chinese_date_lookup(self, y, dd, jdn, 'default', default_Chinese_year_data)
      if multiple_calendars:
        return add_additional_calendars(self, y, dd, jdn, cdate)
      else:
        return cdate
      
    # calendars other than 'default'
    calendar_func = calendar_function_lookup(calendar, ephemeris)
    return western_to_chinese_date_lookup(self, y, dd, jdn, calendar, calendar_func)
    
  def western_to_chinese_year(self, y, m = None, calendar='default', ephemeris='None'):
      """
      Given a Western year y, return the Chinese dates in all days in the year if m is None or Chinese dates in all days in month m in the Western calendar.
      Input: 
        y (int): year in the Western calendar.
        m (int): None if request all days in year y. If 1 <= m <= 12, return dates in month m in year y.
        calender (str): version of Chinese calendar. Only support the calendars listed in available_calendars() below.
      Return:
        a python list of dicts containing the information of the Chinese dates in the year.
      """
      if y != math.floor(y):
        raise ValueError('y must be an integer')
      if calendar=='default' and (y < self.ybeg or y > self.yend):
        raise ValueError('y must be in ['+str(self.ybeg)+','+str(self.yend)+']')
      y = int(y)
      if m is not None:
        if m != math.floor(m):
          raise ValueError('m must be an integer between 1 and 12.')
        if m < 1 or m > 12:
          raise ValueError('m must be an integer between 1 and 12.')
        
      # Calculate the beginning and end of the the Julian dates at noon 
      if m is None:
        jdn1 = int(math.floor(getJDm(y,1,1) + 0.6))
        jdn2 = int(math.floor(getJDm(y+1,1,1) + 0.6))
      else:
        m = int(m)
        jdn1 = int(math.floor(getJDm(y,m,1) + 0.6))
        jdn2 = int(math.floor(getJDm(y+1,1,1) + 0.6)) if m==12 else int(math.floor(getJDm(y,m+1,1) + 0.6))

      jdn = np.arange(jdn1, jdn2)
      calendar_func = calendar_function_lookup(calendar, ephemeris)
      return western_to_chinese_date_lookup_batch(self, jdn, calendar, calendar_func)
      
  def western_to_chinese_year_html(self, y, m = None, calendar='default', 
                                   showJDN=False, ephemeris='None', 
                                   show_chinese_year_info=True,
                                   show_chinese_calendar_info=True):
    """
    Same as western_to_chinese_year() but return an HTML text.
    """
    dates = self.western_to_chinese_year(y, m, calendar)
    if m is None:
      jd1 = getJDm(y,1,1)
      jd2 = getJDm(y+1,1,1)
    else:
      jd1 = getJDm(y, m, 1)
      jd2 = getJDm(y, m+1, 1) if m != 12 else getJDm(y+1, 1, 1)
    f1o3 = 1.0/3 # time difference between UT+8 and UT in days
    # get moon phases and solar terms
    ephemeris = self.set_ephemeris(ephemeris)
    st, mp = self.sm.st_mp_jd(jd1 - f1o3, jd2 - f1o3)
    # get calendrical solar terms
    calst = []
    datongST = []
    if y < 1734 or calendar != 'default':
      calst = self.get_calendrical_solar_terms(calendar, jd1, jd2)
      # reformat calst: [(st_label, jdn), ...] -> [(st_lable, [y, m, d]), ...]
      calst = reformat_calendrical_solar_term_tuples(self, calst)
      if calendar=='default':
        if y > 1666 and y < 1671:
          # calculate Datong solar terms
          datongST = self.get_calendrical_solar_terms('Datong', jd1, jd2)
          datongST = reformat_calendrical_solar_term_tuples(self, datongST)

    inp = {'calendar':calendar, 'y':y, 'm':m, 'dates':dates, 'showJDN':showJDN, 
             'st':st, 'mp':mp, 'show_chinese_year_info':show_chinese_year_info, 
             'show_chinese_calendar_info':show_chinese_calendar_info}
    if len(calst) > 0: inp['calst'] = calst
    if len(datongST) > 0: inp['datongST'] = datongST

    if m is None:
      del inp['m']
      return print_Western_year_html(self, inp)
    else:
      return print_Western_month_html(self, inp)
      
  def get_calendrical_solar_terms(self, calendar, jd1, jd2, ephemeris='None'):
    """
    Retrieve calendrical solar terms for the UT+8 Julian date in the range [jd1, jd2]
    Input:
      calendar: version of Chinese calendar; must be one of the keys in available_calendrical_solar_terms(cal).
    Return: 
      list of tuples [(lab1, jdn1), (lab2, jdn2), ...] where lab1, lab2, ... are the lables of the solar terms (e.g. 'J1', 'Z4') and jdn1, jdn2, ... are the Julian dates at noon of the solar terms.
    """
    li = available_calendrical_solar_terms(self, ephemeris)
    if calendar in li:
        sterm_func = li[calendar]
    else:
        raise ValueError('Calendar '+calendar+' is not supported.')
    
    # Convert jd1 and jd2 to years
    jd_to_wyear = lambda x: np.floor(np.where(x < 2299160.5, (x+0.5)/365.25 - 4712, (x - 2451544.5)/365.2425 + 2000))
    y1 = int(math.floor(jd_to_wyear(jd1)))
    y2 = int(math.floor(jd_to_wyear(jd2)))
    lab = ['J12', 'Z12', 'J1', 'Z1', 'J2', 'Z2', 'J3', 'Z3', 'J4', 'Z4', 'J5', 'Z5', 'J6', 'Z6', 'J7', 'Z7', 'J8', 'Z8', 'J9', 'Z9', 'J10', 'Z10', 'J11', 'Z11']
    if calendar=='default' and y1 < self.ybeg: 
        raise ValueError('Requested jd1 is out of range.')
    if calendar=='default' and y2 > self.yend+1:
        raise ValueError('Requested jd2 is out of range.')
    jd = sterm_func(y1)
    st = list(zip(lab, jd))
    if jd[0] - jd1 > 10:
        jd = sterm_func(y1-1)
        st = list(zip(lab, jd)) + st
    for y in range(y1+1, y2+1):
        jd = sterm_func(y)
        st += list(zip(lab, jd))
    if jd2 - st[-1][1] > 10:
        jd = sterm_func(y2+1)
        st += list(zip(lab, jd))
    return [x for x in st if x[1] >= jd1 and x[1] <= jd2]
  
  def calendrical_solar_terms(self, y, calendar="default", ephemeris='None'):
    """
    Retrieve calendrical solar terms in Western year y.
    Input:
      y (int): Western year
      calendar (str): version of Chinese calendar; must be one of the keys in available_calendrical_solar_terms().
    Output:
      list of dicts with keys 'solar term'/節氣/节气 for the name of the solar term and 'date'/'日期' for the UT+8 Western date of the solar term. For the default calendar and y in [1667, 1670], the keys are 'solar term'/節氣/节气, 'Xinfa'/'西洋新法' (for the UT+8 Western date of Xinfa's solar term), and 'Datong'/'大統曆'/'大统历' (for the UT+8 Western date of solar term based on the Datong system).
    """
    if y != math.floor(y):
      raise ValueError('y must be an integer')
    if calendar=='default' and (y < self.ybeg or y > self.yend):
      raise ValueError('Requested Western year is out of range.')
    if calendar=='Chunqiu' or (y < -479 and calendar=='default'):
      raise ValueError('There is no calendrical solar terms for the Chunqiu calendar.')
    li = available_calendrical_solar_terms(self, ephemeris)
    if calendar in li:
        sterm_func = li[calendar]
    else:
        raise ValueError('Calendar '+calendar+' is not supported.')
    
    jd1 = int(getJDm(y, 1, 1) + 0.6)
    jd2 = int(getJDm(y+1, 1, 1) + 0.6)
    lab = ['J12', 'Z12', 'J1', 'Z1', 'J2', 'Z2', 'J3', 'Z3', 'J4', 'Z4', 'J5', 'Z5', 'J6', 'Z6', 'J7', 'Z7', 'J8', 'Z8', 'J9', 'Z9', 'J10', 'Z10', 'J11', 'Z11']
    jdst_ym1 = sterm_func(y-1)
    jdsty = sterm_func(y)
    jdst_y1 = sterm_func(y+1)
    calst = [(self.stermName[lab[i]], jdst_ym1[i]) for i in range(24) if jdst_ym1[i] >= jd1 and jdst_ym1[i] < jd2]
    calst += [(self.stermName[lab[i]], jdsty[i]) for i in range(24) if jdsty[i] >= jd1 and jdsty[i] < jd2]
    calst += [(self.stermName[lab[i]], jdst_y1[i]) for i in range(24) if jdst_y1[i] >= jd1 and jdst_y1[i] < jd2]
    calst_list = []
    sterm = {'Eng':'solar term', 'ChiT':'節氣', 'ChiS':'节气'}
    qi = sterm[self.lang]
    if calendar=='default' and (y > 1666 and y < 1671):
      xinfa = 'Xinfa' if self.lang=='Eng' else '西洋新法'
      datong = 'Datong' if self.lang=='Eng' else ('大統曆' if self.lang=='ChiT' else '大统历')
      datongST = compute_pingqi(y, 'Datong')
      for i,x in enumerate(calst):
        st = {}
        st[qi] = x[0]
        d = CalDat(x[1])
        st[xinfa] = self.wmonthName[d['mm']-1] + self.wdayName[d['dd']-1]
        d['dd'] += datongST[i] - x[1]
        st[datong] = self.wmonthName[d['mm']-1] + self.wdayName[d['dd']-1]
        calst_list += [st]
    else:
      date = 'date' if self.lang=='Eng' else '日期'
      for x in calst:
        st = {}
        st[qi] = x[0]
        d = CalDat(x[1])
        st[date] = self.wmonthName[d['mm']-1] + self.wdayName[d['dd']-1]
        calst_list += [st]
    return calst_list
      
def available_calendars(ephemeris):
  """
  Return a dict of available calendars. The value of the key is the function that returns a dictionary with keys 'cm', 'calendar', and (optional) 'regign/era' (see the doc string of e.g. default_Chinese_year_data() for detail)
  """
  li = {'default':default_Chinese_year_data, 'Chunqiu':chunqiu_cmonth,
        'Shu':Shu_year_data, 'Wu':Wu_year_data, 'LaterQin':LaterQin_year_data, 
        'NorthernLiang':NorthernLiang_year_data, 'WeiZhouSui':WeiZhouSui_year_data, 
        'WeiQi':WeiQi_year_data, 'LiaoJinYuan':LiaoJinMongol_year_data, 
        'SouthernMing':SouthernMing_year_data}
  li['Zhou'] = lambda cal, y: guliuli_calendar_cmonth(cal, y, 'Zhou')
  li['Yin'] = lambda cal, y: guliuli_calendar_cmonth(cal, y, 'Yin')
  li['Lu'] = lambda cal, y: guliuli_calendar_cmonth(cal, y, 'Lu')
  li['Huangdi'] = lambda cal, y: guliuli_calendar_cmonth(cal, y, 'Huangdi')
  li['Xia1'] = lambda cal, y: guliuli_calendar_cmonth(cal, y, 'Xia1')
  li['Xia2'] = lambda cal, y: guliuli_calendar_cmonth(cal, y, 'Xia2')
  li['Zhuanxu'] = lambda cal, y: guliuli_calendar_cmonth(cal, y, 'Zhuanxu')
  li['Sifen'] = lambda cal, y: pingshou_noZhongqi_cmonth(cal, y, 'Sifen', '')
  li['Qianxiang'] = lambda cal, y: pingshou_noZhongqi_cmonth(cal, y, 'Qianxiang', '')
  li['Sanji'] = lambda cal, y: pingshou_noZhongqi_cmonth(cal, y, 'Sanji', '')
  li['Xuanshi'] = lambda cal, y: pingshou_noZhongqi_cmonth(cal, y, 'Xuanshi', '')
  li['Jingchu'] = lambda cal, y: pingshou_noZhongqi_cmonth(cal, y, 'Jingchu', '')
  li['Zhengguang'] = lambda cal, y: pingshou_noZhongqi_cmonth(cal, y, 'Zhengguang', '')
  li['fakeMingKeRang'] = lambda cal, y: pingshou_noZhongqi_cmonth(cal, y, 'fakeMingKeRang', '')
  li['Tianhe'] = lambda cal, y: pingshou_noZhongqi_cmonth(cal, y, 'Tianhe', '')
  li['Daxiang'] = lambda cal, y: pingshou_noZhongqi_cmonth(cal, y, 'Daxiang', '')
  li['Kaihuang'] = lambda cal, y: pingshou_noZhongqi_cmonth(cal, y, 'Kaihuang', '')
  li['Xinghe'] = lambda cal, y: pingshou_noZhongqi_cmonth(cal, y, 'Xinghe', '')
  li['Tianbao'] = lambda cal, y: pingshou_noZhongqi_cmonth(cal, y, 'Tianbao', '')
  li['GBT'] = lambda cal, y: GBT33661_2017_cmonth(cal, y, ephemeris)
  return li

def available_calendrical_solar_terms(cal, ephemeris):
  """
  Input: cal is the calendar object returned by calendar_conversion class.
  Return: a dict of available calendarical solar terms. The value of the key is the function sterm_func(y) that returns the Julian dates at noon of solar terms J12-Z11 in year y.
  """
  li = {'default':lambda y: calendrical_solar_terms_default(cal, y), 'Wu':calendrical_solar_terms_Wu, 
        'WeiZhouSui':calendrical_solar_terms_WeiZhouSui, 'WeiQi':calendrical_solar_terms_WeiQi, 
        'LiaoJinYuan':calendrical_solar_terms_LiaoJinYuan, 'SouthernMing':calendrical_solar_terms_SouthernMing}
  li['Zhou'] = lambda y: guliuli_solar_terms(y, 'Zhou')
  li['Yin'] = lambda y: guliuli_solar_terms(y, 'Yin')
  li['Lu'] = lambda y: guliuli_solar_terms(y, 'Lu')
  li['Huangdi'] = lambda y: guliuli_solar_terms(y, 'Huangdi')
  li['Xia1'] = lambda y: guliuli_solar_terms(y, 'Xia1')
  li['Xia2'] = lambda y: guliuli_solar_terms(y, 'Xia2')
  li['Zhuanxu'] = lambda y: guliuli_solar_terms(y, 'Zhuanxu')
  li['Shu'] = lambda y: compute_pingqi(y, 'Sifen')
  li['Sifen'] = lambda y: compute_pingqi(y, 'Sifen')
  li['Qianxiang'] = lambda y: compute_pingqi(y, 'Qianxiang')
  li['Sanji'] = lambda y: compute_pingqi(y, 'Sanji')
  li['LaterQin'] = lambda y: compute_pingqi(y, 'Sanji')
  li['Xuanshi'] = lambda y: compute_pingqi(y, 'Xuanshi')
  li['NorthernLiang'] = lambda y: compute_pingqi(y, 'Xuanshi')
  li['Jingchu'] = lambda y: compute_pingqi(y, 'Jingchu')
  li['Zhengguang'] = lambda y: compute_pingqi(y, 'Zhengguang')
  li['fakeMingKeRang'] = lambda y: compute_pingqi(y, 'fakeMingKeRang')
  li['Tianhe'] = lambda y: compute_pingqi(y, 'Tianhe')
  li['Daxiang'] = lambda y: compute_pingqi(y, 'Daxiang')
  li['Kaihuang'] = lambda y: compute_pingqi(y, 'Kaihuang')
  li['Xinghe'] = lambda y: compute_pingqi(y, 'Xinghe')
  li['Tianbao'] = lambda y: compute_pingqi(y, 'Tianbao')
  li['Xuanming'] = lambda y: compute_pingqi(y, 'Xuanming')
  li['RevisedDaming'] = lambda y: compute_pingqi(y, 'RevisedDaming')
  li['Datong'] = lambda y: compute_pingqi(y, 'Datong')
  li['GBT'] = lambda y: GBT33661_2017_solar_terms(cal, y, ephemeris)
  return li

def calendar_function_lookup(calendar, ephemeris):
  """
  Return the calendar function by looking up the available calendars in available_calendars().
  Input:
    calendar (str): name of calendar. If calendar is not in available_calendars(), raise a value error.
  Return:
    calendar function that can be used to gather the information of a Chinese year
  """
  li = available_calendars(ephemeris)
  if not (calendar in li):
    raise ValueError('Calendar '+calendar+' is not supported.')
  return li[calendar]    