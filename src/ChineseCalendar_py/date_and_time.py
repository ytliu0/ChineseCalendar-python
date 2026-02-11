import math
from .DeltaT_Stephenson_Morrison import DeltaT

# Compute JD at midnight at yyyy, mm, dd (year, month, date)
def getJDm(yyyy,mm,dd):
    m1 = mm; yy = yyyy;
    if m1 <= 2: 
       m1 +=12 
       yy -= 1
    if 10000*yy+100*m1+dd <= 15821004:
        # Julian calendar
        b = -2 + math.floor((yy+4716)/4) - 1179
    else:
        # Gregorian calendar
        b = math.floor(yy/400) - math.floor(yy/100) + math.floor(yy/4)
    JD0 = 365*yy + b + math.floor(30.6001*(m1+1)) + dd + 1720996.5
    return JD0

#----------------------------------------------------------
# CalDat: Calendar date and time from jd = jd0 + jd1 (|jd1| is assumed to be << jd0)
# 
# yy,mm,dd Calendar date components
# h, m, s hour, min, sec.
# 
# Ported from Astronomy on Personal Computer, p. 15-16
#-------------------------------------------------
def CalDat(jd0, jd1=0):
    # Convert Julian day number to calendar date
    jd = jd0 + jd1
    a = math.floor(jd+0.5)
    if a < 0:
        return CalDatNegativeJD(jd0, jd1)

    if a < 2299161: # Julian calendar
        b = 0; c = a+1524;
    else: # Gregorian calendar
        b = math.floor((a-1867216.25)/36524.25)
        c = a + b - math.floor(0.25*b) + 1525
    d = math.floor((c-122.1)/365.25)
    if d < 0:  
       d += 1
    e = 365*d + math.floor(0.25*d)
    f = math.floor((c-e)/30.6001)
    if f < 0: 
       f += 1
    dd = c-e - math.floor(30.6001*f)
    mm = f - 1 - 12*math.floor(f/14+1e-5)
    yy = d - 4715 - math.floor((7+mm)/10+1e-5)
    dateString = generateDateString(int(yy),int(mm),int(dd))
    FracOfDay = 0.5 + (jd0 - math.floor(jd0)) + (jd1 - math.floor(jd1))
    Hour = 24*(FracOfDay - math.floor(FracOfDay))
    h = int(Hour)
    m = int(60*(Hour-h))
    s = (Hour - h - m/60)*3600
    timeString = generateTimeString(h,m,s)
    return {'yy':yy, 'mm':mm, 'dd':dd, 'h':h, 'm':m, 's':s, \
           'dateString':dateString, 'timeString':timeString}

#----------------------------------------------------------
# CalDat: Calendar date and time from Julian date jd = jd0+jd1 with jd<0
# 
# yy,mm,dd Calendar date components
# h, m, s hour, min, sec.
# 
#-------------------------------------------------
def CalDatNegativeJD(jd0, jd1):
    jd = jd0 + jd1
    mjd = -math.floor(jd+0.5)
    md = mjd - math.floor(mjd/1461)
    dyear = math.floor(md/(365+1e-10)) + 1
    yyyy = -4712 - dyear
    mjd0 = dyear*365 + math.floor(dyear/4) + 1
    dFromY = mjd0 - mjd
    monthTable = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334, 365]
    if dyear % 4 ==0:
       monthTable = [0, 31, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335, 366]
    for i in range(13):
        if dFromY <= monthTable[i]:
            mm = i
            dd = dFromY - monthTable[i-1]
            break
    dateString = generateDateString(yyyy,mm,dd)
    FracOfDay = (jd0 - math.floor(jd0)) + 0.5 + (jd1 - math.floor(jd1))
    Hour = 24*(FracOfDay - math.floor(FracOfDay));
    h = int(Hour)
    m = int(60*(Hour-h))
    s = (Hour - h - m/60)*3600
    timeString = generateTimeString(h,m,s)
    return {'yy':yyyy, 'mm':mm, 'dd':dd, 'h':h, 'm':m, 's':s, 'dateString':dateString, 'timeString':timeString}

# Generate date string from yyyy, mm and dd:
# return yyyy-MMM-dd, MMM = [Jan, Feb, ..., Dec]
def generateDateString(yyyy,mm,dd):
    absy = '000'+str(abs(yyyy))
    yStr = absy[-4:] if yyyy >=0 else '-'+absy[-4:]
    mon = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
    mmString = mon[mm-1];
    ddString = str(dd) if dd >= 10 else '0'+str(dd)
    return yStr+"-"+mmString+"-"+ddString

# Generate time string from h,m,s: 
# return hh:mm:ss 
def generateTimeString(h,m,s):
    hround = h + m/60 + (s+0.5)/3600
    hh = math.floor(hround)
    mm = math.floor((hround-hh)*60)
    ss = math.floor(3600*(hround-hh-mm/60))
    hh = '0'+str(hh); mm = '0'+str(mm); ss = '0'+str(ss);
    return hh[-2:]+":"+mm[-2:]+":"+ss[-2:]

def get_DeltaT(jd, dalpha, method='sm'):
    """
    Calculate Delta T from a given jd
    Input: jd - Julian date number, method: method used to calculate Delta T.
           Only the 'sm' method (Stephenson et al 2016 & Morrison et al 2021) 
           is currently supported.
    Output: Delta T in days.
    """
    if (method != 'sm'): 
       raise ValueError('Method '+method+' not supported in get_DeltaT()')
    y = (jd + 0.5)/365.25 - 4712 if jd < 2299160.5 else (jd - 2451544.5)/365.2425 + 2000
    return DeltaT(y, dalpha)/86400

def get_dTT_UT(jd_TT, dalpha, jd_up = 2461771.5):
    """
    Given TT Julian date jd_TT, calculate jd_TT - jd_UT, where 
    UT is UT1 for year < 1972 and UTC for 1972 <= year <= year_up and 
    projected UTC for year > year_up. 
    Use UT1 as projected UTC for year > year_up.
    """
    if jd_TT < 2441317.5 or jd_TT > jd_up: return get_DeltaT(jd_TT, dalpha)
    # use leap second table to compute TT - UTC
    # jd_lepas_UT = [2441133.5, 2441499.5, 2441683.5, 2442048.5, 2442413.5, 2442778.5, 
    #             2443144.5, 2443509.5, 2443874.5, 2444239.5, 2444786.5, 2445151.5, 
    #             2445516.5, 2446247.5, 2447161.5, 2447892.5, 2448257.5, 2448804.5, 
    #             2449169.5, 2449534.5, 2450083.5, 2450630.5, 2451179.5, 2453736.5, 
    #             2454832.5, 2456109.5, 2457204.5, 2457754.5]
    # n = len(jd_lepas_UT)
    # jd_leaps_TT = [jd_lepas_UT[i] + (42.184+i)/86400 for i in range(n)]
    # Instead of doing the calculation every time, simply do it once and copy the result:
    jd_leaps_TT = [2441133.5004882407, 2441499.5004998147, 2441683.5005113888, 2442048.500522963, 2442413.5005345372, 2442778.5005461113, 2443144.5005576853, 2443509.5005692593, 2443874.5005808333, 2444239.5005924073, 2444786.5006039813, 2445151.5006155553, 2445516.50062713, 2446247.500638704, 2447161.500650278, 2447892.500661852, 2448257.500673426, 2448804.500685, 2449169.500696574, 2449534.5007081483, 2450083.5007197224, 2450630.5007312964, 2451179.5007428704, 2453736.5007544444, 2454832.5007660184, 2456109.5007775924, 2457204.500789167, 2457754.500800741]
    dtt_ut1 = 41.184 + len([1 for jds in jd_leaps_TT if jd_TT > jds])
    return dtt_ut1/86400

def NdaysGregJul(y):
    """
    return the number of days in a Gregorian/Julian year
    """
    ndays = 355 if y==1582 else 365 + (1 if abs(y) % 4 == 0 else 0)
    if y > 1582:
        ndays += (-1 if y % 100 == 0 else 0) + (1 if y % 400 == 0 else 0)
    return ndays

def generateTimeStringFromH(h, ds=-1):
    """
    Generate time string from number of hours from midlight h.
    Input:
      h (float): hours from midlight.
      ds (int): ds = 0: h -> hh:mm.m, ds = 1: h -> hh:mm:ss
    Output:
      if ds==-1:
        return time string of the form 'hh:mm'
      elif ds==0:
        return time string of the form 'hh:mm.m'
      elif ds==1:
        return time string of the form 'hh:mm:ss'
      else
        return time string of the form 'hh:mm:ss.s'
    """
    h -= 24*math.floor(h/24)
    hround = h + (0.5/60 if ds==-1 else (0.05/60 if ds==0 else (0.5/3600 if ds==1 else 0.05/3600)))
    hh = math.floor(hround)
    if ds==-1:
        mm = math.floor(60*(hround - hh))
        hh = '0'+str(hh) if hh < 10 else str(hh)
        mm = '0'+str(mm) if mm < 10 else str(mm)
        return hh+':'+mm
    if ds==0:
        mm = 0.1*math.floor(600*(hround - hh))
        ms = str(round(mm,1))
        hh = str(hh)
        if len(hh) < 2: 
            hh = '0'+hh
        mm = '0'+ms if mm < 10 else ms
        return hh+':'+mm
    mm = math.floor((hround-hh)*60)
    sss = int(math.floor(36000*(hround-hh-mm/60)))
    ss = sss // 10
    decs = sss % 10
    hh = str(hh); mm = str(mm); ss = str(ss);
    if len(hh) < 2: hh = '0'+hh
    if len(mm) < 2: mm = '0'+mm
    if len(ss) < 2: ss = '0'+ss
    if ds==2: ss += '.'+str(decs)
    return hh+':'+mm+':'+ss

def sexagenary_month_from_cyear_jian(cyear):
    """
    Given a Chinese year cyear, calculate the sexagenary month cycle based on jian in 
    the 12 Chinese months following the Xia standard. The last one 'NA' is reserved for a leap month.
    """
    cyear_stem = (cyear + 726) % 10 # stem number of cyear
    # The sexagenary number of the first month in a jia year is Bing Yin (3). 
    # The sexagenary number of the months cyear can then be calculated by 
    # the number of months counting from the jia year
    cm_sex0 = 12*cyear_stem + 2
    return [str(1 + ((cm_sex0 + i) % 60)) for i in range(12)] + ['NA']