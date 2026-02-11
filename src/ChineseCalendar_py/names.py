def moon_phases_names(lang):
  """
  return the names of the 4 phases New Moon, First Quarter, Full Moon and Third Quarter 
  in a language specified by the lang variable
  """
  if lang=='Eng':
    mp = ["New Moon", "First Quarter", "Full Moon", "Last Quarter"]
  else:
    mp = ["朔", "上弦", "望", "下弦"]
  keys = ['Q0', 'Q1', 'Q2', 'Q3']
  mpName = dict()
  for i, key in enumerate(keys):
    mpName[key] = mp[i]
  return mpName

def solar_term_name(lang):
  if lang=='Eng':
    st = 'solar term'
  elif lang=='ChiT':
    st = '節氣'
  else:
    st = '节气'
  return st

def time_name(lang):
  if lang=='Eng':
    t = 'time'
  elif lang=='ChiT':
    t = '時刻'
  else:
    t = '时刻'
  return t

def solar_terms_names(lang):
  """
  return the names of the 24 solar terms in a language specified by the lang variable
  """
  if lang=='Eng':
    st = ["Z11 (Dec. solstice)", "J12", "Z12", "J1", "Z1", "J2", 
          "Z2 (March equinox)", "J3","Z3", 
          "J4", "Z4", "J5", "Z5 (June solstice)", "J6", "Z6", "J7", "Z7", 
          "J8", "Z8 (Sep. equinox)", "J9", "Z9", "J10", "Z10", "J11"]
  elif lang=='ChiT':
    # traditional Chinese
    st = ["冬至", "小寒", "大寒", "立春", "雨水", "驚蟄", "春分", "清明", 
          "穀雨", "立夏", "小滿", "芒種", "夏至", "小暑", "大暑", "立秋", 
          "處暑", "白露", "秋分", "寒露", "霜降", "立冬", "小雪", "大雪"]
  else:
    # simplified Chinese
    st = ["冬至", "小寒", "大寒", "立春", "雨水", "惊蛰", "春分", "清明", 
          "谷雨", "立夏", "小满", "芒种", "夏至", "小暑", "大暑", "立秋", 
          "处暑", "白露", "秋分", "寒露", "霜降", "立冬", "小雪", "大雪"]
  keys = ["Z11", "J12", "Z12", "J1", "Z1", "J2", "Z2", "J3","Z3", "J4", "Z4", 
          "J5", "Z5", "J6", "Z6", "J7", "Z7", "J8", "Z8", "J9", "Z9", 
          "J10", "Z10", "J11"]
  stermName = dict()
  for i, key in enumerate(keys):
    stermName[key] = st[i]
  return stermName

def western_months_days(lang):
  if lang=='Eng':
    mon = ['Jan ', 'Feb ', 'Mar ', 'Apr ', 'May ', 'Jun ', 'Jul ', 'Aug ', 'Sep ', 'Oct ', 'Nov ', 'Dec ']
    day = [str(i) for i in range(1,32)]
  else:
    mon = [str(i)+'月' for i in range(1, 13)]
    day = [str(i)+'日' for i in range(1, 32)]
  return mon, day

def western_calendar_names(lang):
  if lang=='Eng':
    return ['Proleptic Julian', 'Julian', 'Gregorian']
  elif lang=='ChiT':
    return ['逆推儒略曆', '儒略曆', '格里曆']
  else:
    return ['逆推儒略历', '儒略历', '格里历']

def western_year_month_labels(lang):
  if lang=='Eng':
    return ['-', '-', '']
  else:
    return ['年', '', '']

def eclipse_names(lang):
  if lang=='Eng':
    solar = ['Partial solar eclipse', 'Annular solar eclipse', 'Total solar eclipse', 'Hybrid solar eclipse']
    lunar = ['Penumbral lunar eclipse', 'Partial lunar eclipse', 'Total lunar eclipse']
  elif lang=='ChiT':
    solar = ['日偏食', '日環食', '日全食', '日全環食']
    lunar = ['半影月食', '月偏食', '月全食']
  else:
    solar = ['日偏食', '日环食', '日全食', '日全环食']
    lunar = ['半影月食', '月偏食', '月全食']
  return solar, lunar

def week_names(lang):
  if lang=='Eng':
    week = ["Sun", "Mon", "Tue","Wed","Thu","Fri","Sat"]
  else:
    week = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]
  return week

def stem_branch_names(lang):
  if lang=='Eng':
    stem = ["Jia ","Yi ","Bing ","Ding ", "Wu ", "Ji ", "Geng ","Xin ","Ren ", "Gui "]
    branch = ['Zi', 'Chou', 'Yin', 'Mao', 'Chen', 'Si', 'Wu', 'Wei', 'Shen', 'You', 'Xu', 'Hai']
    branch_animal = ["Rat","Ox","Tiger","Rabbit","Dragon","Snake","Horse","Goat","Monkey","Chicken","Dog","Pig"]
  else:
    stem = ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"]
    branch = ["子","丑","寅","卯","辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    if lang=='ChiT':
      branch_animal = ["鼠", "牛", "虎", "兔", "龍", "蛇", "馬", "羊", "猴", "雞", "狗", "豬"]
    else:
      branch_animal = ["鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"]
  return stem, branch, branch_animal

def chinese_month_names(lang):
  # sep is the separator between month and day in the Chinese date string.
  # In Eng: sep = '-', the date string will look like '6-09'.
  # If ChiT and ChiS: '', the date string will look like '六月初九'
  if lang=='Eng':
    cmonthName = [str(i) for i in range(1,13)]
    leapName = 'leap '
    sep = '-'
  else:
    cmonthName = ["正月","二月","三月","四月","五月", "六月","七月","八月","九月","十月", "十一月","十二月"]
    leapName = '閏' if lang=='ChiT' else '闰'
    sep = ''
  return cmonthName, leapName, sep

def chinese_day_names(lang):
  if lang=='Eng':
    cday = ['0'+str(i) for i in range(1,10)] + [str(i) for i in range(10,31)]
  else:
    num = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十']
    cday = ['初'+num[i] for i in range(10)] + ['十'+num[i] for i in range(9)] + ['二十'] + ['廿'+num[i] for i in range(9)] + ['三十']
  return cday

def chinese_year_num_names(lang):
  if lang=='Eng':
    num = [' '+str(i) for i in range(1,70)]
  else:
    cnum = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十']
    num = ['元'] + [cnum[i] for i in range(1,10)] + ['十'+cnum[i] for i in range(9)] + ['二十']
    for k in range(1, 6):
      num += [cnum[k]+'十'+cnum[i] for i in range(9)]
      if k < 5:
        num += [cnum[k+1]+'十']
  return num

def historical_periods(lang):
  byears = [-723, -480, -220, -205, 9, 23, 25, 220, 265, 317, 420, 581, 618, 908, 960, 1280, 1368, 1645, 1912]
  if lang=='Eng':
    period = ['Spring and Autumn (722 BCE - 481BCE)', 'Warring States (480 BCE - 222 BCE)', 'Qin (221 BCE - 207 BCE)', 'Western Han (206 BCE - 8 CE)', 'Xin (9 - 23)', 'Gengshi (23 - 24)', 'Eastern Han (25 - 219)', 'Three Kingdoms (220-264)', 'Western Jin (265 - 316)', 'Eastern Jin (317 - 419)', 'Northern and Southern Dynasties (420 - 580)', 'Sui (581 - 617)', 'Tang (618 - 907)', 'Five Dynasties (907 - 959)', 'Song (960 - 1279)', 'Yuen (1280 - 1367)', 'Ming (1368 - 1644)', 'Qing (1645 - 1911)', 'Modern (1912 - )']
  elif lang=='ChiT':
    period = ['春秋 (前722 - 前481)', '戰國 (前480 - 前222)', '秦 (前221 - 前207)', '西漢 (前206 - 8)', '新 (9 - 23)', '更始 (23-24)', '東漢 (25 - 219)', '三國 (220 - 264)', '西晋 (265 - 316)', '東晋 (317 - 419)', '南北朝 (420 - 580)', '隋 (581 - 617)', '唐 (618 - 907)', '五代 (907 - 959)', '宋 (960 - 1279)', '元 (1280 - 1367)', '明 (1368 - 1644)', '清 (1645 - 1911)', '現代 (1912 - )']
  else:
    period = ['春秋 (前722 - 前481)', '战国 (前480 - 前222)', '秦 (前221 - 前207)', '西汉 (前206 - 8)', '新 (9 - 23)', '更始 (23-24)', '东汉 (25 - 219)', '三国 (220 - 264)', '西晋 (265 - 316)', '东晋 (317 - 419)', '南北朝 (420 - 580)', '隋 (581 - 617)', '唐 (618 - 907)', '五代 (907 - 959)', '宋 (960 - 1279)', '元 (1280 - 1367)', '明 (1368 - 1644)', '清 (1645 - 1911)', '现代 (1912 - )']
  return byears, period

def no_Zhongqi_label(lang):
  if lang=='Eng':
    return 'no Zhongqi'
  elif lang=='ChiT':
    return '無中氣'
  else:
    return '无中气'

def change_chinese_month_label(cal, cmonth, cyear, cyearData, ind, calendar):
  if calendar=='default' and (cal.lang=='ChiT' or cal.lang=='ChiS'):
    if cyear > 689 and cyear < 701:
      cm = cyearData['cm'][ind]['cm']
      if cm==11 and ind==0:
        return '正月'
      if cm==1:
        return '一月'
  if cyear < -220 and cyearData['cm'][ind]['cm']==-12:
    if cal.lang=='Eng':
      return 'leap month'
    else:
      return cal.leap + '月'
  if cyear < -103 and cyearData['cm'][ind]['cm']==-9:
    if cal.lang=='Eng':
      return 'post 9'
    elif cal.lang=='ChiT':
      return '後九月'
    else:
      return '后九月'
  return cmonth

def chinese_month_label(cal, cyear, cm, calendar):
  """
  Input: 
    cal: the object returned by the class calendar_conversion.
    cyear (int): Chinese year whose new year day is closest to Jan 1 of Western year.
    cm (int): Chinese month number
    calendar (string): Chinese calendar version.
  Return:
    Chinese month name in string
  """
  if cm < 0:
    cmonth = cal.leap + cal.cmonth[-cm-1]
  else:
    cmonth = cal.cmonth[cm-1]
  # change month label in special periods
  if calendar=='default' and (cal.lang=='ChiT' or cal.lang=='ChiS'):
    if cyear > 689 and cyear < 701:
      if cm==11: return '正月'
      if cm==1: return '一月'
  if cyear < -220 and cm==-12:
    if cal.lang=='Eng':
      return 'leap'
    else:
      return cal.leap + '月'
  if cyear < -103 and cm==-9:
    if cal.lang=='Eng':
      return 'post 9'
    elif cal.lang=='ChiT':
      return '後九月'
    else:
      return '后九月'
  return cmonth

def default_calendars_names(lang):
  cy = [-722, -479, -220, -103, -6, 85, 237, 445, 510, 590, 597, 619, 665, 729, 762, 784, 807, 822, 893, 939, 944, 956, 983, 1001, 1024, 1065, 1068, 1075, 1094, 1103, 1106, 1136, 1168, 1177, 1191, 1199, 1208, 1252, 1253, 1271, 1277, 1280, 1281, 1368, 1645, 1667, 1669, 1914, 1929, 1950, 2018]
  if lang=='Eng':
    calName = ['Chunqiu', 'Zhou', 'Qin and Early Han', 'Taichu', 'Santong', 'Sifen', 'Jingchu', 'Yuanjia', 'Daming', 'Kaihuang', 'Daye', 'Wuyinyuan', 'Linde', 'Dayan', 'Wuji', 'Guanxiang', 'Xuanming' ,'Chongxuan', 'Tiaoyuan', 'Chongxuan', 'Qintian', 'Yingtian', 'Qianyuan', 'Yitian', 'Chongtian', 'Mingtian', 'Chongtian', 'Fengyuan', 'Quantian' ,'Zhantian', 'Jiyuan', 'Tongyuan', 'Qiandao', 'Chunxi', 'Huiyuan', 'Tongtian', 'Kaixi', 'Chunyou', 'Huitian', 'Chengtian', 'Bentian', 'Revised Daming', 'Shoushi', 'Datong', 'Shixian', 'Datong', 'Shixian', 'Republic of China', 'Nationalist', 'Purple Mountain', 'Purple Mountain (GB/T 33661-2017)']
  elif lang=='ChiT':
    calName = ['春秋曆', '周曆', '秦漢顓頊曆', '太初曆', '三統曆', '四分曆', '景初曆', '元嘉曆', '大明曆', '開皇曆', '大業曆', '戊寅元曆', '麟德曆', '大衍曆', '五紀曆', '觀象曆', '宣明曆', '崇玄曆', '調元曆', '崇玄曆', '欽天曆', '應天曆', '乾元曆', '儀天曆', '崇天曆', '明天曆', '崇天曆', '奉元曆', '觀天曆', '占天曆', '紀元曆', '統元曆', '乾道曆', '淳熙曆', '會元曆', '統天曆', '開禧曆', '淳祐曆', '會天曆', '成天曆', '本天曆', '重修大明曆', '授時曆', '大統曆', '時憲曆', '大統曆', '時憲曆', '中華民國曆', '國民曆', '紫金曆', '紫金曆 (GB/T 33661-2017)']
  else:
    calName = ['春秋历', '周历', '秦汉颛顼历', '太初历', '三统历', '四分历', '景初历', '元嘉历', '大明历', '开皇历', '大业历', '戊寅元历', '麟德历', '大衍历', '五纪历', '观象历', '宣明历', '崇玄历', '调元历', '崇玄历', '钦天历', '应天历', '乾元历', '仪天历', '崇天历', '明天历', '崇天历', '奉元历', '观天历', '占天历', '纪元历', '统元历', '乾道历', '淳熙历', '会元历', '统天历', '开禧历', '淳佑历', '会天历', '成天历', '本天历', '重修大明历', '授时历', '大统历', '时宪历', '大统历', '时宪历', '中华民国历', '国民历', '紫金历', '紫金历 (GB/T 33661-2017)']
  return cy, calName
