import requests
import unicodedata2
from gcp_tts_calls import list_languages

available = list_languages()
languages = []
for i in available:
    languages.append(i[:len(i)-3])

shortened = ['af-ZA','ar-XA','bg-BG','cmn-CN','cmn-TW','cs-CZ','da-DK','de-DE','el-GR','en-AU','en-GB',
             'en-IN','en-US','es-ES','fi-FI','fil-PH','fr-CA','fr-FR','hu-HU','id-ID','is-IS','it-IT',
             'ja-JP','ko-KR','lv-LV','ms-MY','nb-NO','nl-BE','nl-NL','pl-PL','pt-BR','pt-PT','ro-RO',
             'ru-RU','sk-SK','sr-RS','sv-SE','th-TH','tr-TR','uk-UA','vi-VN','yue-HK']
countries = []
for i in shortened:
    countries.append(i[-2:])

mapping = {'AD':'ES','AE':'XA','AF':'XA','AG':'US','AI':'US','AL':'IT','AM':'RU','AO':'PT','AQ':'US',
          'AR':'ES','AS':'US','AT':'DE','AU':'AU','AW':'NL','AX':'SE','AZ':'TR','BA':'RS','BB':'US',
          'BD':'IN','BE':'BE','BF':'FR','BG':'BG','BH':'XA','BI':'FR','BJ':'FR','BL':'FR','BM':'US',
          'BN':'MY','BO':'ES','BQ':'NL','BR':'BR','BS':'US','BT':'IN','BV':'NO','BW':'US','BY':'RU',
          'BZ':'GB','CA':'CA','CC':'MY','CD':'FR','CF':'FR','CG':'FR','CH':'DE','CI':'FR','CK':'AU',
          'CL':'ES','CM':'FR','CN':'CN','CO':'ES','CR':'ES','CU':'ES','CV':'PT','CW':'NL','CX':'US',
          'CY':'GR','CZ':'CZ','DE':'DE','DJ':'XA','DK':'DK','DM':'GB','DO':'ES','DZ':'XA','EC':'ES',
          'EE':'FI','EG':'XA','EH':'XA','ER':'XA','ES':'ES','ET':'XA','FI':'FI','FJ':'GB','FK':'US',
          'FM':'US','FO':'DK','FR':'FR','GA':'FR','GB':'GB','GD':'GB','GE':'US','GF':'FR','GG':'US',
          'GH':'US','GI':'US','GL':'IS','GM':'US','GN':'FR','GP':'FR','GQ':'ES','GR':'GR','GS':'US',
          'GT':'ES','GU':'US','GW':'PT','GY':'US','HK':'HK','HM':'AU','HN':'ES','HR':'RS','HT':'FR',
          'HU':'HU','ID':'ID','IE':'GB','IL':'XA','IM':'GB','IN':'IN','IO':'GB','IQ':'XA','IR':'XA',
          'IS':'IS','IT':'IT','JE':'GB','JM':'US','JO':'XA','JP':'JP','KE':'US','KG':'RU','KH':'VN',
          'KI':'US','KM':'FR','KN':'US','KP':'KR','KR':'KR','KW':'XA','KY':'GB','KZ':'RU','LA':'TH',
          'LB':'XA','LC':'US','LI':'DE','LK':'IN','LR':'US','LS':'US','LT':'LV','LU':'FR','LV':'LV',
          'LY':'XA','MA':'XA','MC':'FR','MD':'RO','ME':'RS','MF':'FR','MG':'FR','MH':'US','MK':'CZ',
          'ML':'FR','MM':'CN','MN':'CN','MO':'CN','MP':'US','MQ':'FR','MR':'XA','MS':'US','MT':'US',
          'MU':'US','MV':'IN','MW':'US','MX':'ES','MY':'MY','MZ':'PT','NA':'US','NC':'FR','NE':'FR',
          'NF':'AU','NG':'US','NI':'ES','NL':'NL','NO':'NO','NP':'IN','NR':'AU','NU':'AU','NZ':'AU',
          'OM':'XA','PA':'ES','PE':'ES','PF':'FR','PG':'US','PH':'PH','PK':'XA','PL':'PL','PM':'FR',
          'PN':'GB','PR':'ES','PS':'XA','PT':'PT','PW':'AU','PY':'ES','QA':'XA','RE':'FR','RO':'RO',
          'RS':'RS','RU':'RU','RW':'US','SA':'XA','SB':'AU','SC':'FR','SD':'XA','SE':'SE','SG':'MY',
          'SH':'GB','SI':'RS','SJ':'NO','SK':'SK','SL':'US','SM':'IT','SN':'FR','SO':'XA','SR':'NL',
          'SS':'US','ST':'PT','SV':'ES','SX':'NL','SY':'XA','SZ':'ZA','TC':'GB','TD':'FR','TF':'FR',
          'TG':'FR','TH':'TH','TJ':'XA','TK':'US','TL':'PT','TM':'TR','TN':'XA','TO':'US','TR':'TR',
          'TT':'US','TV':'GB','TW':'TW','TZ':'US','UA':'UA','UG':'US','UM':'US','US':'US','UY':'ES',
          'UZ':'TR','VA':'IT','VE':'US','VG':'GB','VI':'US','VN':'VN','VU':'US','WF':'FR','WS':'AU',
          'YE':'XA','YT':'FR','ZA':'ZA','ZM':'US','ZW':'US'}
    

def detect_language(name):
    dic = {'ARABIC':'ar','CYRILLIC':'ru','BENGALI':'bn','LATIN':'en','CJK':'cmn','GREEK':'el',
           'GUJARATI':'gu','DEVANAGARI':'hi','KANNADA':'kn','MALAYALAM':'ml','GURMUKHI':'pa',
           'TAMIL':'ta','TELUGU':'te','THAI':'th'}
    ch = name[0]
    temp = unicodedata2.name(ch)
    temp = temp.split(' ')
    key = temp[0]
    if key in dic:
        return dic[key]
    return 'en'
    


def name_to_locale(name, pref_name):
    
    pref_name.strip()
    lang = detect_language(pref_name)
    if lang != 'en':
        j = languages.index(lang)
        return available[j]
    
    try:
        name = name.lower()
        name = name.strip()
        name.replace('.','')
        name = name.replace(" ", "%20")
        url = "https://v2.namsor.com/NamSorAPIv2/api2/json/country/" + name
        headers = {
         "Accept": "application/json",
         "X-API-KEY": "528343c43d73091c6772a48062521eb3"
        }
        response = requests.request("GET", url, headers=headers)
        js = response.json()
        coun = js['country']
    except:
        coun = 'US'
    if coun in mapping:
        coun = mapping[coun]
    else:
        coun = 'US'
    if coun not in countries:
        coun = 'US'
    j = countries.index(coun)
    return shortened[j]