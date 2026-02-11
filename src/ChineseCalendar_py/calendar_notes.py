from .names import solar_terms_names, western_months_days, chinese_day_names

# Calendar notes at the bottom of Gregorian month m/Chinese month cm in year y.
def monthly_calendarNotes(y, m, lang, calendar, cm=-9999):
    if y < 618: 
        return monthly_calendarNotesBefore618(y, m, lang, calendar, cm)
    if calendar=='default' and y > 617 and y < 908: 
        return monthly_calendarNotesTang(y, m, lang, cm)
    if calendar=='default' and y > 1367 and y < 1645: 
        return monthly_calendarNotesMing(y, m, lang, cm)
    if calendar=='default' and y > 1644 and y < 1912: 
        return monthly_calendarNotesQing(y, m, lang, cm)
    if calendar=='SouthernMing': 
        return monthly_calendarNotesSouthernMing(y, m, lang, cm)
    if calendar=='default' and y > 1911 and y < 1980: 
        return monthly_calendarNotes1912_1979(y, m, lang, cm)
    if calendar=='default' and y > 2050:
        return monthly_calendarNotesAfter2050(y, m, lang, cm)
    return ''

def monthly_calendarNotesBefore618(y, m, lang, calendar, cm):
    note = ''
    # Han calendar reform
    if calendar=='default' and y==-103 and (m==6 or cm==4):
        if lang=='Eng':
            note = 'New calendar is displayed starting from month 5. The lunar conjunction day was one day earlier than that of the old calendar, turning month 4 into a short month.'
        elif lang=='ChiT':
            note = '五月起的日曆依太初曆，朔日比舊曆早一日，使四月變成小月。'
        else:
            note = '五月起的日历依太初历，朔日比旧历早一日，使四月变成小月。'

    # Xin dynasty
    if calendar=='default' and y==9 and (m==1 or cm==1):
        if lang=='Eng':
            note = 'The chou month was supposed to be month 12. It became month 1 by edict. Hence, there was no month 12 in the Chinese year Wu chen.'
        elif lang=='ChiT':
            note = '本來十二月是建丑，改正朔後建丑變成正月，所以戊辰年沒有十二月。'
        else:
            note = '本来十二月是建丑，改正朔后建丑变成正月，所以戊辰年没有十二月。'
    if calendar=='default' and y==23 and (m > 1 and m < 12):
        month_numChi = ["正","二","三","四","五","六","七","八","九","十", "十一","十二"]
        cdates_eng = ['February 10th', 'March 11th', 'April 10th', 'May 9th', 'June 8th', 'July 7th', 'August 6th', 'September 4th', 'October 4th', 'November 2nd']
        cdates_chi = ['2月10日', '3月11日', '4月10日', '5月9日', '6月8日', '7月7日', '8月6日', '9月4日', '10月4日', '11月2日']
        msg = {'Eng':cdates_eng[m-2]+' was the first day of month '+str(m)+' in the Xin calendar and the first day of month '+str(m-1)+' in the Gengshi calendar.',
               'ChiT':cdates_chi[m-2]+'是地皇四年'+month_numChi[m-1]+'月初一、更始元年'+month_numChi[m-2]+'月初一。', 
               'ChiS':cdates_chi[m-2]+'是地皇四年'+month_numChi[m-1]+'月初一、更始元年'+month_numChi[m-2]+'月初一。'}
        note = msg[lang]
    if calendar=='default' and y==23 and (cm > 1 and cm < 12):
        month_numChi = ["正","二","三","四","五","六","七","八","九","十", "十一","十二"]
        cdates_eng = ['February 10th', 'March 11th', 'April 10th', 'May 9th', 'June 8th', 'July 7th', 'August 6th', 'September 4th', 'October 4th', 'November 2nd']
        cdates_chi = ['2月10日', '3月11日', '4月10日', '5月9日', '6月8日', '7月7日', '8月6日', '9月4日', '10月4日', '11月2日']
        msg = {'Eng':cdates_eng[cm-2]+' was the first day of month '+str(cm)+' in the Xin calendar and the first day of month '+str(cm-1)+' in the Gengshi calendar.',
               'ChiT':cdates_chi[cm-2]+'是地皇四年'+month_numChi[cm-1]+'月初一、更始元年'+month_numChi[cm-2]+'月初一。', 
               'ChiS':cdates_chi[cm-2]+'是地皇四年'+month_numChi[cm-1]+'月初一、更始元年'+month_numChi[cm-2]+'月初一。'}
        note = msg[lang]
    if calendar=='default' and y==23 and (m==12 or cm==12):
        if lang=='Eng':
            note = 'December 2nd was the first day of month 12 in the Xin calendar and the first day of month 11 in the Genshi calendar; December 31st was the first day of month 12 in the Genshi calendar.'
        else:
            note = '12月2日是地皇四年十二月初一、更始元年十一月初一。12月31日是更始元年十二月初一。'
    
    # Wei dynasty
    if calendar=='default' and ((y==237 and m==2) or (y==236 and cm==12)):
        if lang=='Eng':
            note = 'Note that month 12 had only 28 days. This was due to the adoption of a new version of calendar in month 1. There are discrepancies between the data in the main text and Appendix 2 in the book <i>3500 Years of Calendars and Astronomical Phenomena</i>. The main text uses the new calendar in month 1, but Appendix 2 uses the new calendar in month 6. Here the data in the main text are used, in which the first days of each month before month 6 are one day earlier.'
        elif lang=='ChiT':
            note = '由於新曆法(景初曆)於正月初一開始使用，十二月只有二十八日。《三千五百年历日天象》的正文與其附表2的資料不合，正文在正月改用景初曆，附表2在六月才改曆。這裡用正文的數據，在六月前的朔日都比附表2早一日。'
        else:
            note = '由于新历法(景初历)于正月初一开始使用，十二月只有二十八日。《三千五百年历日天象》的正文与其附表2的资料不合，正文在正月改用景初历，附表2在六月才改历。这里用正文的数据，在六月前的朔日都比附表2早一日。'
    if calendar=='default' and y==237 and (m==4 or cm==4):
        if lang=='Eng':
            note = 'The chen month was supposed to be month 3. It became month 4 by edict. Hence, there was no month 3 in this Chinese year.'
        elif lang=='ChiT':
            note = '本來三月是建辰，改正朔後變成四月，所以丁巳年沒有三月。'
        else:
            note = '本来三月是建辰，改正朔后变成四月，所以丁巳年没有三月。'
    cond = (y==239 and m==12) or (y==240 and m < 3) or (y==239 and cm==12)
    if calendar=='default' and cond:
        if lang=='Eng':
            note = 'Since month 1 was to switch back to be the yin month in the year Geng shen, there were two month 12s in the year Ji wei. The first one was the zi month and the second one was the chou month. These two month 12s should not be confused as they can be distinguished by their sexagenary month cycles.'
        elif lang=='ChiT':
            note = '庚申年的正月恢復為建寅，己未年的農曆有兩個十二月:建子和建丑。由於已註明了月干支，兩個十二月應不會被混淆。'
        else:
            note = '庚申年的正月恢复为建寅，己未年的农历有两个十二月:建子和建丑。由于已注明了月干支，两个十二月应不会被混淆。'

    # Wu dynasty
    if calendar=='Wu' and y==238 and (m==11 or cm==-10):
        if lang=='Eng':
            note = 'In Appendix 2 of the book <i>3500 Years of Calendars and Astronomical Phenomena</i>, the sexagenary day of the leap month conjunction is listed as ji chou, corresponding to Nov. 25. This is at odds with my calculation. The result of my calculation is consistent with the data on the <a href="http://sinocal.sinica.edu.tw/" target="_blank">Chinese-Western calendar conversion website</a> created by Academia Sinica in Taiwan. The preface of the book says that the calendar data in its appendices are based on the book 《歷代長術輯要》(<i>Compilation of Historical Calendars</i>) by Wang Yuezhen (汪曰楨). I looked at the book and found that the date listed there was also the same as my calculation. I suspect that the date listed in <i>3500 Years of Calendars and Astronomical Phenomena</i> is wrong. The book also lists the sexagenary day of the month 11 conjunction as ji chou, which is certainly wrong since this date was far away from the new moon close to the beginning of month 11.'
        elif lang=='ChiT':
            note = '《三千五百年历日天象》附表2記閏十月己丑朔和十一月己丑朔。十一月己丑朔無疑是錯的，這裡列出的閏十月戊子朔是根據我的推步，結果與台灣中央研究院的<a href="http://sinocal.sinica.edu.tw/" target="_blank">兩千年中西曆轉換網站</a>一致，《三千五百年历日天象》前言說其附表參照清汪曰楨的《歷代長術輯要》，翻查此書發現亦記閏十月戊子。'
        else:
            note = '《三千五百年历日天象》附表2记闰十月己丑朔和十一月己丑朔。十一月己丑朔无疑是错的，这里列出的闰十月戊子朔是根据我的推步，结果与台湾中央研究院的<a href="http://sinocal.sinica.edu.tw/" target="_blank">两千年中西历转换网站</a>一致，《三千五百年历日天象》前言说其附表参照清汪曰桢的《历代长术辑要》，翻查此书发现亦记闰十月戊子。'

    # Southern and Northern dynasties
    if calendar=='WeiZhouSui' and y==447 and (m==12 or cm==11):
        if lang=='Eng':
            note = "According to <i>Index to Comprehensive Mirror to Aid in Governmance</i>, the month 11 conjunction occurred on a jia xu day (Dec. 23). However, in <i>Compilation of Historical Calendars</i> by Wang Yuezhen, the month 12 conjunction was listed on a jia xu day and is at odds with its statement that the winter solstice occurred on a jia xu day in month 11. The month 12 conjunction on a jia xu day is certainly a typo because a jia xu day was 29 days (or 89 days) after a yi si day, which was the leap month 10 conjunction date. So jia xu day could only be the month 11 conjunction date. In <i>3500 Years of Calendars and Astronomical Phenomena</i> by Zhang Peiyu and <i>Tables of Historical Lunar Conjunctions and Leap Months</i> by Chen Yuan, the month 11 conjunction is mistakenly listed on Dec. 24. They were probably misled by Wang's typo. The book <i>A Sino-Western Calendar For Two Thousand Years (1-2000)</i> by Hsueh Chung-San and Ouyang Yi correctly places the month 11 conjunction on Dec. 23. Surprisingly, the <a href='http://sinocal.sinica.edu.tw/' target='_blank'>Chinese-Western calendar conversion website</a> created by Academia Sinica in Taiwan, whose ancient calendar data are based on <i>A Sino-Western Calendar For Two Thousand Years (1-2000)</i>, does not follow the book and mistakenly places the month 11 conjunction on Dec. 24."
        elif lang=='ChiT':
            note = '《通鑑目錄》記十一月甲戌朔，汪曰楨《歷代長術輯要》卻記「十乙亥、十二甲戌朔、閏十(十甲辰小雪、十一甲戌冬至)」，沒有記閏十月朔和十一月朔干支就是說兩朔日的天干和都是乙，但是「十二甲戌」是錯的，因為閏十朔是乙巳，而甲戌在乙巳後29日(或89日)，絕不可能是十二月朔，而且與其「十一甲戌冬至」相悖，可見「十二甲戌朔」應是「十一甲戌朔」之誤，「十二甲戌朔」是宋曆而非魏曆。張培瑜《三千五百年历日天象》和陳垣《二十史朔閏表》可能被《歷代長術輯要》誤導，記十一月乙亥朔及十二月甲辰朔。薛仲三、歐陽頤的《兩千年中西曆對照表》則沒有錯，奇怪的是臺灣中央研究院的<a href="http://sinocal.sinica.edu.tw/" target="_blank">兩千年中西曆轉換</a>卻不跟從《兩千年中西曆對照表》，也弄錯了十一月朔的日期。'
        else:
            note = '《通鉴目录》记十一月甲戌朔，汪曰桢《历代长术辑要》却记「十乙亥、十二甲戌朔、闰十(十甲辰小雪、十一甲戌冬至)」，没有记闰十月朔和十一月朔干支就是说两朔日的天干和都是乙，但是「十二甲戌」是错的，因为闰十朔是乙巳，而甲戌在乙巳后29日(或89日)，绝不可能是十二月朔，而且与其「十一甲戌冬至」相悖，可见「十二甲戌朔」应是「十一甲戌朔」之误，「十二甲戌朔」是宋历而非魏历。张培瑜《三千五百年历日天象》和陈垣《二十史朔闰表》可能被《历代长术辑要》误导，记十一月乙亥朔及十二月甲辰朔。薛仲三、欧阳颐的《两千年中西历对照表》则没有错，奇怪的是台湾中央研究院的<a href="http://sinocal.sinica.edu.tw/" target="_blank">两千年中西历转换</a>却不跟从《两千年中西历对照表》，也弄错了十一月朔的日期。'
    if calendar=='default' and y==502 and (m==6 or cm==-5):
        if lang=='Eng':
            note = 'There is a discrepancy between the main text and Appendix 3 in the book <i>3500 Years of Calendars and Astronomical Phenomena</i>. The leap month in this year is listed as after month 5 in the main text but after month 4 in Appendix 3.'
        elif lang=='ChiT':
            note = '《三千五百年历日天象》的正文與其附表3的資料不一致，正文記這年閏五月，附表3則為閏四月。'
        else:
            note = '《三千五百年历日天象》的正文与其附表3的资料不一致，正文记這年闰五月，附表3则为闰四月。'
    if calendar=='default' and y==575 and (m==9 or cm==-8):
        if lang=='Eng':
            note = 'There is a discrepancy between the main text and Appendix 3 in the book <i>3500 Years of Calendars and Astronomical Phenomena</i>. The leap month in this year is listed as after month 8 in the main text but after month 9 in Appendix 3.'
        elif lang=='ChiT':
            note = '《三千五百年历日天象》的正文與其附表3的資料不一致，正文記這年閏八月，附表3則為閏九月。'
        else:
            note = '《三千五百年历日天象》的正文与其附表3的资料不一致，正文记這年闰八月，附表3则为闰九月。'
    if calendar=='WeiQi' and y==575 and (m==9 or cm==-8):
        if lang=='Eng':
            note = "Appendix 3 of the book <i>3500 Years of Calendars and Astronomical Phenomena</i> lists the leap month as after month 9. This is at odds with my calculation, which agrees with the data on the <a href='http://sinocal.sinica.edu.tw/' target='_blank'>Chinese-Western calendar conversion website</a> created by Academia Sinica in Taiwan. The data in Appendix 3 are supposed to be based on the book 《歷代長術輯要》(<i>Compilation of Historical Calendars</i>) by Wang Yuezhen (汪曰楨), but that book also lists the leap month as after month 8. That's why I use my calculation here."
        elif lang=='ChiT':
            note = '《三千五百年历日天象》附表3記這年北齊閏九月，與我計算的閏八月不一致，台灣中央研究院的<a href="http://sinocal.sinica.edu.tw/" target="_blank">兩千年中西曆轉換網站</a>和汪曰楨的《歷代長術輯要》也記這年閏八月，所以這裡不取《三千五百年历日天象》的數據。'
        else:
            note = '《三千五百年历日天象》附表3记这年北齐闰九月，与我计算的闰八月不一致，台湾中央研究院的<a href="http://sinocal.sinica.edu.tw/" target="_blank">两千年中西历转换网站</a>和汪曰桢的《历代长术辑要》也记这年闰八月，所以这里不取《三千五百年历日天象》的数据。'
        
    return note

def monthly_calendarNotesTang(y, m, lang, cm):
    note = ''
    if y==678 and (m==11 or m==12 or cm==11 or cm==-11):
        if lang=='Eng':
            note = 'The <i>Old Book of Tang</i> mentions leap month 10 in this year. However, the <i>New Book of Tang</i> mentions leap month 11. Many scholars adopt the data in the <i>New Book of Tang</i>. However, Huang Yi-Long, Professor in the Institute of History at the National Tsing-Hua University in Taiwan, <a href="http://ccsdb.ncl.edu.tw/ccs/image/01_010_002_01_11.pdf" target="_blank">investigated the issue</a> and concludes that the record in the <i>Old Book of Tang</i> is more reliable. His analysis places leap month 10 beginning on Nov. 19 and month 11 beginning on Dec. 19.'
        elif lang=='ChiT':
            note = '《舊唐書》有閏十月的記載，《新唐書》卻有閏十一月記載，學者一般取《新唐書》的閏月。但台灣國立清華大學歷史研究所的黃一農教授經過<a href="http://ccsdb.ncl.edu.tw/ccs/image/01_010_002_01_11.pdf" target="_blank">考證</a>後認為《舊唐書》的記載比較可信。根據他的考證，閏十月朔是癸丑(11月19日)，十一月朔是癸未(12月19日)。'
        else:
            note = '《旧唐书》有闰十月的记载，《新唐书》却有闰十一月记载，学者一般取《新唐书》的闰月。但台湾国立清华大学历史研究所的黄一农教授经过<a href="http://ccsdb.ncl.edu.tw/ccs/image/01_010_002_01_11.pdf" target="_blank">考证</a>后认为《旧唐书》的记载比较可信。根据他的考证，闰十月朔是癸丑(11月19日)，十一月朔是癸未(12月19日)。'
    if y==684 and (m==1 or cm==1):
        if lang=='Eng':
            note = 'The New Year day was supposed to be on Jan 22, but it was moved to Jan 23 by edict.'
        elif lang=='ChiT':
            note = '正月朔本在癸未(1月22日)，但唐高宗在弘道元年八月下旨，強將十二月改為大月，使正月朔移至甲申(1月23日)。'
        else:
            note = '正月朔本在癸未(1月22日)，但唐高宗在弘道元年八月下旨，强将十二月改为大月，使正月朔移至甲申(1月23日)。'
    if (y==697 and m==12) or (y==698 and cm==11):
        if lang=='Eng':
            note = 'The calendrical winter solstice was originally on Dec. 18, but Empress Consort Wu changed several calendar dates by edict. It was claimed that several predicted conjunction dates in the previous years were incorrect, resulting in the Moon being visible on the last days of lunar months. The claim was in fact incorrect and was a pretense for the empress to change calendar dates so that the winter solstice would fall on the jia zi day (Dec. 20) and coincide with the lunar conjunction. After an "investigation", it was decided that the winter solstice should be moved to the jia zi day (Dec. 20), which "happened to coincide" with the lunar conjunction. Because of this change, the lunar month started on Nov. 20 became a leap month and the winter solstice became the New Year day. There was originally a leap month after month 12. It had to be changed to month 12. In order to do that, the major solar term Z12 was moved from Jan 17, 698 to Jan 18, 698.'
        elif lang=='ChiT':
            note = '曆書冬至本在壬戌(12月18日)，閏十月本為正月，但武則天為了營造正月甲子合朔冬至之罕見曆象，七月下詔強行更改曆日。詔書偽稱曆官所推合朔時刻有不合天象，出現了「晦仍見月，有爽天經」之象，經「重更尋討」後「果差一日」，於是強將原本所推冬至移後二日為正月甲子合朔冬至，使原本的正月變為閏十月，為了除消原本所推的閏十二月，又強將大寒由壬辰(698年1月17日，正月廿九)推遲一日至癸巳(698年1月18日，十二月初一)。'
        else:
            note = '历书冬至本在壬戌(12月18日)，闰十月本为正月，但武则天为了营造正月甲子合朔冬至之罕见历象，七月下诏强行更改历日。诏书伪称历官所推合朔时刻有不合天象，出现了「晦仍见月，有爽天经」之象，经「重更寻讨」后「果差一日」，于是强将原本所推冬至移后二日为正月甲子合朔冬至，使原本的正月变为闰十月，为了除消原本所推的闰十二月，又强将大寒由壬辰(698年1月17日，正月廿九)推迟一日至癸巳(698年1月18日，十二月初一)。'
    if y==698 and (m==1 or cm==12):
        if lang=='Eng':
            note = 'The calendrical Z12 was originally on Jan. 17 (the day day of month 11), but was changed to Jan. 18 in order to cancel a leap month originally calculated but was moved to after the 10th month of the previous year.'
        elif lang=='ChiT':
            note = '曆書大寒本在壬辰(1月17日，正月廿九)，曆官強行移後一日以除消原本所推的閏月。'
        else:
            note = '历书大寒本在壬辰(1月17日，正月廿九)，历官强行移后一日以除消原本所推的闰月。'
    if (y==725 and m==1) or (y==724 and cm==-12):
        if lang=='Eng':
            note = 'The conjunction on Jan 19 was supposed to be the New Year day for the Chinese year in 725. However, in order to prevent a solar eclipse on the New Year day, the leap month was moved to a month earlier by edict and became the last month in the Chinese year in 724 and the New Year day was moved to Feb 18, 725.'
        elif lang=='ChiT':
            note = '丙辰朔本是開元十三年正月朔，為避正旦日食，當時強將閏月推前一月，使正月丙辰朔變閏十二月丙辰朔，閏正月丙戌朔(2月18日)變正月丙戌朔。'
        else:
            note = '丙辰朔本是开元十三年正月朔，为避正旦日食，当时强将闰月推前一月，使正月丙辰朔变闰十二月丙辰朔，闰正月丙戌朔(2月18日)变正月丙戌朔。'
    if y==725 and (m==2 or cm==1):
        if lang=='Eng':
            note = 'The month associated with the conjunction on Feb 18 was supposed to be a leap month, but the leap month was moved to a month earlier in order to prevent a solar eclipse on the New Year day. As a result, the Feb 18 conjunction became the New Year day. The calendrical Z1 was also moved from Feb 16 to Feb 18 to be consistent with the change.'
        elif lang=='ChiT':
            note = '丙戌朔本是閏正月朔，為避正旦日食，當時強將閏月推前一月，故閏正月朔變為正月朔。曆書雨水(當時稱為啟蟄)本在甲申(2月16日)，亦強進為丙戌(2月18日)。'
        else:
            note = '丙戌朔本是闰正月朔，为避正旦日食，当时强将闰月推前一月，故闰正月朔变为正月朔。历书雨水(当时称为启蛰)本在甲申(2月16日)，亦强进为丙戌(2月18日)。'
    if (y==761 and m==12) or (y==762 and cm==1):
        if lang=='Eng':
            note = 'The zi month was supposed to be month 11, but it became month 1 by edict. There were no months 11 and 12 in the year Xin chou'
        elif lang=='ChiT':
            note = '本來建子是十一月，改正朔後變成正月。辛丑年沒有十一和十二月。'
        else:
            note = '本来建子是十一月，改正朔后变成正月。辛丑年没有十一和十二月。'
    if y==762 and m==4:
        if lang=='Eng':
            note = 'Note that there was a second month 4 and second month 5 this year because it was decided that after the first month 5, the month numbers were switched back to the yin month being month 1, mao month being month 2, chen being month 3, si month being month 4 and so on. As a result, there were two month 4s and two month 5s in this Chinese year. They can be distinguished by their sexagenary month cycles.'
        elif lang=='ChiT':
            note = '五月之後的那個月是四月。這是因為五月後正朔改回以建寅為正月、建卯為二月、建辰為三月、建巳為四月等。農曆壬寅年因此有兩個四月（建卯和建巳）和兩個五月（建辰和建午）。由於已註明月干支，這些重複的月份應不會被混潸。'
        else:
            note = '五月之后的那个月是四月。这是因为五月后正朔改回以建寅为正月、建卯为二月、建辰为三月、建巳为四月等。农历壬寅年因此有两个四月（建卯和建巳）和两个五月（建辰和建午）。由于已注明月干支，这些重复的月份应不会被混潸。'
    return note

def monthly_calendarNotesMing(y, m, lang, cm):
    note = ''
    
    # Gregorian calendar reform
    if y==1582 and (m==10 or cm==9):
        if lang=='Eng':
            note = 'Note that October 4 was followed by October 15 because of the Gregorian calendar reform.'
        elif lang=='ChiT':
            note = '由於格里高里曆改，10月4日的下一日是10月15日，跳了10日。'
        else:
            note = '由于格里高里历改，10月4日的下一日是10月15日，跳了10日。'

    if y==1462 and (m==11 or cm==11):
        if lang=='Eng':
            note = '<i>3500 Years of Calendars and Astronomical Phenomena</i> lists the first day of month 11 on Nov. 22, which is inconsistent with the calendar issued by the Ming government (Nov. 21).'
        elif lang=='ChiT':
            note = '《三千五百年历日天象》記十一月壬辰朔(11月22日)，不合當年的《大統曆》曆書(辛卯朔, 11月21日)，見<a href="http://ccsdb.ncl.edu.tw/ccs/image/01_010_002_01_11.pdf" target="_blank">「中國史曆表朔閏訂正舉隅 &mdash; 以唐《麟德曆》行用時期為例」</a>緒言。'
        else:
            note = '《三千五百年历日天象》记十一月壬辰朔(11月22日)，不合当年的《大统历》历书(辛卯朔, 11月21日), 见<a href="http://ccsdb.ncl.edu.tw/ccs/image/01_010_002_01_11.pdf" target="_blank">「中国史历表朔闰订正举隅 &mdash; 以唐《麟德历》行用时期为例」</a>绪言。'
    if y==1581 and (m==10 or cm==10):
        if lang=='Eng':
            note = '<i>3500 Years of Calendars and Astronomical Phenomena</i> lists the first day of month 10 on Oct. 28, which is inconsistent with the calendar issued by the Ming government (Oct. 27).'
        elif lang=='ChiT':
            note = '《三千五百年历日天象》記十月壬辰朔(10月28日)，不合當年的《大統曆》曆書(辛卯朔, 10月27日)，見《國家圖書館藏明代大統曆日彙編》第三冊第606頁。'
        else:
            note = '《三千五百年历日天象》记十月壬辰朔(10月28日)，不合当年的《大统历》历书(辛卯朔, 10月27日)，见《国家图书馆藏明代大统历日汇编》第三册第606页。'
    if y==1588 and (m==3 or cm==3):
        if lang=='Eng':
            note = '<i>3500 Years of Calendars and Astronomical Phenomena</i> lists the first day of month 3 on Mar. 26, which is inconsistent with the calendar issued by the Ming government (Mar. 27).'
        elif lang=='ChiT':
            note = '《三千五百年历日天象》記三月癸未朔(3月26日)，不合<a href="http://catalog.digitalarchives.tw/item/00/07/ec/c9.html" target="_blank">當年的《大統曆》曆書</a>(甲申朔, 3月27日)。'
        else:
            note = '《三千五百年历日天象》记三月癸未朔(3月26日)，不合<a href="http://catalog.digitalarchives.tw/item/00/07/ec/c9.html" target="_blank">当年的《大统历》历书</a>(甲申朔, 3月27日)。'
    if y==1588 and (m==4 or cm==4):
        if lang=='Eng':
            note = '<i>3500 Years of Calendars and Astronomical Phenomena</i> lists the first day of month 4 on Apr. 25, which is inconsistent with the calendar issued by the Ming government (Apr. 26).'
        elif lang=='ChiT':
            note = '《三千五百年历日天象》記四月癸丑朔(4月25日)，不合<a href="http://catalog.digitalarchives.tw/item/00/07/ec/c9.html" target="_blank">當年的《大統曆》曆書</a>(甲寅朔, 4月26日)。'
        else:
            note = '《三千五百年历日天象》记四月癸丑朔(4月25日)，不合<a href="http://catalog.digitalarchives.tw/item/00/07/ec/c9.html" target="_blank">当年的《大统历》历书</a>(甲寅朔, 4月26日)。'
    if (y==1589 and m==1) or (y==1588 and cm==12):
        if lang=='Eng':
            note = '<i>3500 Years of Calendars and Astronomical Phenomena</i> lists the first day of month 12 on Jan. 17, which is inconsistent with the calendar issued by the Ming government (Jan. 16).'
        elif lang=='ChiT':
            note = '《三千五百年历日天象》記十二月庚辰朔(1月17日)，不合當年的《大統曆》曆書(己卯朔, 1月16日)，見《國家圖書館藏明代大統曆日彙編》第四冊第175頁。'
        else:
            note = '《三千五百年历日天象》记十二月庚辰朔(1月17日)，不合当年的《大统历》历书(己卯朔, 1月16日)，见《国家图书馆藏明代大统历日汇编》第四册第175页。'
    if y==1600 and (m==2 or cm==1):
        if lang=='Eng':
            note = '<i>3500 Years of Calendars and Astronomical Phenomena</i> lists the New Year day on Feb. 14, which is inconsistent with the calendar issued by the Ming government (Feb. 15).'
        elif lang=='ChiT':
            note = '《三千五百年历日天象》記正月乙巳朔(2月14日)，不合當年的《大統曆》曆書(丙午朔, 2月15日)，見《國家圖書館藏明代大統曆日彙編》第四冊第445頁。'
        else:
            note = '《三千五百年历日天象》记正月乙巳朔(2月14日)，不合当年的《大统历》历书(丙午朔, 2月15日)，见《国家图书馆藏明代大统历日汇编》第四册第445页。'
    if y==1609 and (m==2 or cm==1):
        if lang=='Eng':
            note = '<i>3500 Years of Calendars and Astronomical Phenomena</i> lists the New Year day on Feb. 4, which is inconsistent with the calendar issued by the Ming government (Feb. 5).'
        elif lang=='ChiT':
            note = '《三千五百年历日天象》記正月癸未朔(2月4日)，不合當年的《大統曆》曆書(甲申朔, 2月5日)，見《國家圖書館藏明代大統曆日彙編》第五冊第67頁。'
        else:
            note = '《三千五百年历日天象》记正月癸未朔(2月4日)，不合当年的《大统历》历书(甲申朔, 2月5日)，见《国家图书馆藏明代大统历日汇编》第五册第67页。'
            
    return note

def monthly_calendarNotesQing(y, m, lang, cm):
    note = ''

    if y==1645 and (m==7 or cm==-6):
        if lang=='Eng':
            note = 'Note that leap month 6 contained the major solar term Z6, breaking the rule that a leap month must not contain a major solar term. Wang Yuezhen (汪曰楨), a Chinese mathematician in the 19th century, explained that even though the solar term Z6 and the lunar conjunction associated with the month occurred on the same day, Z6 occurred earlier in the day than the lunar conjunction and was counted as a major solar term of the previous month. As a result, leap month 6 did not contain any major solar term. This "rule" was only used in this year. It was never used again after this year.'
        elif lang=='ChiT':
            note = '中氣大暑出現在閏六月初一，違反了閏月不含中氣的規定。清朝曆算家汪曰楨解釋說雖然大暑與朔發生在同一日，大暑的時刻早於合朔時刻，屬於前月之中氣，所以閏六月不含中氣。這說法明顯不合傳統，屬於新的置閏法則，但是這新法則只在這一年用過，以後不再使用。'
        else:
            note = '中气大暑出现在闰六月初一，违反了闰月不含中气的规定。清朝历算家汪曰桢解释说虽然大暑与朔发生在同一日，大暑的时刻早于合朔时刻，属于前月之中气，所以闰六月不含中气。这说法明显不合传统，属于新的置闰法则，但是这新法则只在这一年用过，以后不再使用。'
        return note
    if y==1662 and (m==2 or cm==1):
        if lang=='Eng':
            note = 'The Chinese New Year in 1662 was originally on Feb. 19. There was a leap month after month 7 in 1661 and two major solar terms (Z11 and Z12) in month 11. The major solar term Z1 was originally placed on the last day of month 12 in 1661, leaving the first month in 1662 without a major solar term. To avoid controversy, the New Year Day was moved to Feb. 18 so that the first month would contain Z1, thus moving the month without major solar term to the last month of 1661.'
        elif lang=='ChiT':
            note = '康熙元年正月初一本在丙子日(2月19日)，事緣順治十八年閏七月，當年十一月含冬至和大寒兩中氣，雨水本來定在十二月晦，但這使康熙元年正月不含中氣。為免遭人非議，欽天監將正月初一提前一日至乙亥日(2月18日)，使正月含雨水，無中氣月便移到十二月。'
        else:
            note = '康熙元年正月初一本在丙子日(2月19日)，事缘顺治十八年闰七月，当年十一月含冬至和大寒两中气，雨水本来定在十二月晦，但这使康熙元年正月不含中气。为免遭人非议，钦天监将正月初一提前一日至乙亥日(2月18日)，使正月含雨水，无中气月便移到十二月。'
        return note
    if y==1670 and (m==1 or cm==1):
        if lang=='Eng':
            note = 'The Chinese month that began on Jan 21 was a leap month according to the old calendar rule since it did not contain a major solar term. It was the first month of 1670 according to the new rule since it contained the major solar term Z1. In April 1669, the Kangxi Emperor abolished the old rule and ordered by decree to move the leap month from after the 12th month of 1669 to after the second month of 1670.'
        elif lang=='ChiT':
            note = '己丑朔(1月21日)對應的月份依舊法因不含中氣，為康熙八年閏十二月，依新法則含中氣雨水，為康熙九年正月。康熙帝在康熙八年三月下詔復用西洋新法，廢康熙八年閏十二月，改為康熙九年閏二月。'
        else:
            note = '己丑朔(1月21日)对应的月份依旧法因不含中气，为康熙八年闰十二月，依新法则含中气雨水，为康熙九年正月。康熙帝在康熙八年三月下诏复用西洋新法，废康熙八年闰十二月，改为康熙九年闰二月。'
        return note
    if y==1679 and (m==5 or cm==4):
        if lang=='Eng':
            note = "In both <i>3500 Years of Calendars and Astronomical Phenomena</i> (by Zhang Peiyu) and <i>A Chinese calendar translated into the western calendar from 1516 to 1941</i> (by Zheng Hesheng), the calendrical solar term Z4 is listed on May 20. However, the Shixian Calendar for the 18th year of Emperor Kangxi's Reign (i.e. Feb. 11, 1679 - Jan. 30, 1680), a yearly calendar issued by the Imperial Astronomical Bureau in the Qing dynasty, lists Z4 on May 21 at 9:01am in Beijing's local apparent solar time. The calendarical solar term for Z4 is listed on May 21 here based on the Shixian Calendar."
        elif lang=='ChiT':
            note = '張培瑜《三千五百年历日天象》和鄭鶴聲《近世中西史日對照表》皆記小滿為5月20日，但《大清康熙十八年歲次己未時憲曆》則載「(四月)十二日丙子巳初初刻一分小滿四月中」，即小滿在四月十二日(公曆5月21日)九時零一分(北京地方真太陽時)。這裡根據《大清時憲曆》記曆書小滿為公曆5月21日。'
        else:
            note = '张培瑜《三千五百年历日天象》和郑鹤声《近世中西史日对照表》皆记小满为5月20日，但《大清康熙十八年岁次己未时宪历》则载「(四月)十二日丙子巳初初刻一分小满四月中」，即小满在四月十二日(公历5月21日)九时零一分(北京地方真太阳时)。这里根据《大清时宪历》记历书小满为公历5月21日。'
        return note
    if y==1848 and m==12:
        if lang=='Eng':
            note = 'Z11 (December solstice) was on Dec 21 (11-26 in Chinese calendar) at 23:59:37 (UT1+8) according to the calculation using DE441. The calendrical Z11 was on Dec 22 (11-27).'
        elif lang=='ChiT':
            note = 'DE441曆表算出的冬至時刻在12月21日(十一月廿六)23:59:57 (UT1+8)，曆書冬至在12月22日(十一月廿七)。'
        else:
            note = 'DE441历表算出的冬至时刻在12月21日(十一月廿六)23:59:57 (UT1+8)，历书冬至在12月22日(十一月廿七)。'
        return note
    if y==1848 and cm==11:
        if lang=='Eng':
            note = 'Z11 (December solstice) was on 26d at 23:59:37 (UT1+8) according to the calculation using DE441. The calendrical Z11 was on 27d.'
        elif lang=='ChiT':
            note = 'DE441曆表算出的冬至時刻在廿六日23:59:57 (UT1+8)，曆書冬至在廿七日。'
        else:
            note = 'DE441历表算出的冬至时刻在廿六日23:59:57 (UT1+8)，历书冬至在廿七日。'
        return note
    
    # The calendrical solar terms after 1733 that didn't match solar terms computed by modern method
    # 'cmq', if present, means that the Chinese month of the solar term is in the month indicated by 
    # 'cmq' not 'cm'.
    items  = [{'y':1736, 'm':1, 's':'Z12', 'd':20, 'cy':1735, 'cm':12, 'cd':8},
              {'y':1739, 'm':1, 's':'J12', 'd':5, 'cy':1738, 'cm':11, 'cd':26},
              {'y':1744, 'm':7, 's':'Z6', 'd':22, 'cy':1744, 'cm':6, 'cd':13},
              {'y':1746, 'm':3, 's':'J2', 'd':5, 'cy':1746, 'cm':2, 'cd':14},
              {'y':1747, 'm':7, 's':'J6', 'd':7, 'cy':1747, 'cm':6, 'cmq':5, 'cd':30},
              {'y':1749, 'm':4, 's':'J3', 'd':4, 'cy':1749, 'cm':2, 'cd':18},
              {'y':1751, 'm':10, 's':'J9', 'd':9, 'cy':1751, 'cm':8, 'cd':21},
              {'y':1753, 'm':6, 's':'J5', 'd':5, 'cy':1753, 'cm':5, 'cd':4},
              {'y':1756, 'm':9, 's':'Z8', 'd':23, 'cy':1756, 'cm':8, 'cd':29},
              {'y':1760, 'm':4, 's':'Z3', 'd':19, 'cy':1760, 'cm':3, 'cd':4},
              {'y':1774, 'm':2, 's':'J1', 'd':3, 'cy':1773, 'cm':12, 'cd':23},
              {'y':1774, 'm':9, 's':'J8', 'd':8, 'cy':1774, 'cm':8, 'cd':3},
              {'y':1779, 'm':3, 's':'J2', 'd':5, 'cy':1779, 'cm':1, 'cd':18},
              {'y':1779, 'm':6, 's':'Z5', 'd':21, 'cy':1779, 'cm':5, 'cd':8},
              {'y':1781, 'm':12, 's':'J11', 'd':7, 'cy':1781, 'cm':10, 'cd':22},
              {'y':1782, 'm':4, 's':'J3', 'd':4, 'cy':1782, 'cm':2, 'cd':22},
              {'y':1784, 'm':10, 's':'J9', 'd':8, 'cy':1784, 'cm':8, 'cd':24},
              {'y':1787, 'm':2, 's':'Z1', 'd':18, 'cy':1787, 'cm':1, 'cd':1},
              {'y':1807, 'm':2, 's':'J1', 'd':4, 'cy':1806, 'cm':12, 'cd':27},
              {'y':1809, 'm':1, 's':'J12', 'd':5, 'cy':1808, 'cm':11, 'cd':20},
              {'y':1809, 'm':11, 's':'Z10', 'd':23, 'cy':1809, 'cm':10, 'cd':16},
              {'y':1812, 'm':3, 's':'J2', 'd':5, 'cy':1812, 'cm':1, 'cd':22},
              {'y':1815, 'm':4, 's':'J3', 'd':5, 'cy':1815, 'cm':2, 'cd':26},
              {'y':1817, 'm':10, 's':'J9', 'd':9, 'cy':1817, 'cm':8, 'cd':29},
              {'y':1820, 'm':2, 's':'Z1', 'd':19, 'cy':1820, 'cm':1, 'cd':6},
              {'y':1824, 'm':8, 's':'J7', 'd':8, 'cy':1824, 'cm':7, 'cd':14},
              {'y':1826, 'm':5, 's':'Z4', 'd':21, 'cy':1826, 'cm':4, 'cd':15},
              {'y':1829, 'm':11, 's':'J10', 'd':8, 'cy':1829, 'cm':10, 'cd':12},
              {'y':1836, 'm':9, 's':'J8', 'd':8, 'cy':1836, 'cm':7, 'cd':28},
              {'y':1844, 'm':6, 's':'J5', 'd':6, 'cy':1844, 'cm':4, 'cd':21},
              {'y':1846, 'm':11, 's':'Z10', 'd':23, 'cy':1846, 'cm':10, 'cd':5},
              {'y':1849, 'm':5, 's':'J4', 'd':5, 'cy':1849, 'cm':4, 'cd':13},
              {'y':1850, 'm':10, 's':'J9', 'd':9, 'cy':1850, 'cm':9, 'cd':5},
              {'y':1851, 'm':9, 's':'Z8', 'd':24, 'cy':1851, 'cm':8, 'cd':29},
              {'y':1851, 'm':12, 's':'J11', 'd':8, 'cy':1851, 'cm':10, 'cd':16},
              {'y':1855, 'm':4, 's':'Z3', 'd':20, 'cy':1855, 'cm':3, 'cd':5},
              {'y':1862, 'm':10, 's':'Z9', 'd':24, 'cy':1862, 'cm':9, 'cd':2},
              {'y':1862, 'm':11, 's':'J10', 'd':8, 'cy':1862, 'cm':9, 'cd':17},
              {'y':1864, 'm':7, 's':'Z6', 'd':23, 'cy':1864, 'cm':6, 'cd':20},
              {'y':1866, 'm':10, 's':'Z9', 'd':24, 'cy':1866, 'cm':9, 'cd':16},
              {'y':1867, 'm':7, 's':'J6', 'd':8, 'cy':1867, 'cm':6, 'cd':7},
              {'y':1867, 'm':8, 's':'Z7', 'd':24, 'cy':1867, 'cm':7, 'cd':25},
              {'y':1879, 'm':1, 's':'J12', 'd':6, 'cy':1878, 'cm':12, 'cd':14},
              {'y':1879, 'm':11, 's':'Z10', 'd':23, 'cy':1879, 'cm':10, 'cd':10},
              {'y':1883, 'm':10, 's':'J9', 'd':9, 'cy':1883, 'cm':9, 'cd':9},
              {'y':1884, 'm':9, 's':'Z8', 'd':23, 'cy':1884, 'cm':8, 'cd':5},
              {'y':1884, 'm':12, 's':'J11', 'd':7, 'cy':1884, 'cm':10, 'cd':20},
              {'y':1886, 'm':8, 's':'J7', 'd':8, 'cy':1886, 'cm':7, 'cd':9},
              {'y':1895, 'm':10, 's':'Z9', 'd':24, 'cy':1895, 'cm':9, 'cd':7},
              {'y':1895, 'm':11, 's':'J10', 'd':8, 'cy':1895, 'cm':9, 'cd':22},
              {'y':1898, 'm':9, 's':'J8', 'd':8, 'cy':1898, 'cm':7, 'cd':23},
              {'y':1899, 'm':6, 's':'Z5', 'd':22, 'cy':1899, 'cm':5, 'cd':15},
              {'y':1899, 'm':10, 's':'Z9', 'd':24,'cy':1899, 'cm':9, 'cd':20}]
    if y==1862 and cm==9:
        if lang=='Eng':
            return 'The calendrical Z9 was on 2d and the calendrical J10 was on 17d.'
        elif lang=='ChiT':
            return '曆書霜降在初二，曆書立冬在十七日。'
        else:
            return '历书霜降在初二，历书立冬在十七日。'
    if y==1895 and cm==9:
        if lang=='Eng':
            return 'The calendrical Z9 was on 7d and the calendrical J10 was on 22d.'
        elif lang=='ChiT':
            return '曆書霜降在初七，曆書立冬在廿二日。'
        else:
            return '历书霜降在初七，历书立冬在廿二日。'
    
    for x in items:
        if cm < -9998:
            if y==x['y'] and m==x['m']:
                sterm = solar_terms_names(lang)[x['s']]
                mon, day = western_months_days(lang)
                if lang=='Eng':
                    note = 'The calendrical ' + sterm + ' was on ' + mon[m-1] + ' ' + str(x['d']) + '.'
                else:
                    note = ('曆書' if lang=='ChiT' else '历书') + sterm + '在' + day[x['d']-1] + '。'
                return note
        else:
            if y==x['cy'] and cm==x['cm']:
                sterm = solar_terms_names(lang)[x['s']]
                if lang=='Eng':
                    note = 'The calendrical ' + sterm + ' was on ' + str(x['cd']) + 'd'
                    if 'cmq' in x:
                        note += ' in month ' + str(x['cmq']) if x['cmq'] > 0 else ' in leap month ' + str(-x['cmq'])
                    note += '.'
                else:
                    month_numChi = ["正","二","三","四","五","六","七","八","九","十", "十一","十二"]
                    cday = chinese_day_names(lang)
                    note = ('曆書' if lang=='ChiT' else '历书') + sterm + '在'
                    if 'cmq' in x:
                        note += month_numChi[x['cmq']-1] + '月' if x['cmq'] > 0 else ('閏' if lang=='ChiT' else '闰') + '月'
                    note += cday[x['cd']-1]
                    if x['cd'] > 9: note += '日'
                    note += '。'
                return note
    return note

def monthly_calendarNotesSouthernMing(y, m, lang, cm):
    notes = [{'y':1648, 'm':4, 'cy':1648, 'cm':-3,
         'n':{'Eng':'Several sources indicate that the leap month in this year was after the 6th month, which I find to be very unlikely.', 
              'ChiT':'王叔武"南明史料朔閏考異"引 《劫灰錄》、 《鹿樵紀聞》、 《明季南略》、 《爝火錄》說永曆二年閏六月，我認為閏六月很可能不對。',
              'ChiS':'王叔武"南明史料朔闰考异"引 《劫灰录》、 《鹿樵纪闻》、 《明季南略》、 《爝火录》说永历二年闰六月，我认为闰六月很可能不对。'}},
        {'y':1649, 'm':2, 'cy':1649, 'cm':1,
         'n':{'Eng':'Two dfferent versions of calendar in the Southern Ming dynasty were produced in the Chinese year in 1649. One of them was produced by the officials of the Yongli emperor, in which the New Year day was on February 11th, 1649. Another version was produced by the officials of the Prince of Lu, who named himself regent. The New Year day of the Lu calendar was on February 12th, 1649. According to the calculation of the Datong system, the New Year day was on February 11th, 1649.',
              'ChiT':'永曆三年和魯王監國四年正月朔有異:永曆三年正月庚申朔(公曆2月11日);《魯監國大統曆》則有魯監國四年正月辛酉朔(2月12日)。依明大統曆推算此年正月朔為庚申。',
              'ChiS':'永历三年和鲁王监国四年正月朔有异:永历三年正月庚申朔(公历2月11日);《鲁监国大统历》则有鲁监国四年正月辛酉朔(2月12日)。依明大统历推算此年正月朔为庚申。'}},
        {'y':1650, 'm':12, 'cy':1650, 'cm':-11,
         'n':{'Eng':"According to <i>Canming Datong Li</i> or <i>Datong Calendar of the Waning Ming Dynasty</i> by Fu Yili and <i>Yan Ping Wang Hu Guan Yang Ying Cong Zheng Shi Lu</i> (or <i>Account of the quartermaster Yang Ying's campaign with Prince Yanping</i>), the leap month in 1650 was after the 11th month in the Southern Ming calendar. This is consistent with the calculation by the Datong system. However, the Datong calendars produced by the Zheng dynasty for 1671, 1676 and 1677 recorded the leap month to be after the 12th month. Leap month 12 was probably based on an unofficial calendar expediently produced by the Zheng officials in 1649 since the official emperor calendar had not arrived in time because of war.", 
              'ChiT':'傅以禮《殘明大統曆》和《延平王戶官楊英從征實錄》記永曆四年閏十一月，符合大統曆的推算，但明鄭頒行的《永曆二十五年大統曆》、《永曆三十年大統曆》及《永曆三十一年大統曆》都記永曆四年閏十二月。閏十二月或許是當年鄭氏命官員權宜頒行的大統曆推算出的。', 
              'ChiS':'傅以礼《残明大统历》和《延平王户官杨英从征实录》记永历四年闰十一月，符合大统历的推算，但明郑颁行的《永历二十五年大统历》、《永历三十年大统历》及《永历三十一年大统历》都记永历四年闰十二月。闰十二月或许是当年郑氏命官员权宜颁行的大统历推算出的。'}},
        {'y':1651, 'm':1, 'cy':-9999, 'cm':-9999,
         'n':{'Eng':"According to <i>Canming Datong Li</i> or <i>Datong Calendar of the Waning Ming Dynasty</i> by Fu Yili and <i>Yan Ping Wang Hu Guan Yang Ying Cong Zheng Shi Lu</i> (or <i>Account of the quartermaster Yang Ying's campaign with Prince Yanping</i>), the leap month in 1650 was after the 11th month in the Southern Ming calendar. This is consistent with the calculation by the Datong system. However, the Datong calendars produced by the Zheng dynasty for 1671, 1676 and 1677 recorded the leap month to be after the 12th month. Leap month 12 was probably based on an unofficial calendar expediently produced by the Zheng officials in 1649 since the official emperor calendar had not arrived in time because of war.", 
              'ChiT':'傅以禮《殘明大統曆》和《延平王戶官楊英從征實錄》記永曆四年閏十一月，符合大統曆的推算，但明鄭頒行的《永曆二十五年大統曆》、《永曆三十年大統曆》及《永曆三十一年大統曆》都記永曆四年閏十二月。閏十二月或許是當年鄭氏命官員權宜頒行的大統曆推算出的。',
              'ChiS':'傅以礼《残明大统历》和《延平王户官杨英从征实录》记永历四年闰十一月，符合大统历的推算，但明郑颁行的《永历二十五年大统历》、《永历三十年大统历》及《永历三十一年大统历》都记永历四年闰十二月。闰十二月或许是当年郑氏命官员权宜颁行的大统历推算出的。'}},
        {'y':1652, 'm':2, 'cy':1652, 'cm':1,
         'n':{'Eng':"Two dfferent versions of calendar were produced in the Chinese year in 1652: emperor Yongli's and Prince Lu's version. The New Year day of the Yongli calendar was on February 10th, 1652. The New Year day of the Lu calendar was on February 9th, 1652. According to the calculation of the Datong system, the New Year day was on February 10th, 1652.",
              'ChiT':'永曆六年和魯王監國七年正月朔有異:永曆六年正月甲戌朔(公曆2月10日);《魯監國大統曆》則有魯監國七年正月癸酉朔(2月9日)。依明大統曆推算此年正月朔為甲戌。',
              'ChiS':'永历六年和鲁王监国七年正月朔有异:永历六年正月甲戌朔(公历2月10日);《鲁监国大统历》则有鲁监国七年正月癸酉朔(2月9日)。依明大统历推算此年正月朔为甲戌。'}},
        {'y':1653, 'm':8, 'cy':1653, 'cm':-7,
         'n':{'Eng':"There are discrepancies in the leap month in this year among various sources. <i>Canming Datong Li</i> or <i>Datong Calendar of the Waning Ming Dynasty</i> records the leap month to be after the 7th month, which is consistent with the caleculation of the Datong system. <i>Yan Ping Wang Hu Guan Yang Ying Cong Zheng Shi Lu</i> or <i>Account of the quartermaster Yang Ying's campaign with Prince Yanping</i> has the leap month after the 8th month. The chronicle <i>Xing Zai Yang Qiu</i> records the leap month to be after the 6th month. The Datong calendar produced by the Zheng dynasty for 1671 also records leap month after the 6th month. However, in the Datong calendar for 1676 and 1677, the leap month is changed to being after the 8th month. I think leap month 6 is unlikely. Both leap month 7 and 8 are possible. Here I follow <i>Datong Calendar of the Waning Ming Dynasty</i> and place the leap month after the 7th month.",
              'ChiT':'此年的閏月有爭議，依大統曆推算閏七月，傅以禮《殘明大統曆》亦記閏七月，但是《延平王戶官楊英從征實錄》記閏八月，《行在陽秋》記閏六月，明鄭頒行的《永曆二十五年大統曆》也記閏六月，但是後來頒行的《永曆三十年大統曆》及《永曆三十一年大統曆》卻改為閏八月。我認為閏六月不大可能，閏七月和閏八月機會較大，此處依《殘明大統曆》記閏七月。',
              'ChiS':'此年的闰月有争议，依大统历推算闰七月，傅以礼《残明大统历》亦记闰七月，但是《延平王户官杨英从征实录》记闰八月，《行在阳秋》记闰六月，明郑颁行的《永历二十五年大统历》也记闰六月，但是后来颁行的《永历三十年大统历》及《永历三十一年大统历》却改为闰八月。我认为闰六月不大可能，闰七月和闰八月机会较大，此处依《残明大统历》记闰七月。'}},
        {'y':1663, 'm':9, 'cy':1663, 'cm':8,
         'n':{'Eng':'Calendrical J8 should be on September 6th according to the calculation of the Datong system. However, <i>Canming Datong Li</i> or <i>Datong Calendar of the Waning Ming Dynasty</i> records J8 on September 5th, which is the date listed here.',
              'ChiT':'依大統曆推算白露在八月初五(公曆9月6日)，但傅以禮《殘明大統曆》記八月初四(9月5日)，此處曆書白露依《殘明大統曆》。',
              'ChiS':'依大统历推算白露在八月初五(公历9月6日)，但傅以礼《残明大统历》记八月初四(9月5日)，此处历书白露依《残明大统历》。'}},
        {'y':1671, 'm':2, 'cy':1671, 'cm':1,
         'n':{'Eng':"The Chinese Near Year in 1671 was on February 9th according to <i>Canming Datong Li</i> or <i>Datong Calendar of the Waning Ming Dynasty</i>, which also agrees with the calculation of the Datong system. However, the Datong calendar produced by the Zheng dynasty for 1671 indicates that the New Year day was on February 10th. Even though Zheng dynasty claimed that their calendars were produced expediently and should not to be taken as official, by this time the Yongli emperor had died and the Southern Ming dynasty had already ended. Zheng's calendar became the de facto official Datong calendar of the state. So I change the New Year day to February 10th in accord with Zheng's calendar.",
              'ChiT':'依大統曆推算永曆二十五正月朔在癸丑(公曆2月9日)，傅以禮《殘明大統曆》亦記正月癸丑朔，但是明鄭頒行的《永曆二十五年大統曆》記正月甲寅朔(2月10日)。雖然鄭氏奉明正朔，聲稱其大統曆乃「權宜頒行」，但是當時永曆帝已死，南明也已亡，明鄭的大統曆變相成為正統的大統曆書，所以此處依明鄭大統曆記正月甲寅朔。',
              'ChiS':'依大统历推算永历二十五正月朔在癸丑(公历2月9日)，傅以礼《残明大统历》亦记正月癸丑朔，但是明郑颁行的《永历二十五年大统历》记正月甲寅朔(2月10日)。虽然郑氏奉明正朔，声称其大统历乃「权宜颁行」，但是当时永历帝已死，南明也已亡，明郑的大统历变相成为正统的大统历书，所以此处依明郑大统历记正月甲寅朔。'}},
        {'y':1674, 'm':7, 'cy':1674, 'cm':6,
         'n':{'Eng':'According to the calculation of the Datong system, the month 6 conjunction was on July 4th, which is inconsistent with the record in <i>Canming Datong Li</i> or <i>Datong Calendar of the Waning Ming Dynasty</i> (July 3rd). July 3rd is used here.',
              'ChiT':'依明大統曆推算六月朔在甲午(公曆7月4日)，此處依傅以禮《殘明大統曆》改為六月癸巳朔(7月3日)。',
              'ChiS':'依明大统历推算六月朔在甲午(公历7月4日)，此处依傅以礼《残明大统历》改为六月癸巳朔(7月3日)。'}},
        {'y':1674, 'm':9, 'cy':1674, 'cm':9,
         'n':{'Eng':'According to the calculation of the Datong system, the month 9 conjunction was on September 30th, which is inconsistent with the record in <i>Canming Datong Li</i> or <i>Datong Calendar of the Waning Ming Dynasty</i> (September 29th). September 29th is used here.',
              'ChiT':'依明大統曆推算九月朔在壬戌(公曆9月30日)，此處依傅以禮《殘明大統曆》改為九月辛酉朔(9月29日)。',
              'ChiS':'依明大统历推算九月朔在壬戌(公历9月30日)，此处依傅以礼《残明大统历》改为九月辛酉朔(9月29日)。'}},
        {'y':1675, 'm':7, 'cy':1675, 'cm':-6,
         'n':{'Eng':'According to the calculation of the Datong system, a conjunction occurred on July 22nd. <i>Canming Datong Li</i> or <i>Datong Calendar of the Waning Ming Dynasty</i> records a conjunction on July 23rd. The one-day difference changed the leap month in this year. July 22nd conjunction resulted in a leap month after the 5th month. July 23rd conjunction resulted in a leap month after the 6th month. Leap month 6 is also recorded in the calendars produced by the Zheng dynasty for 1676 and 1677. So I use the data in <i>Datong Calendar of the Waning Ming Dynasty</i>.',
              'ChiT':'依明大統曆推算有朔日在丁巳(公曆7月22日)，對應的朔日在傅以禮《殘明大統曆》出現在下一日戊午(7月23日)。此一日之差造成閏月分歧:依大統曆推算閏五月，《殘明大統曆》則為閏六月。明鄭頒行的《永曆三十年大統曆》及《永曆三十一年大統曆》都記永曆二十九年閏六月，所以此處朔閏依《殘明大統曆》。',
              'ChiS':'依明大统历推算有朔日在丁巳(公历7月22日)，对应的朔日在傅以礼《残明大统历》出现在下一日戊午(7月23日)。此一日之差造成闰月分歧:依大统历推算闰五月，《残明大统历》则为闰六月。明郑颁行的《永历三十年大统历》及《永历三十一年大统历》都记永历二十九年闰六月，所以此处朔闰依《残明大统历》。'}},
        {'y':1676, 'm':12, 'cy':1676, 'cm':11,
         'n':{'Eng':'<i>Canming Datong Li</i> or <i>Datong Calendar of the Waning Ming Dynasty</i> records that Z11 (winter solstice) was on the 16th day in month 11 (Dec. 20), which is inconsistent with the calculation of the Datong system (Dec. 21). The official Datong Calendar for 1676 records Z11 on the 17th day in month 11 (Dec. 21). So the Z11 date in <i>Datong Calendar of the Waning Ming Dynasty</i> is wrong.', 
              'ChiT':'《殘明大統曆》記冬至在十一月十六(公曆12月20日)，不合明大統曆的推步(十一月十七)。明鄭頒行的《永曆三十年大統曆》記冬至在十一月十七(12月21日)，證實《殘明大統曆》的冬至日期錯了。',
              'ChiS':'《残明大统历》记冬至在十一月十六(公历12月20日)，不合明大统历的推步(十一月十七)。明郑颁行的《永历三十年大统历》记冬至在十一月十七(12月21日)，证实《残明大统历》的冬至日期错了。'}},
        {'y':1677, 'm':7, 'cy':1677, 'cm':7, 
         'n':{'Eng':'According to the calculation of the Datong system, month 7 conjunction was on July 29th, which is inconsistent with July 30th recorded in <i>Canming Datong Li</i> or  <i>Datong Calendar of the Waning Ming Dynasty</i> and the calendar produced by the Zheng dynasty for 1677. The Zheng calendar date is used here.',
              'ChiT':'依明大統曆推算七月朔在乙亥(公曆7月29日)，不合傅以禮《殘明大統曆》及明鄭《永曆三十一年大統曆》的丙子朔(7月30日)。此處依《殘明大統曆》及明鄭大統曆記七月丙子朔。',
              'ChiS':'依明大统历推算七月朔在乙亥(公历7月29日)，不合傅以礼《残明大统历》及明郑《永历三十一年大统历》的丙子朔(7月30日)。此处依《残明大统历》及明郑大统历记七月丙子朔。'}},
        {'y':1678, 'm':7, 'cy':1678, 'cm':6,
         'n':{'Eng':'According to the calculation of the Datong system, the month 6 conjunction was on July 18th, inconsistent with July 19th recorded in <i>Canming Datong Li</i> or <i>Datong Calendar of the Waning Ming Dynasty</i>. July 19th is used here.',
              'ChiT':'依明大統曆推算六月朔在己巳(公曆7月18日)，不合傅以禮《殘明大統曆》的庚午朔(7月19日)。此處依《殘明大統曆》記六月庚午朔。',
              'ChiS':'依明大统历推算六月朔在己巳(公历7月18日)，不合傅以礼《残明大统历》的庚午朔(7月19日)。此处依《残明大统历》记六月庚午朔。'}}, 
        {'y':1682, 'm':2, 'cy':1682, 'cm':1,
         'n':{'Eng':'According to the calculation of the Datong system, the Chinese New Year in 1682 was on February 8th, inconsistent with February 7th recorded in <i>Canming Datong Li</i> or <i>Datong Calendar of the Waning Ming Dynasty</i>. February 7th is used here.',
              'ChiT':'依明大統曆推算永曆三十六年正月朔在庚戌(公曆2月8日)，不合傅以禮《殘明大統曆》的己酉朔(2月7日)。此處依《殘明大統曆》記正月己酉朔。',
              'ChiS':'依明大统历推算永历三十六年正月朔在庚戌(公历2月8日)，不合傅以礼《残明大统历》的己酉朔(2月7日)。此处依《残明大统历》记正月己酉朔。'}}]
    for x in notes:
        if cm < -9998:
            if y==x['y'] and m==x['m']: return x['n'][lang]
        else:
            if y==x['cy'] and cm==x['cm']: return x['n'][lang]
    return ''

def monthly_calendarNotes1912_1979(y, m, lang, cm):
    if cm < -9998:
        notes = [{'y':1912, 'm':11, 
            'n':{'Eng':'The calendrical Z10 was on Nov 23.', 
                'ChiT':'曆書小雪在23日。', 'ChiS':'历书小雪在23日。'}}, 
            {'y':1913, 'm':9,
            'n':{'Eng':'The calendrical Z8 (September equinox) was on Sep 24.',
                'ChiT':'曆書秋分在24日。', 'ChiS':'历书秋分在24日。'}},
            {'y':1917, 'm':12,
            'n':{'Eng':'The calendrical J11 was on Dec 7.',
                'ChiT':'曆書大雪在7日。', 'ChiS':'历书大雪在7日。'}},
            {'y':1927, 'm':9,
            'n':{'Eng':'The calendrical J8 was on Sep 8.',
                'ChiT':'曆書白露在8日。', 'ChiS':'历书白露在8日。'}},
            {'y':1928, 'm':6,
            'n':{'Eng':'The calendrical Z5 (June solstice) was on June 21.',
                'ChiT':'曆書夏至在21日。', 'ChiS':'历书夏至在21日。'}},
            {'y':1979, 'm':1,
            'n':{'Eng':'Z12 calculated by DE441 was at 23:59:54 (UTC+8) on Jan. 20. <i>Chinese Astronomical Almanac for the Year 1979</i> lists Z12 at 00:00 (UTC+8) on Jan 21, so the calendrical Z12 was on Jan 21.',
                'ChiT':'DE441曆表推算的大寒時刻是1月20日23:59:54 (UTC+8)，《一九七九年中国天文年历》載大寒時刻為1月21日00:00 (UTC+8)，故曆書大寒在1月21日。',
                'ChiS':'DE441历表推算的大寒时刻是1月20日23:59:54 (UTC+8)，《一九七九年中国天文年历》载大寒时刻为1月21日00:00 (UTC+8)，故历书大寒在1月21日。'}}]
        for x in notes:
            if y==x['y'] and m==x['m']: return x['n'][lang]
    else:
        notes = [{'y':1912, 'm':10, 
            'n':{'Eng':'The calendrical Z10 was on 15d.', 
                'ChiT':'曆書小雪在十五日。', 'ChiS':'历书小雪在十五日。'}}, 
            {'y':1913, 'm':8,
            'n':{'Eng':'The calendrical Z8 (September equinox) was on 24d.',
                'ChiT':'曆書秋分在廿四日。', 'ChiS':'历书秋分在廿四日。'}},
            {'y':1917, 'm':10,
            'n':{'Eng':'The calendrical J11 was on 23d.',
                'ChiT':'曆書大雪在廿三日。', 'ChiS':'历书大雪在廿三日。'}},
            {'y':1927, 'm':8,
            'n':{'Eng':'The calendrical J8 was on 13d.',
                'ChiT':'曆書白露在十三日。', 'ChiS':'历书白露在十三日。'}},
            {'y':1928, 'm':5,
            'n':{'Eng':'The calendrical Z5 (June solstice) was on 4d.',
                'ChiT':'曆書夏至在初四。', 'ChiS':'历书夏至在初四。'}},
            {'y':1978, 'm':12,
            'n':{'Eng':'Z12 calculated by DE441 was at 23:59:54 (UTC+8) on 22d. <i>Chinese Astronomical Almanac for the Year 1979</i> lists Z12 at 00:00 (UTC+8) on 23d, so the calendrical Z12 was on 13d.',
                'ChiT':'DE441曆表推算的大寒時刻是廿二日23:59:54 (UTC+8)，《一九七九年中国天文年历》載大寒時刻為廿三日00:00 (UTC+8)，故曆書大寒在廿三日。',
                'ChiS':'DE441历表推算的大寒时刻是廿二日23:59:54 (UTC+8)，《一九七九年中国天文年历》载大寒时刻为廿三日00:00 (UTC+8)，故历书大寒在廿三日。'}}]
        for x in notes:
            if y==x['y'] and cm==x['m']: return x['n'][lang]
    return ''

def monthly_calendarNotesAfter2050(y, m, lang, cm):
    suffix = {'Eng':' is close to the midnight. The actual date may be off by one day.',
              'ChiT':'的時刻接近午夜零時，實際日期或會與所示日期有一日之差。',
              'ChiS':'的时刻接近午夜零时，实际日期或会与所示日期有一日之差。'}
    note_early = {'Eng':'The lunar conjunction (Q0) is close to the midnight. The start day of the month may be one day earlier.',
                  'ChiT':'朔的時刻接近午夜零時，初一或會提早一天。',
                  'ChiS':'朔的时刻接近午夜零时，初一或会提早一天。'}
    note_late = {'Eng':'The lunar conjunction (Q0) is close to the midnight. The start day of the month may be one day later.',
                 'ChiT':'朔的時刻接近午夜零時，初一或會推遲一天。',
                 'ChiS':'朔的时刻接近午夜零时，初一或会推迟一天。'}
    if y==2051 and (m==3 or cm==2):
        if lang=='Eng':
            note = 'The time of Z2 (March equinox)' + suffix['Eng']
        else:
            note = '春分' + suffix[lang]
        return note
    if y==2057 and (m==9 or cm==9): return note_early[lang]
    if (y==2083 and m==2) or (y==2082 and cm==12): 
        if lang=='Eng':
            note = 'The time of J1' + suffix['Eng']
        else:
            note = '立春' + suffix[lang]
        return note
    if y==2084 and (m==3 or cm==2):
        if lang=='Eng':
            note = 'The time of Z2 (March equinox)' + suffix['Eng']
        else:
            note = '春分' + suffix[lang]
        return note
    if y==2089 and (m==9 or cm==8): return note_late[lang]
    if y==2097 and (m==8 or cm==7): return note_early[lang]
    if y==2114 and (m==11 or cm==10):
        if lang=='Eng':
            note = 'The time of Z10' + suffix['Eng']
        else:
            note = '小雪' + suffix[lang]
        return note
    if y==2115 and (m==2 or cm==2): return note_late[lang]
    if y==2116 and (m==5 or cm==4): return note_late[lang]
    if y==2133 and (m==9 or cm==9): return note_early[lang]
    if y==2142 and (m==9 or cm==7): 
        if lang=='Eng':
            note = 'The time of J8' + suffix['Eng']
        else:
            note = '白露' + suffix[lang]
        return note
    if y==2155 and (m==10 or cm==9):
        if lang=='Eng':
            note = 'The time of Z9' + suffix['Eng']
        else:
            note = '霜降' + suffix[lang]
        return note
    if y==2157 and (m==12 or cm==11):
        if lang=='Eng':
            note = 'The time of Z11 (December solstice)' + suffix['Eng']
        else:
            note = '冬至' + suffix[lang]
        return note
    if y==2165 and (m==12 or cm==11): return note_early[lang]
    if y==2172 and (m==10 or cm==9): return note_early[lang]
    if y==2183 and (m==3 or cm==2):
        if lang=='Eng':
            note = 'The time of Z2 (March equinox)' + suffix['Eng']
        else:
            note = '春分' + suffix[lang]
        return note
    if y==2186 and (m==2 or cm==1):
        if lang=='Eng':
            note = 'The time of J1' + suffix['Eng']
        else:
            note = '立春' + suffix[lang]
        return note
    return ''

def addYearInfo(y, lang, calendar): 
    """
    Add information in particular years
    """
    info = ''
    
    # Qin and early Han dynasty
    if calendar=='default' and y >= -220 and y <= -103:
        if lang=='Eng':
            return "The calendars used between 221 BCE and 104 BCE were modified versions of the Zhuanxu calendar, one of the old calendars used in the third century BCE in the state of Qin. The first month was the hai month (present-day month 10). However, it was still called month 10 instead of month 1. The numerical order of the months in a year was 10, 11, 12, 1, 2, ..., 9. The intercalary month was placed at the end of a year, called post month 9. There was a major calendar reform in 104 BCE, where the first month of a year was changed to month 1 and the intercalary month was placed in the month that did not contain a major solar term. The Chinese year in 104 BCE had 15 Chinese months as a result of the change.<br />The calendars in this period are reconstructed according to the description in the article \"Researches on Calendars from Qin to early Han (246 B.C. to 104 B.C.) &mdash; centering on excavated calendrical bamboo slips\" (秦至汉初(前246至前104)历法研究&mdash;以出土历简为中心), L&#464; Zh&#333;ngl&#237;n (李忠林), in <i>Studies in Chinese History</i> (《中国史研究》), issue no. 2, pp. 17&ndash;69 (2012)."
        elif lang=='ChiT':
            return "秦朝及漢初(公元前221年 &ndash; 前104年)的曆法沿用顓頊曆的月序。顓頊曆是古六曆之一，據說戰國後期在秦國使用。顓頊曆以建亥(即今天的十月)為年首，但仍稱建亥為十月。月的數序是十月、十一月、十二月、正月、二月……九月，閏月置於年終，稱為後九月。秦朝的曆法與顓頊曆稍有不同。漢朝建立後基本上沿用秦曆，一百年間只作了少許修改，直到漢武帝太初元年(公元前104年)才頒行新曆法，以建寅(正月)為年首，並把閏月置於無中氣的月份，這使公元前104年的農曆年有十五個農曆月。秦朝為了避秦始皇名諱(正、政同音)，把正月改稱「端月」，到漢朝又改回正月。這裡沒有跟從歷史，在秦朝仍稱建寅為正月。<br />這裡的復原日曆是根據李忠林的文章「秦至汉初(前246至前104)历法研究&mdash;以出土历简为中心」，發表於《中国史研究》2012年第2期第17&ndash;69頁。"
        else:
            return "秦朝及汉初(公元前221年 &ndash; 前104年)的历法沿用颛顼历的月序。颛顼历是古六历之一，据说战国后期在秦国使用。颛顼历以建亥(即今天的十月)为年首，但仍称建亥为十月。月的数序是十月、十一月、十二月、正月、二月……九月，闰月置于年终，称为后九月。秦朝的历法与颛顼历稍有不同。汉朝建立后基本上沿用秦历，一百年间只作了少许修改，直到汉武帝太初元年(公元前104年)才颁行新历法，以建寅(正月)为年首，并把闰月置于无中气的月份，这使公元前104年的农历年有十五个农历月。秦朝为了避秦始皇名讳(正、政同音)，把正月改称「端月」，到汉朝又改回正月。这里没有跟从历史，在秦朝仍称建寅为正月。<br />这里的复原日历是根据李忠林的文章「秦至汉初(前246至前104)历法研究&mdash;以出土历简为中心」，发表于《中国史研究》2012年第2期第17&ndash;69页。"

    # Xin dynasty
    if calendar=='default' and y >= 9 and y <= 23:
        if lang=='Eng':
            info = "The Xin dynasty was established in 9 CE. The chou month (present day month 12) was designated as the first month of a year; the yin month (present day month 1) became month 2 and so on. The Chinese month numbers were shifted by one. As a result, the Chinese year in 8 CE (Wu chen) had only 11 months. When the Xin dynasty was overthrown in 23 CE, the month numbers were switched back with month 1 being the yin month again."
            if y==23:
                info += '<br />As a result, the Chinese year in 23 CE had two sets of calendar: one for the Xin dynasty (chou month being the first month) and the other for the restored Han dynasty (yin month being the first month), also known as Gengshi. The two sets of calendar had 11 overlapping months: months 2-12 in the Xin calendar were the same as months 1-11 in the Gengshi calendar.'
        elif lang=='ChiT':
            info = "公元9年，王莽建立新朝，改正朔以殷正建丑(即現在的十二月)為年首，故公元8年的農曆年(戊辰年)只有十一個月。農曆月的數序是:建丑為正月、建寅為二月等等，與現在通用的月序相差一個月。新朝於地皇四年(癸未年，公元23年)亡，綠林軍擁立漢淮南王劉玄为帝，改元更始元年，恢復以建寅(即現在的正月)為年首。"
            if y==23:
                info += '<br />地皇四年和更始元年有十一個月重疊。地皇四年用丑正、更始元年用寅正，所以地皇四年二至十二月相當於更始元年正至十一月。'
        else:
            info = "公元9年，王莽建立新朝，改正朔以殷正建丑(即现在的十二月)为年首，故公元8年的农历年(戊辰年)只有十一个月。农历月的数序是:建丑为正月、建寅为二月等等，与现在通用的月序相差一个月。新朝于地皇四年(癸未年，公元23年)亡，绿林军拥立汉淮南王刘玄为帝，改元更始元年，恢复以建寅(即现在的正月)为年首。"
            if y==23:
                info += '<br />地皇四年和更始元年有十一个月重叠。地皇四年用丑正、更始元年用寅正，所以地皇四年二至十二月相当于更始元年正至十一月。'
        return info

    # Wei dynasty
    if y >= 237 and y <= 240 and calendar=='default':
        if lang=='Eng':
            return "In 237 CE, emperor Mingdi of the Wei dynasty declared that the chou month (present day month 12) would be the first month of a year; the yin month (present day month 1) became month 2 and so on. The Chinese month numbers were shifted by one. The new system was imposed after month 2 in the Chinese year in 237, in which month 4 was followed by month 2. When the emperor died in 239 CE, the month numbers were switched back with month 1 being the yin month again in the following year. As a result, the Chinese year in 239 had 13 months, where month 12 appeared twice."
        elif lang=='ChiT':
            return "魏青龍五年（丁巳年，公元237年），魏明帝改正朔，以殷正建丑(即現在的十二月)為年首，二月後實施，並改元景初元年。所以丁巳年沒有三月份，二月後的月份是四月。農曆月的數序是:建丑為正月、建寅為二月等等，與現在通用的月序相差一個月。景初三年（公元239年）明帝駕崩,次年恢復以建寅(即現在的正月)為年首。景初三年有兩個十二月。"
        else:
            return "魏青龙五年（丁巳年，公元237年），魏明帝改正朔，以殷正建丑(即现在的十二月)为年首，二月后实施，并改元景初元年。所以丁巳年没有三月份，二月后的月份是四月。农历月的数序是:建丑为正月、建寅为二月等等，与现在通用的月序相差一个月。景初三年（公元239年）明帝驾崩,次年恢复以建寅(即现在的正月)为年首。景初三年有两个十二月。"

    # Empress Consort Wu
    if calendar=='default' and y >= 689 and y<= 700:
        if lang=='Eng':
            return "In December 689, Empress Consort Wu designated the zi month (month 11) as the first month of a year. However, the month numbers did not change. The zi month was named Zheng, which is usually referred to month 1; chou month was stilled called month 12; yin month was month 1 and so on. Here the Zheng month is still labelled as month 11. The first month of a year was changed back to month 1 in February 701. The Chinese year in 689 only had 11 months (one leap month), whereas the Chinese year in 700 had 15 months (one leap month)."
        elif lang=='ChiT':
            return "公元689年12月，武則天改正朔，以周正建子(即現在的十一月)為年首，建子改稱正月，建寅（即現在的正月）改稱一月，其他農曆月的數序不變（即正月、十二月、一月、二月⋯⋯十月）。公元701年2月又改回以建寅為年首。公元689年的農曆年（己丑年）只有十一個月（其中一個月是閏月），而公元700年的農曆年（庚子年）有十五個月（其中一個月是閏月）。"
        else:
            return "公元689年12月，武则天改正朔，以周正建子(即现在的十一月)为年首，建子改称正月，建寅（即现在的正月）改称一月，其他农历月的数序不变（即正月、十二月、一月、二月__十月）。公元701年2月又改回以建寅为年首。公元689年的农历年（己丑年）只有十一个月（其中一个月是闰月），而公元700年的农历年（庚子年）有十五个月（其中一个月是闰月）。"

    # Tang Suzong
    if calendar=='default' and y==761 or y==762:
        if lang=='Eng':
            return "In December 761, emperor Suzong of the Tang dynasty designated the zi month (present day month 11) as the first month of a year; the chou month (present day month 12) became month 2; the yin month (present day month 1) became month 3 and so on. The Chinese month numbers were shifted by two. As a result, the Chinese year in 761 (Xin chou) had only 10 months. The month numbers ware switched back to the old system in April 762. The Chinese year in 762 (Ren yin) had 14 months, with two month 4s and two month 5s."
        elif lang=='ChiT':
            return "公元761年12月，唐肅宗改正朔，以周正建子(即現在的十一月)為年首，建子改稱正月、建丑（即現在的十二月）改稱二月、建寅（即現在的正月）改稱三月等等，與現在通用的月序相差二個月。公元762年4月又把農曆月的數序改回以建寅為正月、建卯為二月等。公元761年的農曆年（辛丑年）只有十個月,而公元762年的農曆年（壬寅年）則有十四個月，其中有兩個四月和兩個五月。"
        else:
            return "公元761年12月，唐肃宗改正朔，以周正建子(即现在的十一月)为年首，建子改称正月、建丑（即现在的十二月）改称二月、建寅（即现在的正月）改称三月等等，与现在通用的月序相差二个月。公元762年4月又把农历月的数序改回以建寅为正月、建卯为二月等。公元761年的农历年（辛丑年）只有十个月,而公元762年的农历年（壬寅年）则有十四个月，其中有两个四月和两个五月。"

    # Gregorian calendar reform
    if y==1582:
        if lang=='Eng':
            return "Gregorian calendar reform: Julian calendar was used until October 4, after which the Gregorian calendar was used. To restore the March equinox to the date it had in 325 CE (March 21), the date was advanced so that October 4 was followed by October 15."
        elif lang=='ChiT':
            return "格里高里曆改:公曆在10月4日及之前用儒略曆，之後用格里高里曆。為使春分的日期回復到3月21日(公元325年時的春分日期)，10月4日的下一日改為10月15日，跳了10日。"
        else:
            return "格里高里历改:公历在10月4日及之前用儒略历，之后用格里高里历。为使春分的日期回复到3月21日(公元325年时的春分日期)，10月4日的下一日改为10月15日，跳了10日。"

    # Calendar Case
    if y > 1666.5 and y < 1670.5 and calendar=='default':
        if lang=='Eng':
            return 'Following the Calendar Case (see, e.g., <a href="https://halshs.archives-ouvertes.fr/halshs-01222267/document" target="_blank">Jami 2015</a> and <a href="https://journals.sagepub.com/doi/full/10.1177/0021828620901887" target="_blank">Cullen &amp; Jami 2020</a>), the Qing government abolished the Western system of astronomy in the calendar computation in 1667-1669. The calendars in this period were calculated by the <i>Datong</i> system, which was used in the Ming dynasty. The 24 solar terms were calculated based on the <i>pingqi</i> rule, which took into account only the mean motion of the Sun. Two sets of calendrical solar terms are provided here for reference: the Xinfa solar terms are based on <i>3500 Years of Calendars and Astronomical Phenomena</i>, which are recomputed using the Western system; the <i>Datong</i> solar terms are based on the <i>Datong</i> system. As for the lunar conjunctions, the dates calculated using the <i>Datong</i> astronomical system are identical to those computed using the Western system in these years.'
        elif lang=='ChiT':
            return '康熙六年至八年清政府因<a href="https://zh.wikipedia.org/zh-hant/%E5%BA%B7%E7%86%99%E5%8E%86%E7%8B%B1" target="_blank">曆獄</a>廢除西洋新法，復用明朝《大統曆》，二十四節氣改回平氣。這裡提供兩套曆書節氣:「新法節氣」根據《三千五百年历日天象》，此乃以後的欽天監依西洋新法追推的定氣;「大統曆節氣」根據明朝《大統曆》推算。至於朔日，依明朝《大統曆》和依《西洋新法曆書》計算結果在這幾年的日期完全一致。'
        else:
            return '康熙六年至八年清政府因<a href="https://zh.wikipedia.org/zh-cn/%E5%BA%B7%E7%86%99%E5%8E%86%E7%8B%B1" target="_blank">历狱</a>废除西洋新法，复用明朝《大统历》，二十四节气改回平气。这里提供两套历书节气:「新法节气」根据《三千五百年历日天象》，此乃以后的钦天监依西洋新法追推的定气;「大统历节气」根据明朝《大统历》推算。至于朔日，依明朝《大统历》和依《西洋新法历书》计算结果在这几年的日期完全一致。'

    return info

def addChineseYearNote(y, lang, calendar):
    if y < 618:
        return ChineseYearNoteBeforeTang(y, lang, calendar)
    elif y < 960:
        return ChineseYearNoteTang(y, lang, calendar)
    if y > 1367 and y < 1912 and calendar=='default':
        return ChineseYearNoteMingQing(y, lang)
    if calendar=='SouthernMing': 
        return ChineseYearNoteSouthernMingZheng(y, lang)
    if calendar=='default' and y > 2050:
        return ChineseYearNoteAfter2050(y, lang)
    return ''

def ChineseYearNoteBeforeTang(y, lang, calendar):
    if y==-103 and calendar=='default':
        if lang=='Eng':
            return '<p style="color:red;">The calendar reform caused this year having 15 Chinese months. New calendar is assumed to start from month 5. The lunar conjunction day was one day earlier than that of the old calendar, turning month 4 into a short month.</p>'
        elif lang=='ChiT':
            return '<p style="color:red;">太初元年的曆改使這年有十五個農曆月。五月起的日曆依太初曆，朔日比舊曆早一日，使四月變成小月。</p>'
        else:
            return '<p style="color:red;">太初元年的历改使這年有十五个农历月。五月起的日历依太初历，朔日比旧历早一日，使四月变成小月。</p>'

    if calendar=='default' and y==8:
        if lang=='Eng':
            return '<p style="color:red;">The Xin dynasty was established in 9 CE. The chou month (present day month 12) was desnigated as the first month of a year; the yin month (present day month 1) became month 2 and so on. The Chinese month numbers were shifted by one. As a result, the Chinese year in 8 CE (Wu chen) had only 11 months.</p>'
        elif lang=='ChiT':
            return '<p style="color:red;">公元9年，王莽建立新朝，改正朔以殷正建丑(即現在的十二月)為年首，故公元8年的中曆年(戊辰年)只有十一個月。</p>'
        else:
            return '<p style="color:red;">公元9年，王莽建立新朝，改正朔以殷正建丑(即现在的十二月)为年首，故公元8年的农历年(戊辰年)只有十一个月。</p>'
        
    if y==236 and calendar=='default':
        if lang=='Eng':
            return '<p style="color:red;">Note that month 12 had only 28 days. This was due to the adoption of a new version of calendar in month 1 in the following year.</p>'
        elif lang=='ChiT':
            return '<p style="color:red;">由於新曆法(景初曆)於次年正月初一開始使用，十二月只有二十八日。</p>'
        else:
            return '<p style="color:red;">由于新历法(景初历)于次年正月初一开始使用，十二月只有二十八日。</p>'

    if y==238 and calendar=='Wu':
        if lang=='Eng':
            return '<p style="color:red;">In Appendix 2 of the book <i>3500 Years of Calendars and Astronomical Phenomena</i>, the sexagenary day of the leap month 10 conjunction is listed as ji; chou, corresponding to Nov. 25. This is at odds with my calculation. The result of my calculation is consistent with the data on the <a href="http://sinocal.sinica.edu.tw/" target="_blank">Chinese-Western calendar conversion website</a> created by Academia Sinica in Taiwan. The preface of the book says that the calendar data in its appendices are based on the book 《歷代長術輯要》(<i>Compilation of Historical Calendars</i>) by Wang Yuezhen (汪曰楨). I looked at the book and found that the date listed there was also the same as my calculation. I suspect that the date listed in <i>3500 Years of Calendars and Astronomical Phenomena</i> is wrong. The book also lists the sexagenary day of the month 11 conjunction in the Wu state as ji chou, which is certainly wrong since this date was far away from the new moon close to the beginning of month 11.</p>'
        elif lang=='ChiT':
            return '<p style="color:red;">《三千五百年历日天象》附表2記吳赤烏元年閏十月己丑朔和十一月己丑朔。十一月己丑朔無疑是錯的，這裡列出的閏十月戊子朔是根據我的推步，結果與台灣中央研究院的<a href="http://sinocal.sinica.edu.tw/" target="_blank">兩千年中西曆轉換網站</a>一致，《三千五百年历日天象》前言說其附表參照清汪曰楨的《歷代長術輯要》，翻查此書發現亦記吳閏十月戊子。</p>'
        else:
            return '<p style="color:red;">《三千五百年历日天象》附表2记吴赤乌元年闰十月己丑朔和十一月己丑朔。十一月己丑朔无疑是错的，这里列出的闰十月戊子朔是根据我的推步，结果与台湾中央研究院的<a href="http://sinocal.sinica.edu.tw/" target="_blank">两千年中西历转换网站</a>一致，《三千五百年历日天象》前言说其附表参照清汪曰桢的《历代长术辑要》，翻查此书发现亦记吴闰十月戊子。</p>'

    if y==447 and calendar=='WeiZhouSui':
        if lang=='Eng':
            return "<p style='color:red;'>According to <i>Index to Comprehensive Mirror to Aid in Governmance</i>, the month 11 conjunction occurred on a jia xu day (Dec. 23). However, in <i>Compilation of Historical Calendars</i> by Wang Yuezhen, the month 12 conjunction was listed on a jia xu day and is at odds with its statement that the winter solstice occurred on a jia xu day in month 11. The month 12 conjunction on a jia xu day is certainly a typo because a jia xu day was 29 days (or 89 days) after a yi si day, which was the leap month 10 conjunction date. So jia xu day could only be the month 11 conjunction date. In <i>3500 Years of Calendars and Astronomical Phenomena</i> by Zhang Peiyu and <i>Tables of Historical Lunar Conjunctions and Leap Months</i> by Chan Yuan, the month 11 conjunction is mistakenly listed on Dec. 24. They were probably misled by Wang's typo. The book <i>A Sino-Western Calendar For Two Thousand Years (1-2000)</i> by Hsueh Chung-San and Ouyang Yi correctly places the month 11 conjunction on Dec. 23. Surprisingly, the <a href='http://sinocal.sinica.edu.tw/' target='_blank'>Chinese-Western calendar conversion website</a> created by Academia Sinica in Taiwan, whose ancient calendar data are based on <i>A Sino-Western Calendar For Two Thousand Years (1-2000)</i>, does not follow the book and mistakenly places the month 11 conjunction on Dec. 24.</p>"
        elif lang=='ChiT':
            return '<p style="color:red;">《通鑑目錄》記太武帝太平真君八年(447年)十一月甲戌朔，汪曰楨《歷代長術輯要》卻記「十乙亥、十二甲戌朔、閏十(十甲辰小雪、十一甲戌冬至)」，沒有記閏十月朔和十一月朔干支就是說兩朔日的天干和都是乙，但是「十二甲戌」是錯的，因為閏十朔是乙巳，而甲戌在乙巳後29日(或89日)，絕不可能是十二月朔，而且與其「十一甲戌冬至」相悖，可見「十二甲戌朔」應是「十一甲戌朔」之誤，「十二甲戌朔」是宋曆而非魏曆。張培瑜《三千五百年历日天象》和陳垣《二十史朔閏表》可能被《歷代長術輯要》誤導，記十一月乙亥朔及十二月甲辰朔。薛仲三、歐陽頤的《兩千年中西曆對照表》則沒有錯，奇怪的是臺灣中央研究院的<a href="http://sinocal.sinica.edu.tw/" target="_blank">兩千年中西曆轉換</a>卻不跟從《兩千年中西曆對照表》，也弄錯了十一月朔的日期。</p>'
        else:
            return '<p style="color:red;">《通鉴目录》记太武帝太平真君八年(447年)十一月甲戌朔，汪曰桢《历代长术辑要》却记「十乙亥、十二甲戌朔、闰十(十甲辰小雪、十一甲戌冬至)」，没有记闰十月朔和十一月朔干支就是说两朔日的天干和都是乙，但是「十二甲戌」是错的，因为闰十朔是乙巳，而甲戌在乙巳后29日(或89日)，绝不可能是十二月朔，而且与其「十一甲戌冬至」相悖，可见「十二甲戌朔」应是「十一甲戌朔」之误，「十二甲戌朔」是宋历而非魏历。张培瑜《三千五百年历日天象》和陈垣《二十史朔闰表》可能被《历代长术辑要》误导，记十一月乙亥朔及十二月甲辰朔。薛仲三、欧阳颐的《两千年中西历对照表》则没有错，奇怪的是台湾中央研究院的<a href="http://sinocal.sinica.edu.tw/" target="_blank">两千年中西历转换</a>却不跟从《两千年中西历对照表》，也弄错了十一月朔的日期。</p>'

    if y==502 and calendar=='default':
        if lang=='Eng':
            return '<p style="color:red;">There is a discrepancy between the main text and Appendix 3 in the book <i>3500 Years of Calendars and Astronomical Phenomena</i>. The leap month in this year is listed as after month 5 in the main text but after month 4 in Appendix 3.</p>'
        elif lang=='ChiT':
            return '<p style="color:red;">《三千五百年历日天象》的正文與其附表3的資料不一致，正文記這年閏五月，附表3則為閏四月。</p>'
        else:
            return '<p style="color:red;">《三千五百年历日天象》的正文与其附表3的资料不一致，正文记这年闰五月，附表3则为闰四月。</p>'

    if y==575 and calendar=='default':
        if lang=='Eng':
            return '<p style="color:red;">There is a discrepancy between the main text and Appendix 3 in the book <i>3500 Years of Calendars and Astronomical Phenomena</i>. The leap month in this year is listed as after month 8 in the main text but after month 9 in Appendix 3.</p>'
        elif lang=='ChiT':
            return '<p style="color:red;">《三千五百年历日天象》的正文與其附表3的資料不一致，正文記這年閏八月，附表3則為閏九月。</p>'
        else:
            return '<p style="color:red;">《三千五百年历日天象》的正文与其附表3的资料不一致，正文记这年闰八月，附表3则为闰九月。</p>'

    if y==575 and calendar=='WeiQi':
        if lang=='Eng':
            return "<p style='color:red;'>Appendix 3 of the book <i>3500 Years of Calendars and Astronomical Phenomena</i> lists the leap month in this year as after month 9. This is at odds with my calculation, which agrees with the data on the <a href='http://sinocal.sinica.edu.tw/' target='_blank'>Chinese-Western calendar conversion website</a> created by Academia Sinica in Taiwan. The data in Appendix 3 are supposed to be based on the book 《歷代長術輯要》(<i>Compilation of Historical Calendars</i>) by Wang Yuezhen (汪曰楨), but that book also lists the leap month as after month 8. That's why I use my calculation here.</p>"
        elif lang=='ChiT':
            return '<p style="color:red;">《三千五百年历日天象》附表3記北齊武平六年為閏九月，與我計算的閏八月不一致，台灣中央研究院的<a href="http://sinocal.sinica.edu.tw/" target="_blank">兩千年中西曆轉換網站</a>和汪曰楨的《歷代長術輯要》也記北齊武平六年為閏八月，所以這裡不取《三千五百年历日天象》的數據。</p>'
        else:
            return '<p style="color:red;">《三千五百年历日天象》附表3记北齐武平六年为闰九月，与我计算的闰八月不一致，台湾中央研究院的<a href="http://sinocal.sinica.edu.tw/" target="_blank">两千年中西历转换网站</a>和汪曰桢的《历代长术辑要》也记北齐武平六年为闰八月，所以这里不取《三千五百年历日天象》的数据。</p>'
        
    return ''

def ChineseYearNoteTang(y, lang, calendar):
    if y==678 and calendar=='default':
        if lang=='Eng':
            return '<p style="color:red;">The <i>Old Book of Tang</i> mentions leap month 10 in this year. However, the <i>New Book of Tang</i> mentions leap month 11. Many scholars adopt the information in the <i>New Book of Tang</i>. However, Huang Yi-Long, Professor in the Institute of History at the National Tsing-Hua University in Taiwan, <a href="http://ccsdb.ncl.edu.tw/ccs/image/01_010_002_01_11.pdf" target="_blank">investigated the issue</a> and concludes that the record in the <i>Old Book of Tang</i> is more reliable. His analysis places leap month 10 beginning on Nov. 19 and month 11 beginning on Dec. 19.</p>'
        elif lang=='ChiT':
            return '<p style="color:red;">《舊唐書》有儀鳳三年閏十月的記載，《新唐書》卻有閏十一月記載，學者一般取《新唐書》的閏月。但台灣國立清華大學歷史研究所的黃一農教授經過<a href="http://ccsdb.ncl.edu.tw/ccs/image/01_010_002_01_11.pdf" target="_blank">考證</a>後認為《舊唐書》的記載比較可信。根據他的考證，閏十月朔是癸丑(11月19日)，十一月朔是癸未(12月19日)。</p>'
        else:
            return '<p style="color:red;">《旧唐书》有仪凤三年闰十月的记载，《新唐书》却有闰十一月记载，学者一般取《新唐书》的闰月。但台湾国立清华大学历史研究所的黄一农教授经过<a href="http://ccsdb.ncl.edu.tw/ccs/image/01_010_002_01_11.pdf" target="_blank">考证</a>后认为《旧唐书》的记载比较可信。根据他的考证，闰十月朔是癸丑(11月19日)，十一月朔是癸未(12月19日)。</p>'

    if y==684 and calendar=='default':
        if lang=='Eng':
            return '<p style="color:red;">The New Year day in this year was supposed to be on Jan 22, 684, but it was moved to Jan 23 by edict.</p>'
        elif lang=='ChiT':
            return '<p style="color:red;">嗣聖元年正月朔本在癸未(684年1月22日)，但唐高宗在弘道元年八月下旨，強將十二月改為大月，使正月朔移至甲申(1月23日)。</p>'
        else:
            return '<p style="color:red;">嗣圣元年正月朔本在癸未(684年1月22日)，但唐高宗在弘道元年八月下旨，强将十二月改为大月，使正月朔移至甲申(1月23日)。</p>'

    if y > 696 and y < 699 and calendar=='default':
        if lang=='Eng':
            return '<p style="color:red;">In 697, Empress Consort Wu changed several calendar dates by edict in order to create a rare phenomenon that a winter solstice occurred on a jia zi day and coincided with a lunar conjunction. It was claimed that several predicted conjunction dates in the previous years were incorrect, resulting in the Moon being visible on the last days of lunar months. The claim was in fact incorrect and was a pretense for the empress to change calendar dates. After an "investigation," it was decided that the winter solstice should be moved two days later to the jia zi day (Dec. 20), which "happened to coincide" with the lunar conjunction. Because of this change, the lunar month started on Nov. 20, 697 became a leap month and the winter solstice became the New Year day. There was originally a leap month after month 12 in 698. In order to cancel the leap month, the middle solar term Z12 was moved from Jan 17, 698 to Jan 18, 698.</p>'
        elif lang=='ChiT':
            return '<p style="color:red;">萬歲通天二年，武則天為了營造正月甲子合朔冬至罕見曆象，偽稱曆官所推合朔時刻有不合天象，出現了「晦仍見月，有爽天經」之象，強將聖曆元年冬至移後兩日、大寒移後一日，使原本所推聖曆元年正月甲午朔變為通天二年閏十月甲午朔、聖曆元年十二月甲子朔變正月甲子朔，閏十二月癸巳朔變十二月癸巳朔。</p>'
        else:
            return '<p style="color:red;">万岁通天二年，武则天为了营造正月甲子合朔冬至罕见历象，伪称历官所推合朔时刻有不合天象，出现了「晦仍见月，有爽天经」之象，强将圣历元年冬至移后两日、大寒移后一日，使原本所推圣历元年正月甲午朔变为通天二年闰十月甲午朔、圣历元年十二月甲子朔变正月甲子朔，闰十二月癸巳朔变十二月癸巳朔。</p>'

    if y > 723 and y < 726 and calendar=='default':
        if lang=='Eng':
            return '<p style="color:red;">The New Year day in the Chinese year in 725 was supposed to be on Jan 19, 725 and there was a leap month after the first month. However, in order to prevent a solar eclipse on the New Year day, the leap month was moved to a month earlier by edict and became the last month in the Chinese year in 724 and the New Year day was moved to Feb 18, 725. The calendrical Z1 was also moved from Feb 16 to Feb 18 to be consistent with the change.</p>'
        elif lang=='ChiT':
            return '<p style="color:red;">開元十三年正月朔本在丙辰(725年1月19日)，為避正旦日食，當時強將閏月推前一月，使正月丙辰朔變閏十二月丙辰朔，閏正月丙戌朔(725年2月18日)變正月丙戌朔。曆書雨水(當時稱為啟蟄)本在甲申(2月16日)，亦強進為丙戌(2月18日)。</p>'
        else:
            return '<p style="color:red;">开元十三年正月朔本在丙辰(725年1月19日)，为避正旦日食，当时强将闰月推前一月，使正月丙辰朔变闰十二月丙辰朔，闰正月丙戌朔(725年2月18日)变正月丙戌朔。历书雨水(当时称为启蛰)本在甲申(2月16日)，亦强进为丙戌(2月18日)。</p>'
        
    return ''

def ChineseYearNoteMingQing(y, lang):
    if y==1462:
        if lang=='Eng':
            return '<p style="color:red;"><i>3500 Years of Calendars and Astronomical Phenomena</i> lists the first day of month 11 on Nov. 22, which is inconsistent with the calendar issued by the Ming government (Nov. 21).</p>'
        elif lang=='ChiT':
            return '<p style="color:red;">《三千五百年历日天象》記十一月壬辰朔(11月22日)，不合當年的《大統曆》曆書(辛卯朔, 11月21日)，見<a href="http://ccsdb.ncl.edu.tw/ccs/image/01_010_002_01_11.pdf" target="_blank">「中國史曆表朔閏訂正舉隅 &mdash; 以唐《麟德曆》行用時期為例」</a>緒言。</p>'
        else:
            return '<p style="color:red;">《三千五百年历日天象》记十一月壬辰朔(11月22日)，不合当年的《大统历》历书(辛卯朔, 11月21日)，见<a href="http://ccsdb.ncl.edu.tw/ccs/image/01_010_002_01_11.pdf" target="_blank">「中国史历表朔闰订正举隅 &mdash; 以唐《麟德历》行用时期为例」</a>绪言。</p>'

    if y==1581:
        if lang=='Eng':
            return '<p style="color:red;"><i>3500 Years of Calendars and Astronomical Phenomena</i> lists the first day of month 10 on Oct. 28, which is inconsistent with the calendar issued by the Ming government (Oct. 27).</p>'
        elif lang=='ChiT':
            return '<p style="color:red;">《三千五百年历日天象》記十月壬辰朔(10月28日)，不合當年的《大統曆》曆書(辛卯朔, 10月27日)，見《國家圖書館藏明代大統曆日彙編》第三冊第606頁。</p>'
        else:
            return '<p style="color:red;">《三千五百年历日天象》记十月壬辰朔(10月28日)，不合当年的《大统历》历书(辛卯朔, 10月27日)，见《国家图书馆藏明代大统历日汇编》第三册第606页。</p>'

    if y==1588:
        if lang=='Eng':
            return '<p style="color:red;"><i>3500 Years of Calendars and Astronomical Phenomena</i> lists the first day of month 3 on Mar. 26, the first day of month 4 on Apr. 25, and the first day of month 12 on Jan. 17. These are inconsistent with the dates in the calendar issued by the Ming government (Mar. 27, Apr. 26 and Jan. 16).</p>'
        elif lang=='ChiT':
            return '<p style="color:red;">《三千五百年历日天象》記三月癸未朔(3月26日)、四月癸丑朔(4月25日)、十二月庚辰朔(1月17日)，不合當年的《大統曆》曆書(三月甲申朔, 3月27日; 四月甲寅朔, 4月26日; 十二月己卯朔, 1月16日)，見《國家圖書館藏明代大統曆日彙編》第四冊第135、139、175頁。</p>'
        else:
            return '<p style="color:red;">《三千五百年历日天象》记三月癸未朔(3月26日)、四月癸丑朔(4月25日)、十二月庚辰朔(1月17日)，不合当年的《大统历》历书(三月甲申朔, 3月27日; 四月甲寅朔, 4月26日; 十二月己卯朔, 1月16日)，见《国家图书馆藏明代大统历日汇编》第四册第135页、139页、175页。</p>'

    if y==1600:
        if lang=='Eng':
            return '<p style="color:red;"><i>3500 Years of Calendars and Astronomical Phenomena</i> lists the New Year day on Feb. 14, which is inconsistent with the calendar issued by the Ming government (Feb. 15).</p>'
        elif lang=='ChiT':
            return '<p style="color:red;">《三千五百年历日天象》記正月乙巳朔(2月14日)，不合當年的《大統曆》曆書(丙午朔, 2月15日)，見《國家圖書館藏明代大統曆日彙編》第四冊第445頁。</p>'
        else:
            return '<p style="color:red;">《三千五百年历日天象》记正月乙巳朔(2月14日)，不合当年的《大统历》历书(丙午朔, 2月15日)，见《国家图书馆藏明代大统历日汇编》第四册第445页。</p>'

    if y==1609:
        if lang=='Eng':
            return '<p style="color:red;"><i>3500 Years of Calendars and Astronomical Phenomena</i> lists the New Year day on Feb. 4, which is inconsistent with the calendar issued by the Ming government (Feb. 5).</p>'
        elif lang=='ChiT':
            return '<p style="color:red;">《三千五百年历日天象》記正月癸未朔(2月4日)，不合當年的《大統曆》曆書(甲申朔, 2月5日)，見《國家圖書館藏明代大統曆日彙編》第五冊第67頁。</p>'
        else:
            return '<p style="color:red;">《三千五百年历日天象》记正月癸未朔(2月4日)，不合当年的《大统历》历书(甲申朔, 2月5日)，见《国家图书馆藏明代大统历日汇编》第五册第67页。</p>'
        
    if y==1645:
        if lang=='Eng':
            return '<p style="color:red;">Note that leap month 6 contained the major solar term Z6, breaking the rule that a leap month must not contain a major solar term. Wang Yuezhen (汪曰楨), a Chinese mathematician in the 19th century, explained that even though the solar term Z6 and the lunar conjunction associated with the month occurred on the same day, Z6 occurred earlier in the day than the lunar conjunction and was counted as a major solar term of the previous month. As a result, leap month 6 did not contain any major solar term. This "rule" was only used in this year. It was never used again after this year.</p>'
        elif lang=='ChiT':
            return '<p style="color:red;">中氣大暑出現在閏六月初一，違反了閏月不含中氣的規定。清朝曆算家汪曰楨解釋說雖然大暑與朔發生在同一日，大暑的時刻早於合朔時刻，屬於前月之中氣，所以閏六月不含中氣。這說法明顯不合傳統，屬於新的置閏法則，但是這新法則只在這一年用過，以後不再使用。</p>'
        else:
            return '<p style="color:red;">中气大暑出现在闰六月初一，违反了闰月不含中气的规定。清朝历算家汪曰桢解释说虽然大暑与朔发生在同一日，大暑的时刻早于合朔时刻，属于前月之中气，所以闰六月不含中气。这说法明显不合传统，属于新的置闰法则，但是这新法则只在这一年用过，以后不再使用。</p>'
    
    if y==1662:
        if lang=='Eng':
            return '<p style="color:red;">The New Year Day was originally on Feb. 19. There was a leap month after month 7 in the previous year and two major solar terms (Z11 and Z12) in month 11. The major solar term Z1 was originally placed on the last day of month 12 in the previous year, leaving the first month in this year without a major solar term. To avoid controversy, the New Year Day was moved to Feb. 18 so that the first month would contain Z1, thus moving the month without major solar term to the last month of the previous year.</p>'
        elif lang=='ChiT':
            return '<p style="color:red;">正月朔本在丙子日(2月19日)，事緣順治十八年閏七月，當年十一月含冬至和大寒兩中氣，雨水本來定在十二月晦，但這使康熙元年正月不含中氣。為免遭人非議，欽天監將正月朔提前一日至乙亥日(2月18日)，使正月含雨水，無中氣月便移到十二月。</p>'
        else:
            return '<p style="color:red;">正月朔本在丙子日(2月19日)，事缘顺治十八年闰七月，当年十一月含冬至和大寒两中气，雨水本来定在十二月晦，但这使康熙元年正月不含中气。为免遭人非议，钦天监将正月朔提前一日至乙亥日(2月18日)，使正月含雨水，无中气月便移到十二月。</p>'
    
    if y==1679:
        if lang=='Eng':
            return "<p style='color:red;'>In both <i>3500 Years of Calendars and Astronomical Phenomena</i> (by Zhang Peiyu) and <i>A Chinese calendar translated into the western calendar from 1516 to 1941</i> (by Zheng Hesheng), the calendrical solar term Z4 is listed on May 20. However, the Shixian Calendar for the 18th year of Emperor Kangxi's Reign (i.e. Feb. 11, 1679 - Jan. 30, 1680), a yearly calendar issued by the Imperial Astronomical Bureau in the Qing dynasty, lists Z4 on May 21 at 9:01am in Beijing's local apparent solar time. The calendarical solar term for Z4 is listed on May 21 here based on the Shixian Calendar.</p>"
        elif lang=='ChiT':
            return '<p style="color:red;">張培瑜《三千五百年历日天象》和鄭鶴聲《近世中西史日對照表》皆記小滿為5月20日，但《大清康熙十八年歲次己未時憲曆》則載「(四月)十二日丙子巳初初刻一分小滿四月中」，即小滿在四月十二日(公曆5月21日)九時零一分(北京地方真太陽時)。這裡根據《大清時憲曆》記曆書小滿為公曆5月21日。</p>'
        else:
            return '<p style="color:red;">张培瑜《三千五百年历日天象》和郑鹤声《近世中西史日对照表》皆记小满为5月20日，但《大清康熙十八年岁次己未时宪历》则载「(四月)十二日丙子巳初初刻一分小满四月中」，即小满在四月十二日(公历5月21日)九时零一分(北京地方真太阳时)。这里根据《大清时宪历》记历书小满为公历5月21日。</p>'
        
    return ''

def ChineseYearNoteSouthernMingZheng(y, lang):
    if y==1648:
        if lang=='Eng':
            return '<p style="color:red;">Several sources indicate that the leap month in this year was after the 6th month, which I find to be very unlikely.</p>'
        elif lang=='ChiT':
            return '<p style="color:red;">王叔武"南明史料朔閏考異"引 《劫灰錄》、 《鹿樵紀聞》、 《明季南略》、 《爝火錄》說這年閏六月，我認為閏六月很可能不對。</p>'
        else:
            return '<p style="color:red;">王叔武"南明史料朔闰考异"引 《劫灰录》、 《鹿樵纪闻》、 《明季南略》、 《爝火录》说这年闰六月，我认为闰六月很可能不对。</p>'
    if y==1649:
        if lang=='Eng':
            return '<p style="color:red;">Two dfferent versions of calendar in the Southern Ming dynasty were produced in this year. One of them was produced by the officials of the Yongli emperor, in which the New Year day was on February 11th, 1649. Another version was produced by the officials of the Prince of Lu, who named himself regent. The New Year day of the Lu calendar was on February 12th, 1649. According to the calculation of the Datong system, the New Year day was on February 11th, 1649.</p>'
        elif lang=='ChiT':
            return '<p style="color:red;">永曆三年和魯王監國四年正月朔有異:永曆三年正月庚申朔;《魯監國大統曆》則有魯監國四年正月辛酉朔。依明大統曆推算此年正月為庚申朔。</p>'
        else:
            return '<p style="color:red;">永历三年和鲁王监国四年正月朔有异:永历三年正月庚申朔;《鲁监国大统历》则有鲁监国四年正月辛酉朔。依明大统历推算此年正月为庚申朔。</p>'
    if y==1650:
        if lang=='Eng':
            return "<p style='color:red;'>According to <i>C&#225;n M&#237;ng D&#224; T&#466;ng L&#236;</i> or <i>Datong Calendar of the Waning Ming Dynasty</i> by Fu Yili and <i>Y&#225;n P&#237;ng W&#225;ng H&#249; Gu&#257;n Y&#225;ng Y&#299;ng C&#243;ng Zh&#275;ng Sh&#237; L&#249;</i> (or <i>Account of the quartermaster Yang Ying's campaign with Prince Yanping</i>), the leap month in this year was after the 11th month in the Southern Ming calendar. This is consistent with the calculation by the Datong system. However, the Datong calendars produced by the Zheng dynasty for 1671, 1676 and 1677 recorded the leap month to be after the 12th month. Leap month 12 was probably based on an unofficial calendar expediently produced by the Zheng officials in 1649 since the official emperor calendar had not arrived in time because of war.</p>"
        elif lang=='ChiT':
            return '<p style="color:red;">傅以禮《殘明大統曆》和《延平王戶官楊英從征實錄》記永曆四年閏十一月，符合大統曆的推算，但明鄭頒行的《永曆二十五年大統曆》、《永曆三十年大統曆》及《永曆三十一年大統曆》都記永曆四年閏十二月。閏十二月或許是當年鄭氏命官員權宜頒行的大統曆推算出的。</p>'
        else:
            return '<p style="color:red;">傅以礼《残明大统历》和《延平王户官杨英从征实录》记永历四年闰十一月，符合大统历的推算，但明郑颁行的《永历二十五年大统历》、《永历三十年大统历》及《永历三十一年大统历》都记永历四年闰十二月。闰十二月或许是当年郑氏命官员权宜颁行的大统历推算出的。</p>'
    if y==1652:
        if lang=='Eng':
            return "<p style='color:red;'>Two dfferent versions of calendar were produced in this year: emperor Yongli's and Lu's version. The New Year day of the Yongli calendar was on February 10th, 1652. The New Year day of the Lu calendar was on February 9th, 1652. According to the calculation of the Datong system, the New Year day was on February 10th, 1652.</p>"
        elif lang=='ChiT':
            return '<p style="color:red;">永曆六年和魯王監國七年正月朔有異:永曆六年正月甲戌朔;《魯監國大統曆》則有魯監國七年正月癸酉朔。依明大統曆推算此年正月為甲戌朔。</p>'
        else:
            return '<p style="color:red;">永历六年和鲁王监国七年正月朔有异:永历六年正月甲戌朔;《鲁监国大统历》则有鲁监国七年正月癸酉朔。依明大统历推算此年正月为甲戌朔。</p>'
    if y==1653:
        if lang=='Eng':
            return "<p style='color:red;'>There are discrepancies in the leap month in this year among various sources. <i>Datong Calendar of the Waning Ming Dynasty</i> records the leap month to be after the 7th month, which is consistent with the caleculation of the Datong system. <i>Account of the quartermaster Yang Ying's campaign with Prince Yanping</i> has the leap month after the 8th month. The chronicle <i>X&#237;ng Z&#224;i Y&#225;ng Qi&#363;</i> records the leap month to be after the 6th month. The Datong calendar produced by the Zheng dynasty for 1671 also records leap month after the 6th month. However, in the Datong calendar for 1676 and 1677, the leap month is changed to being after the 8th month. I think leap month 6 is unlikely. Both leap month 7 and 8 are possible. Here I follow <i>Datong Calendar of the Waning Ming Dynasty</i> and place the leap month after the 7th month.</p>"
        elif lang=='ChiT':
            return '<p style="color:red;">永曆七年的閏月有爭議，依大統曆推算閏七月，傅以禮《殘明大統曆》亦記閏七月，但是《延平王戶官楊英從征實錄》記閏八月，《行在陽秋》記閏六月，明鄭頒行的《永曆二十五年大統曆》也記閏六月，但是後來頒行的《永曆三十年大統曆》及《永曆三十一年大統曆》卻改為閏八月。我認為閏六月不大可能，閏七月和閏八月機會較大，此處依《殘明大統曆》記閏七月。</p>'
        else:
            return '<p style="color:red;">永历七年的闰月有争议，依大统历推算闰七月，傅以礼《残明大统历》亦记闰七月，但是《延平王户官杨英从征实录》记闰八月，《行在阳秋》记闰六月，明郑颁行的《永历二十五年大统历》也记闰六月，但是后来颁行的《永历三十年大统历》及《永历三十一年大统历》却改为闰八月。我认为闰六月不大可能，闰七月和闰八月机会较大，此处依《残明大统历》记闰七月。</p>'
    if y==1663:
        if lang=='Eng':
            return '<p style="color:red;">Calendrical J8 should be on September 6th according to the calculation of the Datong system. However, <i>Cán Míng Dà Tǒng Lì</i> or <i>Datong Calendar of the Waning Ming Dynasty</i> records J8 on September 5th, which is the date listed here.</p>'
        elif lang=='ChiT':
            return '<p style="color:red;">依大統曆推算白露在八月初五(公曆9月6日)，但傅以禮《殘明大統曆》記八月初四(9月5日)，此處曆書白露依《殘明大統曆》。</p>'
        else:
            return '<p style="color:red;">依大统历推算白露在八月初五(公历9月6日)，但傅以礼《残明大统历》记八月初四(9月5日)，此处历书白露依《残明大统历》。</p>'
    if y==1671:
        if lang=='Eng':
            return "<p style='color:red;'>The New Year day was on February 9th, 1671 according to <i>Datong Calendar of the Waning Ming Dynasty</i>, which also agrees with the calculation of the Datong system. However, the Datong calendar produced by the Zheng dynasty for 1671 indicates that the New Year day was on February 10th, 1671. Even though Zheng dynasty claimed that their calendars were produced expediently and should not to be taken as official, by this time the Yongli emperor had died and the Southern Ming dynasty had already ended. Zheng's calendar became the de facto official Datong calendar of the state. So I change the New Year day to February 10th, 1671 in accord with Zheng's calendar.</p>"
        elif lang=='ChiT':
            return '<p style="color:red;">依大統曆推算永曆二十五正月癸丑朔，傅以禮《殘明大統曆》亦記正月癸丑朔，但是明鄭頒行的《永曆二十五年大統曆》記正月甲寅朔。雖然鄭氏奉明正朔，聲稱其大統曆乃「權宜頒行」，但是當時永曆帝已死，南明也已亡，明鄭的大統曆變相成為正統的大統曆書，所以此處依明鄭大統曆記正月甲寅朔。</p>'
        else:
            return '<p style="color:red;">依大统历推算永历二十五正月癸丑朔，傅以礼《残明大统历》亦记正月癸丑朔，但是明郑颁行的《永历二十五年大统历》记正月甲寅朔。虽然郑氏奉明正朔，声称其大统历乃「权宜颁行」，但是当时永历帝已死，南明也已亡，明郑的大统历变相成为正统的大统历书，所以此处依明郑大统历记正月甲寅朔。</p>'
    if y==1674:
        if lang=='Eng':
            return '<p style="color:red;">According to the calculation of the Datong system, the month 6 conjunction was on July 4th and month 9 conjunction was on September 30th. These dates are inconsistent with the records in <i>Datong Calendar of the Waning Ming Dynasty</i> (July 3rd and September 29th). The dates here are based on the records in <i>Datong Calendar of the Waning Ming Dynasty</i>.</p>'
        elif lang=='ChiT':
            return '<p style="color:red;">依明大統曆推算永曆二十八年六月甲午朔及九月壬戌朔，此處依傅以禮《殘明大統曆》改為六月癸巳朔和九月辛酉朔。</p>'
        else:
            return '<p style="color:red;">>依明大统历推算永历二十八年六月甲午朔及九月壬戌朔，此处依傅以礼《残明大统历》改为六月癸巳朔和九月辛酉朔。'
    if y==1675:
        if lang=='Eng':
            return '<p style="color:red;">According to the calculation of the Datong system, a conjunction occurred on July 22nd this year. <i>Datong Calendar of the Waning Ming Dynasty</i> records a conjunction on July 23rd. The one-day difference changed the leap month in this year. July 22nd conjunction resulted in a leap month after the 5th month. July 23rd conjunction resulted in a leap month after the 6th month. Leap month 6 is also recorded in the calendars produced by the Zheng dynasty for 1677. So I use the data in <i>Datong Calendar of the Waning Ming Dynasty</i>.</p>'
        elif lang=='ChiT':
            return '<p style="color:red;">依明大統曆推算永曆二十九年有朔日在丁巳(公曆7月22日)，對應的朔日在傅以禮《殘明大統曆》出現在下一日戊午(7月23日)。此一日之差造成閏月分歧:依大統曆推算閏五月，《殘明大統曆》則為閏六月。明鄭頒行的《永曆三十年大統曆》及《永曆三十一年大統曆》都記永曆二十九年閏六月，所以此處朔閏依《殘明大統曆》。</p>'
        else:
            return '<p style="color:red;">依明大统历推算永历二十九年有朔日在丁巳(公历7月22日)，对应的朔日在傅以礼《残明大统历》出现在下一日戊午(7月23日)。此一日之差造成闰月分歧:依大统历推算闰五月，《残明大统历》则为闰六月。明郑颁行的《永历三十年大统历》及《永历三十一年大统历》都记永历二十九年闰六月，所以此处朔闰依《残明大统历》。</p>'
    if y==1676:
        if lang=='Eng':
            return '<p style="color:red;"><i>Cán Míng Dà Tǒng Lì</i> or <i>Datong Calendar of the Waning Ming Dynasty</i> records that Z11 (winter solstice) was on the 16th day in month 11 (Dec. 20), which is inconsistent with the calculation of the Datong system (Dec. 21). The official Datong Calendar for 1676 records Z11 on the 17th day in month 11 (Dec. 21). So the Z11 date in <i>Datong Calendar of the Waning Ming Dynasty</i> is wrong.</p>'
        elif lang=='ChiT':
            return '<p style="color:red;">《殘明大統曆》記冬至在十一月十六(公曆12月20日)，不合明大統曆的推步(十一月十七)。明鄭頒行的《永曆三十年大統曆》記冬至在十一月十七(12月21日)，證實《殘明大統曆》的冬至日期錯了。</p>'
        else:
            return '<p style="color:red;">《残明大统历》记冬至在十一月十六(公历12月20日)，不合明大统历的推步(十一月十七)。明郑颁行的《永历三十年大统历》记冬至在十一月十七(12月21日)，证实《残明大统历》的冬至日期错了。</p>'
    if y==1677:
        if lang=='Eng':
            return '<p style="color:red;">According to the calculation of the Datong system, the month 7 conjunction was on July 29th, which is inconsistent with July 30th recorded in <i>Datong Calendar of the Waning Ming Dynasty</i> and the calendar produced by the Zheng dynasty for 1677. The Zheng calendar date is used here.</p>'
        elif lang=='ChiT':
            return '<p style="color:red;">依明大統曆推算永曆三十一年七月乙亥朔，不合傅以禮《殘明大統曆》及明鄭《永曆三十一年大統曆》的丙子朔。此處依《殘明大統曆》及明鄭大統曆記七月丙子朔。</p>'
        else:
            return '<p style="color:red;">依明大统历推算永历三十一年七月乙亥朔，不合傅以礼《残明大统历》及明郑《永历三十一年大统历》的丙子朔。此处依《残明大统历》及明郑大统历记七月丙子朔。</p>'
    if y==1678:
        if lang=='Eng':
            return '<p style="color:red;">According to the calculation of the Datong system, the month 6 conjunction was on July 18th, inconsistent with July 19th recorded in <i>Datong Calendar of the Waning Ming Dynasty</i>. July 19th is used here.</p>'
        elif lang=='ChiT':
            return '<p style="color:red;">依明大統曆推算永曆三十二年六月己巳朔，不合傅以禮《殘明大統曆》的庚午朔。此處依《殘明大統曆》記六月庚午朔。</p>'
        else:
            return '<p style="color:red;">依明大统历推算永历三十二年六月己巳朔，不合傅以礼《残明大统历》的庚午朔。此处依《残明大统历》记六月庚午朔。</p>'
    if y==1682:
        if lang=='Eng':
            return '<p style="color:red;">According to the calculation of the Datong system, the New Year day was on February 8th, inconsistent with February 7th recorded in <i>Datong Calendar of the Waning Ming Dynasty</i>. February 7th is used here.</p>'
        elif lang=='ChiT':
            return '<p style="color:red;">依明大統曆推算永曆三十六年正月庚戌朔，不合傅以禮《殘明大統曆》的己酉朔。此處依《殘明大統曆》記正月己酉朔。</p>'
        else:
            return '<p style="color:red;">依明大统历推算永历三十六年正月庚戌朔，不合傅以礼《残明大统历》的己酉朔。此处依《残明大统历》记正月己酉朔。</p>'
    return ''

def ChineseYearNoteAfter2050(y, lang):
    early_note = {'Eng':' is close to the midnight. The start day of the month may be one day earlier.', 
                  'ChiT':'的時刻接近午夜零時，初一或會提早一天。', 
                  'ChiS':'的时刻接近午夜零时，初一或会提早一天。'}
    late_note = {'Eng':' is close to the midnight. The start day of the month may be one day later.', 
                 'ChiT':'的時刻接近午夜零時，初一或會推遲一天。',
                 'ChiS':'的时刻接近午夜零时，初一或会推迟一天。'}
    if y==2057 or y==2133 or y==2172:
        if lang=='Eng':
            note = '<p style="color:red;">The month 9 conjunction'
        else:
            note = '<p style="color:red;">九月朔'
        note += early_note[lang] + '</p>'
        return note
    if y==2089:
        if lang=='Eng':
            note = '<p style="color:red;">The month 8 conjunction'
        else:
            note = '<p style="color:red;">八月朔'
        note += late_note[lang] + '</p>'
        return note
    if y==2097:
        if lang=='Eng':
            note = '<p style="color:red;">The month 7 conjunction'
        else:
            note = '<p style="color:red;">七月朔'
        note += early_note[lang] + '</p>'
        return note
    if y==2115:
        if lang=='Eng':
            note = '<p style="color:red;">The month 2 conjunction'
        else:
            note = '<p style="color:red;">二月朔'
        note += late_note[lang] + '</p>'
        return note
    if y==2116:
        if lang=='Eng':
            note = '<p style="color:red;">The month 4 conjunction'
        else:
            note = '<p style="color:red;">四月朔'
        note += late_note[lang] + '</p>'
        return note
    if y==2165:
        if lang=='Eng':
            note = '<p style="color:red;">The month 11 conjunction'
        else:
            note = '<p style="color:red;">十一月朔'
        note += early_note[lang] + '</p>'
        return note
    
    suffix = {'Eng':' is close to midnight. The actual date may be off by one day.',
              'ChiT':'的時刻接近午夜零時，實際日期或會與所示日期有一日之差。',
              'ChiS':'的时刻接近午夜零时，实际日期或会与所示日期有一日之差。'}
    if y==2051:
        if lang=='Eng':
            note = 'The time of Z2 (March equinox)' + suffix['Eng']
        else:
            note = '春分' + suffix[lang]
        return '<p style="color:red;">' + note + '</p>'
    if y==2082: 
        if lang=='Eng':
            note = 'The time of J1 in month 12' + suffix['Eng']
        else:
            note = '十二月立春' + suffix[lang]
        return '<p style="color:red;">' + note + '</p>'
    if y==2084:
        if lang=='Eng':
            note = 'The time of Z2 (March equinox)' + suffix['Eng']
        else:
            note = '春分' + suffix[lang]
        return '<p style="color:red;">' + note + '</p>'
    if y==2114:
        if lang=='Eng':
            note = 'The time of Z10' + suffix['Eng']
        else:
            note = '小雪' + suffix[lang]
        return '<p style="color:red;">' + note + '</p>'
    if y==2142: 
        if lang=='Eng':
            note = 'The time of J8' + suffix['Eng']
        else:
            note = '白露' + suffix[lang]
        return '<p style="color:red;">' + note + '</p>'
    if y==2155:
        if lang=='Eng':
            note = 'The time of Z9' + suffix['Eng']
        else:
            note = '霜降' + suffix[lang]
        return '<p style="color:red;">' + note + '</p>'
    if y==2157:
        if lang=='Eng':
            note = 'The time of Z11 (December solstice)' + suffix['Eng']
        else:
            note = '冬至' + suffix[lang]
        return '<p style="color:red;">' + note + '</p>'
    if y==2183:
        if lang=='Eng':
            note = 'The time of Z2 (March equinox)' + suffix['Eng']
        else:
            note = '春分' + suffix[lang]
        return '<p style="color:red;">' + note + '</p>'
    if y==2186:
        if lang=='Eng':
            note = 'The time of J1 in month 1' + suffix['Eng']
        else:
            note = '正月立春' + suffix[lang]
        return '<p style="color:red;">' + note + '</p>'
    return ''
