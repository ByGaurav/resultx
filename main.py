# Programmed by Mr. Gaurav Gupta
# It is an Original Work and Should not be copied for any Purpose
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from PIL import Image
from io import BytesIO
from pyxlsb import open_workbook as open_xlsb
st.set_page_config(layout="wide",page_icon="rocket",page_title="CBSE X Result Analysis")

# Remove and Inject CSS  
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            viewerBadge_container__1QSob {display: none;}
            footer {visibility: hidden}
            header {visibility: hidden;}
            .css-1rs6os {visibility: hidden;}
            .css-17ziqus {visibility: hidden;}
.css-18e3th9 {
                    padding-top: 0rem;
                    padding-bottom: 10rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
               .css-1d391kg {
                    padding-top: 3.5rem;
                    padding-right: 1rem;
                    padding-bottom: 3.5rem;
                    padding-left: 1rem;
                }
                </style>
            """

st.markdown(hide_st_style,unsafe_allow_html=True)
st.info('Disclaimer: Programmer is not responsible for any errors or omissions, or for the results obtained from the use of this information. All information in this site is provided "as is", with no guarantee of completeness, accuracy, timeliness or of the results obtained from the use of this information...')
user_input1, user_input2 = st.columns([1,2])
with user_input1:
  rno = st.text_input('Enter First Roll Number')
  if rno.isdigit():
    rno = int(float(rno))
  else:
    st.stop()
  

# Check Uplaoded File
with user_input2:
  data_file = st.file_uploader("",type=["txt"])
#data_file = st.file_uploader("",type=["txt"],help="Uplaod File Recieved From CBSE. Don't Make Any Changes to the File Recieved from CBSE, Upload as it is after Downloading")
if not data_file:
  st.stop()
school_code = data_file.name[:-4]
clean_file = school_code+"_clean.txt"
excel_file = school_code+".xlsx"

# Creating Empty DataFrame
df = pd.DataFrame(columns = ['R.No.','NAME','SUB1','MRK1','GRD1','SUB2','MRK2','GRD2','SUB3','MRK3','GRD3','SUB4','MRK4','GRD4','SUB5','MRK5','GRD5','SUB6','MRK6','GRD6','SUB7','MRK7','GRD7','RESULT'])

# Creating Row for Result Late Student
def result_late(df,line1,rno):
  temp_list=[]
  temp_list.insert(0,rno-1)
  find_sub = ['002','085','184','101']
  idx ={}
  for x in find_sub:
    try:
      idx[x] = line1.index(x)
    except ValueError:
      idx=idx
  first_sub_code = min(idx, key=idx.get)
  sname=" ".join(line1[1:line1.index(first_sub_code)])
  del line1[0:line1.index(first_sub_code)]
  temp_list.insert(1,sname)
  for k in range(2,23):
    temp_list.insert(k,None)
  temp_list.insert(24,'R.L.')
  return temp_list
# Creating Row for Result Late Student Ends
  
f = data_file
for line in f:
  line = line.decode('ascii')
  if str(rno) in line:
    rno = rno + 1
    line1 = line.split() # Reading First line having the roll number
    line1.pop(1) # Removing Gender from the first line
    if 'R.L.' in line: 
      df.loc[len(df)] = result_late(df,line1,rno) # Sending Result Late Students to the Function
      continue # Going back to the begining of the For Loop as No second for R.L. Student
    line = next(f)
    line = line.decode('ascii')
    line = line.replace("F E", "E")
    line2 = line.split() # Line2 contains the score and grades
    temp_list = line2 # Creating Temporary List
    temp_list.insert(0,rno-1) 
    if len(temp_list)==11:
      temp_list += [None]
      temp_list += [None]
    if len(temp_list) == 13:
      temp_list += [None]
      temp_list += [None]
    find_sub = ['002','085','184','101'] #First Subject Which is Mandatory
# Finding Index of the Fisrt Subject
    idx ={}
    for x in find_sub:
      try:
        idx[x] = line1.index(x)
      except ValueError:
        idx=idx
    first_sub_code = min(idx, key=idx.get)
# Finding Index of the Fisrt Subject Ends
    sname=" ".join(line1[1:line1.index(first_sub_code)]) #Calculating Full Name
    del line1[0:line1.index(first_sub_code)] # Deleting Whole Data from the begining till the First Subject Code
    temp_list.insert(1,sname) # Inserting Student Name in the temp list
    if line1[len(line1)-2] == 'COMP': 
      del line1[len(line1)-1]#Deleting Subject Code of Compartment Subject
    temp_list.insert(16,line1[len(line1)-1]) #Inserting Result Pass/Fail/Comp
    del line1[len(line1)-1] #Deleting Result Pass/Fail/Comp from
# Adding Subject Codes to the temp list at required Positions
    if len(line1)>=5:
      temp_list.insert(2,line1[0])
      del line1[0]
      temp_list.insert(5,line1[0])
      del line1[0]
      temp_list.insert(8,line1[0])
      del line1[0]
      temp_list.insert(11,line1[0])
      del line1[0]
      temp_list.insert(14,line1[0])
      del line1[0]
    if len(line1)==2:
      temp_list.insert(17,line1[0])
      del line1[0]
      temp_list.insert(20,line1[0])
      del line1[0]
    if len(line1)==1:
      temp_list.insert(17,line1[0])
      del line1[0]
    if len(temp_list)==23:
      temp_list.insert(20,None)
    if len(temp_list)==22:
      temp_list.insert(17,None)
      temp_list.insert(17,None)
# Adding Subject Codes to the temp list at required Positions ENDS
    df.loc[len(df)] = temp_list # Creating DataFrame Row and For Loop Ends Here

cList=[3,6,9,12,15] # Creating List of Marks Index
df['Total']= df.iloc[:,cList].apply(pd.to_numeric, errors='coerce').sum(axis=1) #Calculating Total

# Creating Dictionary of Subject Codes
scode = {
"002":"HINDI COURSE-A",
"003":"URDU COURSE-A",
"004":"PUNJABI",
"005":"BENGALI",
"006":"TAMIL",
"007":"TELUGU",
"008":"SINDHI",
"009":"MARATHI",
"010":"GUJARATI",
"011":"MANIPURI",
"012":"MALAYALAM",
"013":"ODIA",
"014":"ASSAMESE",
"015":"KANNADA",
"016":"ARABIC",
"017":"TIBETAN",
"018":"FRENCH",
"020":"GERMAN",
"021":"RUSSIAN",
"023":"PERSIAN",
"024":"NEPALI",
"025":"LIMBOO",
"026":"LEPCHA",
"031":"CARNATIC MUSIC (VOCAL)",
"032":"CARNATIC MUSIC (MELODIC INSTRUMENTS)",
"033":"CARNATIC MUSIC (PERCUSSION INSTRUMENTS)",
"034":"HINDUSTANI MUSIC (VOCAL)",
"035":"HINDUSTANI MUSIC (MELODIC INSTRUMENTS)",
"036":"HINDUSTANI MUSIC (PERCUSSION INSTRUMENTS)",
"041":"MATHEMATICS -STANDARD",
"049":"PAINTING",
"064":"HOME SCIENCE",
"076":"NATIONAL CADET CORPS (NCC)",
"085":" HINDI COURSE-B",
"086":"SCIENCE",
"087":"SOCIAL SCIENCE",
"089":"TELUGU TELANGANA",
"091":"KOK BOROK",
"092":"BODO",
"093":"TANGKHUL",
"094":"JAPANESE",
"095":"BHUTIA",
"096":"SPANISH",
"097":"KASHMIRI",
"098":"MIZO",
"099":"BAHASA MELAYU",
"101":"ENGLISH COMMUNICATIVE",
"119":"SANSKRIT COMMUNICATIVE",
"122":"SANSKRIT",
"131":"RAI",
"132":"GURUNG",
"133":"TAMANG",
"134":"SHERPA",
"136":"THAI",
"154":"ELEMENTS OF BUSINESS",
"165":"COMPUTER APPLICATIONS",
"184":"ENGLISH LANG & LIT.",
"241":"MATHEAAATICS - BASIC",
"254":"ELEMENTS OF BOOKKEEPING & ACCOUNTANCY",
"303":"URDU COURSE-B",
"401":"Retailing",
"402":"Information Technology",
"403":"Security",
"404":"Automotive",
"405":"Introduction To Financial Markets",
"406":"Introduction To Tourism",
"407":"Beauty & Wellness",
"408":"Agriculture",
"409":"Food Production",
"410":"Front Office Operations",
"411":"Banking & Insurance",
"412":"Marketing & Sales",
"413":"Health Care",
"414":"Apparel",
"415":"Multi Media",
"416":"Multi Skill Foundation Course",
"417":"Artificial Intelligence",
"418":"Physical Activity Trainer (New)",
"419":"Data Science"
}
# Replacing Subject Codes with Subject Names
df['SUB1']=df['SUB1'].map(scode)
df['SUB2']=df['SUB2'].map(scode)
df['SUB3']=df['SUB3'].map(scode)
df['SUB4']=df['SUB4'].map(scode)
df['SUB5']=df['SUB5'].map(scode)
df['SUB6']=df['SUB6'].map(scode)
df['SUB7']=df['SUB7'].map(scode)

# Switch Columns i.e Total before result
df = df[['R.No.','NAME','SUB1','MRK1','GRD1','SUB2','MRK2','GRD2','SUB3','MRK3','GRD3','SUB4','MRK4','GRD4','SUB5','MRK5','GRD5','SUB6','MRK6','GRD6','SUB7','MRK7','GRD7','Total','RESULT']]
df.dropna(axis=1, how='all') # Drop Columns with all NaN Values
df.fillna('', inplace=True) # Remove NaN values
df.set_index('R.No.', inplace=True) # Setting Roll Number as Index
#Printing DataFrame
if df.empty:
  st.stop()
else:
  st.write('TOTAL STUDENTS: ',len(df.index))
  st.dataframe(df.astype(str))

#Calculating Comparment
df_abst = df.loc[df['RESULT'] == 'ABST']
if not df_abst.empty:
  st.write('ABSENT: ',len(df_abst.index))
  st.dataframe(df_abst.astype(str))

#Calculating Comparment
df_comp = df.loc[df['RESULT'] == 'COMP']
if not df_comp.empty:
  st.write('COMPARTMENT: ',len(df_comp.index))
  st.dataframe(df_comp.astype(str))

#Calculating Failures
df_fail = df.loc[df['RESULT'] == 'FAIL']
if not df_fail.empty:
  st.write('Failure: ',len(df_fail.index))
  st.dataframe(df_fail.astype(str))

#Calculating Result Late
df_rl = df.loc[df['RESULT'] == 'R.L.']
if not df_rl.empty:
  st.write('RESULT LATE: ',len(df_rl.index))
  st.dataframe(df_rl.astype(str))

df = df.reset_index(level=0)
#Creating Analysis DataFrame
def analy(subject):
  df1 = df[ (df.SUB1 == subject)][['R.No.','NAME', 'SUB1','MRK1','GRD1']]
  df1.columns = ['R.No.','NAME', 'SUB','MRK','GRD']
  df2 = df[ (df.SUB2 == subject)][['R.No.','NAME', 'SUB2','MRK2','GRD2']]
  df2.columns = ['R.No.','NAME', 'SUB','MRK','GRD']
  df3 = df[ (df.SUB3 == subject)][['R.No.','NAME', 'SUB3','MRK3','GRD3']]
  df3.columns = ['R.No.','NAME', 'SUB','MRK','GRD']
  df4= df[ (df.SUB4 == subject)][['R.No.','NAME', 'SUB4','MRK4','GRD4']]
  df4.columns = ['R.No.','NAME', 'SUB','MRK','GRD']
  df5 = df[ (df.SUB5 == subject)][['R.No.','NAME', 'SUB5','MRK5','GRD5']]
  df5.columns = ['R.No.','NAME', 'SUB','MRK','GRD']
  # Consider Additional Subject
  #df6 = df[ (df.SUB6 == subject)][['Name', 'SUB6','MRK6','GRD6']]
  #df6.columns = ['Name', 'Sub','MRK','GRD']

  df_sub = df1.append(df2, ignore_index = True) 
  df_sub = df_sub.append(df3, ignore_index = True)
  df_sub = df_sub.append(df4, ignore_index = True)
  df_sub = df_sub.append(df5, ignore_index = True)
  #df_sub = df_sub.append(df6, ignore_index = True)
  # Sorted Dataframe of Subject
  df_sub = df_sub.loc[pd.to_numeric(df_sub.MRK, errors='coerce').sort_values(ascending=False).index]
  return(df_sub)
  
#Creating Subject Analysis Data Frame
df_sub = pd.DataFrame()
for i in scode:
  df_sub = df_sub.append(analy(scode[i])) # Creating Dataframe of all the subjects using Function analy

df_sub_A=df_sub[pd.to_numeric(df_sub['MRK'], errors='coerce').notnull()]

# Converting Marks to Numbers
df_sub_A=df_sub_A[['R.No.','NAME', 'SUB', 'MRK','GRD']].apply(pd.to_numeric,errors='coerce').fillna(df_sub_A)
df_sub_A.set_index("R.No.",inplace=True)

#st.dataframe(df_sub)
subs = df_sub_A['SUB'].unique().tolist()
subs.sort()
show_subs = st.selectbox('Choose Subjects to Display',subs)
col1,col2 = st.columns(2)
with col1:
  st.dataframe(df_sub_A.loc[(df_sub_A['SUB'] == show_subs)]) # display DataFrame of Selected Subject
grade_count = df_sub_A.astype(str).groupby(['SUB','GRD']).size().reset_index(name='Count')
#grade_count.set_index(['Sub', 'GRD'],inplace=True)

with col2:
  st.dataframe(grade_count.loc[(grade_count['SUB'] == show_subs)]) # display DataFrame of Selected Subject

# <---------------  Creating Analysis DataFrames Subjectwise   ----------------------->

df_count = df_sub_A.groupby('SUB').count()[['NAME']]
df_count.columns = ['Appeared']

df_pass = df_sub_A[\
     (df_sub_A['GRD'] =='A1') | (df_sub_A['GRD'] =='A2') |\
     (df_sub_A['GRD'] =='B1') | (df_sub_A['GRD'] =='B2') |\
     (df_sub_A['GRD'] =='C1') | (df_sub_A['GRD'] =='C2') |\
     (df_sub_A['GRD'] =='D1') | (df_sub_A['GRD'] =='D2')\
     ].groupby('SUB').count()[['GRD']]
df_pass.columns = ['Pass']

df_fail = df_sub_A[\
     (df_sub_A['GRD'] !='A1') & (df_sub_A['GRD'] !='A2')&\
     (df_sub_A['GRD'] !='B1') & (df_sub_A['GRD'] !='B2')&\
     (df_sub_A['GRD'] !='C1') & (df_sub_A['GRD'] !='C2')&\
     (df_sub_A['GRD'] !='D1') & (df_sub_A['GRD'] !='D2')\
     ].groupby('SUB').count()[['GRD']]
df_fail.columns = ['Fail']

df_100 = df_sub_A[(df_sub_A['MRK']==100)].groupby('SUB').count()[['MRK']]
df_100.columns = ['100']

df_95 = df_sub_A[(df_sub_A['MRK']>95)].groupby('SUB').count()[['MRK']]
df_95.columns = ['95 & Above']

df_90 = df_sub_A[(df_sub_A['MRK']>90)].groupby('SUB').count()[['MRK']]
df_90.columns = ['90 & Above']

df_85 = df_sub_A[(df_sub_A['MRK']>85)].groupby('SUB').count()[['MRK']]
df_85.columns = ['85 & Above']

df_80 = df_sub_A[(df_sub_A['MRK']>80)].groupby('SUB').count()[['MRK']]
df_80.columns = ['80 & Above']

df_75 = df_sub_A[(df_sub_A['MRK']>75)].groupby('SUB').count()[['MRK']]
df_75.columns = ['75 & Above']

df_70 = df_sub_A[(df_sub_A['MRK']>70)].groupby('SUB').count()[['MRK']]
df_70.columns = ['70 & Above']

df_65 = df_sub_A[(df_sub_A['MRK']>65)].groupby('SUB').count()[['MRK']]
df_65.columns = ['65 & Above']

df_60 = df_sub_A[(df_sub_A['MRK']>60)].groupby('SUB').count()[['MRK']]
df_60.columns = ['60 & Above']

df_55 = df_sub_A[(df_sub_A['MRK']>55)].groupby('SUB').count()[['MRK']]
df_55.columns = ['55 & Above']

df_50 = df_sub_A[(df_sub_A['MRK']>50)].groupby('SUB').count()[['MRK']]
df_50.columns = ['50 & Above']

df_45 = df_sub_A[(df_sub_A['MRK']>45)].groupby('SUB').count()[['MRK']]
df_45.columns = ['45 & Above']

df_40 = df_sub_A[(df_sub_A['MRK']>40)].groupby('SUB').count()[['MRK']]
df_40.columns = ['40 & Above']

df_A1 = df_sub_A[(df_sub_A['GRD']=='A1')].groupby('SUB').count()[['GRD']]
df_A1.columns = ['A1']

df_A2 = df_sub_A[(df_sub_A['GRD']=='A2')].groupby('SUB').count()[['GRD']]
df_A2.columns = ['A2']

df_B1 = df_sub_A[(df_sub_A['GRD']=='B1')].groupby('SUB').count()[['GRD']]
df_B1.columns = ['B1']

df_B2 = df_sub_A[(df_sub_A['GRD']=='B2')].groupby('SUB').count()[['GRD']]
df_B2.columns = ['B2']

df_C1 = df_sub_A[(df_sub_A['GRD']=='C1')].groupby('SUB').count()[['GRD']]
df_C1.columns = ['C1']

df_C2 = df_sub_A[(df_sub_A['GRD']=='C2')].groupby('SUB').count()[['GRD']]
df_C2.columns = ['C2']

df_D1 = df_sub_A[(df_sub_A['GRD']=='D1')].groupby('SUB').count()[['GRD']]
df_D1.columns = ['D1']

df_D2 = df_sub_A[(df_sub_A['GRD']=='D2')].groupby('SUB').count()[['GRD']]
df_D2.columns = ['D2']

qpi = round(df_sub_A.groupby('SUB').mean()[['MRK']],2)
qpi.columns = ['QPI']

# Joining all Datatframes to make a single Analysis Dataframe
analysis = pd.concat([qpi,df_count,df_pass,df_fail,\
                      df_100,df_95,df_90,df_85,df_80,df_75,df_70,df_65,df_60,df_55,df_50,df_45,df_40,\
                      df_A1,df_A2,df_B1,df_B2,df_C1,df_C2,df_D1,df_D2],axis=1,sort=False)
st.dataframe(analysis.fillna(0).astype(str))

st.info("Disclaimer: Programmer is not responsible for any error in the analysis or results obtained by this program")
st.stop()
