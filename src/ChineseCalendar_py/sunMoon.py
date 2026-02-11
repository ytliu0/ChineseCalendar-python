import numpy as np
import pandas as pd
from .names import moon_phases_names, solar_terms_names, western_months_days, solar_term_name, time_name, eclipse_names
from .date_and_time import *
import importlib_resources

class sunMoon:
  """
  Class containing methods to retrieve the UT+8 times of moon phases and solar terms
  """
  def __init__(self, lang, ephemeris='DE441'):
    supported_ephemeris = ['DE431', 'DE441']
    match = sum([1 if ephemeris==x else 0 for x in supported_ephemeris])
    if match==0:
      raise ValueError('Ephemeris '+ephemeris+' is not supported!')
    supported_lang = ['Eng', 'ChiT', 'ChiS']
    match = sum([1 if lang==x else 0 for x in supported_lang])
    if match==0:
      raise ValueError('Language '+lang+' is not supported!')
    
    if ephemeris=='DE441':
      from .eclipse_links_DE441 import eclipse_year_range, solar_eclipse_link, lunar_eclipse_link
    else:
      from .eclipse_links_DE431 import eclipse_year_range, solar_eclipse_link, lunar_eclipse_link

    self.ephemeris = ephemeris
    self.dalpha = -0.116 if ephemeris=='DE441' else 0 # adjusted tidal acceleration
    self.lang = lang
    # beginning year of the eclipse data
    self.ec_ybeg = eclipse_year_range()[0]
    # load eclipse data
    self.solar_eclipses = solar_eclipse_link()
    self.lunar_eclipses = lunar_eclipse_link()
    
    # set names
    self.mpName = moon_phases_names(lang)
    self.stermName = solar_terms_names(lang)
    self.wmonthName, self.wdayName = western_months_days(lang)
    self.solarTermName = solar_term_name(lang)
    self.timeName = time_name(lang)
    self.solarEclipseName, self.lunarEclipseName = eclipse_names(lang)

    # read moon phase and solar term data file and set up data array
    infile = importlib_resources.files().joinpath('sunMoon_'+ephemeris+'.csv')
    smData = np.loadtxt(infile, delimiter=',', skiprows=1)
    self.ybeg = int(smData[0, 0] + 1)
    self.yend = int(smData[-1, 0] - 1)
    # remove first column
    self.smData = smData[:,1:]

  def st_mp(self, y):
    """
    Retrieve all solar terms and moon phases in Western year y
    Return: 2 lists: st, mp
      st: a list [[lab1, info1], [lab2, info2], ...] containing all solar terms in year y, where lab1, lab2, ... are the labels of the solar terms (e.g. 'J8', 'Z3') and info1, info2, ... are dictionaries containing the date and time information of the solar terms.
      mp: a list [[lab1, info1], [lab2, info2], ...] containing all moon phases in year y, where lab1, lab2, ... are the labels of the moon phases (e.g. 'Q0', 'Q3') and info1, info2, ... are dictionaries containing the date and time information of the moon phases.
    """
    if y != math.floor(y):
      raise ValueError('Requested year is not an integer!')
    if y < self.ybeg or y > self.yend:
      raise ValueError('Requested year must be in the range ['+str(self.ybeg)+','+str(self.yend)+']')
    krow = int(y) - self.ybeg + 1
    jd0_ym1, st_ym1, mp_ym1 = row_data_to_ut(self.smData[krow-1], self.dalpha)
    jd0_y, st_y, mp_y = row_data_to_ut(self.smData[krow], self.dalpha)
    jd0_y1, st_y1, mp_y1 = row_data_to_ut(self.smData[krow+1], self.dalpha)
    d0 = int(jd0_y - jd0_ym1 + 1e-3) 
    d1 = int(jd0_y1 - jd0_y + 1e-3)
    st_ym1 = [[x[0], x[1]-d0, x[2]] for x in st_ym1 if x[1] >= d0+1]
    mp_ym1 = [[x[0], x[1]-d0, x[2]] for x in mp_ym1 if x[1] >= d0+1]
    st_y1 = [[x[0], x[1]+d1, x[2]] for x in st_y1 if x[1] < 1]
    mp_y1 = [[x[0], x[1]+d1, x[2]] for x in mp_y1 if x[1] < 1]
    st = [x for x in st_y if x[1] >= 1 and x[1] < d1+1]
    mp = [x for x in mp_y if x[1] >= 1 and x[1] < d1+1]
    stb = st[0][1] # date of the first solar term in st
    mpb = mp[0][1] # date of the first moon phase in mp
    ste = st[-1][1] # date of the last solar term in st
    mpe = mp[-1][1] # date of the last moon phase in mp
    if len(st_ym1) > 0:
      st = [x for x in st_ym1 if x[1] < stb-0.1] + st
    if len(st_y1) > 0:
      st += [x for x in st_y1 if x[1] > ste+0.1]
    if len(mp_ym1) > 0:
      mp = [x for x in mp_ym1 if x[1] < mpb-0.1] + mp
    if len(mp_y1) > 0:
      mp += [x for x in mp_y1 if x[1] > mpe+0.1]

    st = self.reformat_list(st, jd0_y, 'st')
    mp = self.reformat_list(mp, jd0_y, 'mp')

    # eclipses 
    krow = int(y) - self.ec_ybeg # row number for year y in the eclipse data array
    # solarEclipses is a matrix of the form [[d1, ind1, type1], [d2, ind2, type2], ...], 
    # where the first column (d1, d2, ...) represents the number of days of a solar eclipse from Dec 31, y-1, 
    # the second column (ind1, ind2, ...) represents the solar-eclipse index used by my eclipse website, 
    # and the last column (type1, type2, ...) is a numerical representation of the eclipse type.
    solarEclipses = self.solar_eclipses[krow]
    extra = self.solar_eclipses[krow - 1]
    for x in extra:
      if d0 - x[0] < 3:
        # This is close of the beginning of y, add it to be safe
        solarEclipses += [[x[0]-d0, x[1], x[2]]]
    extra = self.solar_eclipses[krow + 1]
    for x in extra:
      if x[0] < 3:
        # This is close to the end of y, add it to be safe
        solarEclipses += [[x[0] + d1, x[1], x[2]]]
    # lunarEclipses is a matrix of the form [[d1, ind1, type1], [d2, ind2, type2], ...]. 
    # The columns contain the same information as in solarEclipses but they are for lunar eclipses.
    lunarEclipses = self.lunar_eclipses[krow]
    extra = self.lunar_eclipses[krow - 1]
    for x in extra:
      if d0 - x[0] < 3:
        # This is close of the beginning of y, add it to be safe
        lunarEclipses += [[x[0]-d0, x[1], x[2]]]
    extra = self.lunar_eclipses[krow + 1]
    for x in extra:
      if x[0] < 3:
        # This is close to the end of y, add it to be safe
        lunarEclipses += [[x[0] + d1, x[1], x[2]]]
    self.add_eclipse_info(mp, solarEclipses, lunarEclipses, y)

    return st, mp
  
  def st_mp_jd(self, jd1, jd2):
    """
    Retrieve all solar terms and moon phases whose UT Julian dates are in the range [jd1, jd2].
    Return: 2 lists: st, mp
      st: a list [[lab1, info1], [lab2, info2], ...] containing all solar terms in year y, where lab1, lab2, ... are the labels of the solar terms (e.g. 'J8', 'Z3') and info1, info2, ... are dictionaries containing the date and time information of the solar terms.
      mp: a list [[lab1, info1], [lab2, info2], ...] containing all moon phases in year y, where lab1, lab2, ... are the labels of the moon phases (e.g. 'Q0', 'Q3') and info1, info2, ... are dictionaries containing the date and time information of the moon phases.
    """
    jd_to_wyear = lambda x: np.floor(np.where(x < 2299160.5, (x+0.5)/365.25 - 4712, (x - 2451544.5)/365.2425 + 2000))
    jd1_tt = jd1 + get_dTT_UT(jd1, self.dalpha)
    jd2_tt = jd2 + get_dTT_UT(jd2, self.dalpha)
    y1 = int(math.floor(jd_to_wyear(jd1_tt)))
    y2 = int(math.floor(jd_to_wyear(jd2_tt)))
    st, mp = self.st_mp(y1)
    if st[0][1]['jd0_ut'] + st[0][1]['jd1_ut'] - jd1 > 10 or mp[0][1]['jd0_ut'] + mp[0][1]['jd1_ut'] - jd1 > 5:
      s, m = self.st_mp(y1-1)
      st = s + st
      mp = m + mp
    for y in range(y1+1, y2+1):
      s, m = self.st_mp(y)
      st += s
      mp += m
    if jd2 - st[0][1]['jd0_ut'] - st[0][1]['jd1_ut'] > 10 or jd2 - mp[0][1]['jd0_ut'] - mp[0][1]['jd1_ut'] > 5:
      s, m = self.st_mp(y2+1)
      st += s
      mp += m
    # Now filter out the solar terms and moon phases not in [jd1, jd2]
    st = [x for x in st if x[1]['jd0_ut'] + x[1]['jd1_ut'] >= jd1 and x[1]['jd0_ut'] + x[1]['jd1_ut'] <= jd2]
    mp = [x for x in mp if x[1]['jd0_ut'] + x[1]['jd1_ut'] >= jd1 and x[1]['jd0_ut'] + x[1]['jd1_ut'] <= jd2]
    return st, mp

  def st_mp_df(self, y):
    """
    Retrieve all solar terms and moon phases in Western year y and put them into pandas dataframes.
    Return: 2 pandas dataframes df_st and df_mp
      df_st: 2 columns, first column: name of solar term, second column: UT+8 time of solar term
      df_mp: 4 columns, 1st column stores the times of new moons, 2nd column stores the times of first quarters, 3rd column stores the times of full moons, 4th column stores the times of third quarters. New moons and full moons contain eclipse information with HTML tags. Use IPython.display.HTML(df_mp.to_html) to display the table properly in the Jupyter notebook.
    """
    st, mp = self.st_mp(y)
    Q0 = [x[1]['dateString']+', '+x[1]['timeString'] for x in mp if x[0]=='Q0']
    Q1 = [x[1]['dateString']+', '+x[1]['timeString'] for x in mp if x[0]=='Q1']
    Q2 = [x[1]['dateString']+', '+x[1]['timeString'] for x in mp if x[0]=='Q2']
    Q3 = [x[1]['dateString']+', '+x[1]['timeString'] for x in mp if x[0]=='Q3']
    # add eclipse info
    Q0d = [x[1] for x in mp if x[0]=='Q0']
    for i,x in enumerate(Q0d):
      if 'eclipse' in x:
        Q0[i] += '<br /><a href="'+x['eclipse url']+'">'+x['eclipse']+'</a>'
    Q2d = [x[1] for x in mp if x[0]=='Q2']
    for i,x in enumerate(Q2d):
      if 'eclipse' in x:
        Q2[i] += '<br /><a href="'+x['eclipse url']+'">'+x['eclipse']+'</a>'
    # mpb = 0 if the first moon phase is Q0, 1 if Q1, 2 if Q2, 3 if Q3
    mpb = int(mp[0][0][-1])
    if mpb > 0:
      Q0 = [' ']+Q0
    if mpb > 1:
      Q1 = [' ']+Q1
    if mpb > 2:
      Q2 = [' ']+Q2
    # mpe = 0 if the last moon phase is Q0, 1 if Q1, 2 if Q2, 3 if Q3
    mpe = int(mp[-1][0][-1])
    if mpe < 3:
      Q3 += [' ']
    if mpe < 2:
      Q2 += [' ']
    if mpe < 1:
      Q1 += [' ']
    df_mp = pd.DataFrame(np.transpose(np.array([Q0, Q1, Q2, Q3])), columns = list(self.mpName.values()))
    stName = [self.stermName[x[0]] for x in st]
    stTime = [x[1]['dateString']+', '+x[1]['timeString'] for x in st]
    df_st = pd.DataFrame(np.transpose(np.array([stName, stTime])), 
             columns = [self.solarTermName, self.timeName+' (UT+8)'])
    return df_st, df_mp
  
  def reformat_list(self, list, jd0, type):
    """
    Given a list [[lab1, ut1, e1], [lab2, ut2, e2], ...], return a new list [[lab1, info1], [lab2, info2], ...]. 
    lab1, lab2, ...: labels of solar terms or moon phases (e.g. 'Z3', 'Q2').
    ut1, ut2, ...:  UT+8 Julian dates - reference Jilian date returned by row_data_to_ut().
    e1, e2, ...: each of them is dictionary containing the UT+8 date and time information returned by row_data_to_ut().
    info1, info2, ...: dictionaries derived from e1, e2, ...
    """
    newList = ['']*len(list)
    ename = self.mpName if type=='mp' else self.stermName
    jd0_ut = math.floor(jd0) + 0.5
    f1o3 = 1.0/3
    for i, x in enumerate(list):
      info = {'event':ename[x[0]], 'year':x[2]['yy'], 'month':x[2]['mm'], 'date':x[2]['dd']}
      h = 24*(x[1] - math.floor(x[1])) + 0.5/60
      hh = math.floor(h)
      mm = math.floor(60*(h - hh))
      info['hour'] = hh
      info['minute'] = mm
      info['dateString'] = self.wmonthName[x[2]['mm']-1] + self.wdayName[x[2]['dd']-1]
      info['timeString'] = ('0'+str(hh))[-2:] + ':' + ('0'+str(mm))[-2:]
      info['jd0_ut'] = jd0_ut
      info['jd1_ut'] = x[1] - f1o3  # UT+8 -> UT
      newList[i] = [x[0], info]
    return newList

  def add_eclipse_info(self, mp, se, le, y):
    """
    Add eclipse information (if any) to new moons and full moons.
    Input:
      mp: a list [[lab1, info1], [lab2, info2], ...], where lab1, lab2, ... are moon-phase labels (e.g. 'Q0', 'Q3') and each of info1, info2, ... are dictionaries containing the date and time information of the moon phases.
      se: a matrix of the form [[d1, ind1, type1], [d2, ind2, type2], ...], where the first column (d1, d2, ...)represents the number of days of a solar eclipse from Dec 31, y-1, the second column (ind1, ind2, ...) represents the solar-eclipse index used by my eclipse website, and the last column (type1, type2, ...) is a numerical representation of the eclipse type.
      le: a list [[lab1, info1], [lab2, info2], ...] resembling se but it's for lunar eclipses.
      y: year
    Return: none, but the eclipse information (eclipse type and url) is added to the appropriate info dictionaries in the list mp.
    """
    for i, x in enumerate(mp):
      if x[0]=='Q0':
        for e in se:
          if abs(x[1]['jd1_ut'] - e[0]) < 5:
            ybeg = 1 + 100*math.floor(0.01*(y - 0.5))
            if y==ybeg and e[1] > 200: ybeg -= 100
            if y-ybeg==99 and e[1] < 200: ybeg += 100
            mp[i][1]['eclipse'] = self.solarEclipseName[e[2]]
            mp[i][1]['eclipse url'] = 'http://ytliu.epizy.com/eclipse/one_solar_eclipse_general.html?ybeg=' + str(ybeg) + '&ind=' + str(e[1]) + '&DE=' + self.ephemeris[-3:]+'&ref=python'
      if x[0]=='Q2':
        for e in le:
          if abs(x[1]['jd1_ut'] - e[0]) < 5:
            ybeg = 1 + 100*math.floor(0.01*(y - 0.5))
            if y==ybeg and e[1] > 200: ybeg -= 100
            if y-ybeg==99 and e[1] < 200: ybeg += 100
            mp[i][1]['eclipse'] = self.lunarEclipseName[e[2]]
            mp[i][1]['eclipse url'] = 'http://ytliu.epizy.com/eclipse/one_lunar_eclipse_general.html?ybeg=' + str(ybeg) + '&ind=' + str(e[1]) + '&DE=' + self.ephemeris[-3:] + '&shrule=revised_Danjon&ref=python'

def row_data_to_ut(row, dalpha):
  """
  Convert one row of solar-term, moon-phase times from TT to UT+8
  Return: jd0, st, mp
    jd0: reference Julian date
    st: a list containing [[lab1, s1, sdt1, ], [lab2, s2, sdt2], ...], where 
        lab1, lab2, ...: solar-term labels (e.g. 'J7', 'Z12')
        s1, s2, ...: UT+8 Julian dates - jd0 of the solar terms
        sdt1, sdt2, ...: each of them is a dictionary containing the UT+8 date and time information of a solar term.
    mp: a list containing [[lab1, m1, mdt1], [lab2, m2, mdt2], ...], where 
        lab1, lab2, ...: moon=phase labels (e.g. 'Q0', 'Q3') 
        m1, m2, ...: UT+8 Julian dates - jd0 of the moon phases
        mdt1, mdt2, ...:  each of them is a dictionary containing the UT+8 date and time information of a moon phase.
  """
  jd0 = row[0] # reference JD
  ut = [row[i] - get_dTT_UT(jd0+row[i], dalpha) for i in range(1,86)] # UT+8 dates 
  mp_lab = ['Q0', 'Q1', 'Q2', 'Q3']*15
  st_lab = ["Z11", "J12", "Z12", "J1", "Z1", "J2", "Z2", "J3","Z3", "J4", "Z4", 
        "J5", "Z5", "J6", "Z6", "J7", "Z7", "J8", "Z8", "J9", "Z9", 
        "J10", "Z10", "J11", "Z11"]
  lab = st_lab + mp_lab
  dt = 0.5 # add dt to convert floor(jd0)+ut from UT to UT+8
  ut_lab = [[lab[i], ut[i], CalDat(math.floor(jd0), ut[i]+dt)] for i in range(85)]
  st = [ut_lab[i] for i in range(25)]
  mp = [ut_lab[i+25] for i in range(60)]
  return jd0, st, mp
