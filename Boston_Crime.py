'''
Created on Jul 25, 2020 by YashTHK

Programming Assignment 5: Boston Crime Data Analysis 
A virtual space creation  dedicated for crime analysis for the city of Boston.

This program creates a virtual space for analysis of raw data of crime for the cit of Boston. The analysis can
be dome in many forms nad chosen from a dropdown menu. Each analysis has a statistical implication and charts
or visualization. 
'''
#importing the required modules
#Streamlit for virtual space creation and formatting 
import streamlit as sl
#Statistics for analysing the mode and mean of the data
import statistics as st
#Pandas for analyzing the data in dataframes 
import pandas as pd
#Matplotlib for plotting pie chart 
import matplotlib.pyplot as plt
#Pydeck for ploting map 
import pydeck as pdk
#Altair for plotting case histograms
import altair as alt

#-----------------------------------------------------------------------------
#Printing the title and basic information about the space
sl.title('Boston Crime Data Analysis (2020)')
sl.header('--------------------------------------------------------------')
sl.success('This is an interactive space to study and understand the crime statistics in Boston.')
sl.info('The Boston Crime Dataset has been identified to analyze the general criminal behavior in \nBoston, capital city of Massachusetts. In general, Massachusetts has comparatively low\ncriminal activity records compared to other states and national averages, with major types\nof crimes involving a dispute, leading to verbal abuse & assault at times. This analysis\nwill primarily focus on the crimes associated with the general public, such as, assault,\nkidnapping, sex offence, etc.')
sl.success('The space has been divided into five sections with each one focussing on either a specific analysis or visualisation.')

#------------------------------------------------------------------------------
#Reading the data
#Creating te dataframe
#Dataframe manipulation
frame = pd.read_csv('BostonCrime.csv')
frame['CODE'] = frame['OFFENSE_DESCRIPTION'].astype(str).str[0] + frame['OFFENSE_CODE'].map(str)

#Creating another dataframe for just the crimes
offense_dict = {frame['OFFENSE_CODE'].unique()[i] : frame['OFFENSE_DESCRIPTION'].unique()[i] for i in range(len(frame['OFFENSE_DESCRIPTION'].unique()))}
frame1 = pd.DataFrame(offense_dict, index =['alphaCode']).transpose()
frame1.index.name = 'numericCode'
frame1.reset_index(level=0, inplace=True)
frame1['Code'] = frame1['alphaCode'].astype(str).str[0] + frame1['numericCode'].map(str)

#Reading another file to get the names of the districts
#Making a dictionary of these district and their codes in the data

data = pd.read_csv('BostonDistricts.csv')
district = data['DISTRICT_NUMBER'].tolist()
district_name = data['DISTRICT_NAME'].tolist()   

DISTRICTS = {district[i]: district_name[i] for i in range(len(district))}

#Dictionary for Months 
MONTHS = {1:'January', 2:'February', 3:'March', 4:'April', 5:'May', 6:'June', 7:'July'}

#Using the groupby function to group the data as per their crimes
#This allows to segregate data based on the crime
d = dict(tuple(frame.groupby('CODE')))
for i, g in frame.groupby('CODE'):
    globals()['frame_' + str(i)] = g
    
#------------------------------------------------------------------------------
#Function for analysis of crime district-wise
def unsafeDistrict(dataframe):        
    unsafeDistrict_dict = {DISTRICTS[dataframe['DISTRICT'].unique()[i]] :dataframe['DISTRICT'].value_counts()[i] for i in range(len(dataframe['DISTRICT'].unique()))} 
    unsafeDistricts = pd.DataFrame(unsafeDistrict_dict, index = ['Frequency']).transpose()
    unsafeDistricts.index.name = 'District'
    unsafeDistricts.reset_index(level=0, inplace=True)
    mostUnsafeDistrict = unsafeDistricts['District'][0]
        
    sl.warning(f'The district associated with highest frequency of the concerned crime is {mostUnsafeDistrict}.')
    sl.write('Frequency of the concerned crime(District-wise): ')
    sl.write(unsafeDistricts)
    sl.write(alt.Chart(unsafeDistricts).mark_bar(size=20).encode(x = alt.X('District', sort = None), y = 'Frequency').properties(width = 600, height = 500))

#------------------------------------------------------------------------------
#Function for analysis of crime street-wise    
def unsafeStreet(dataframe):
    unsafeStreet_dict = {dataframe['STREET'].unique()[i] :dataframe['STREET'].value_counts()[i] for i in range(len(dataframe['STREET'].unique()))}
    unsafeStreets = pd.DataFrame(unsafeStreet_dict, index = ['Frequency']).transpose()
    unsafeStreets.index.name = 'Street'
    unsafeStreets.reset_index(level=0, inplace=True)
    mostUnsafeStreet = unsafeStreets['Street'][0]
  
    sl.warning(f'The street associated with highest frequency of the concerned crime is {mostUnsafeStreet}.')
    sl.write('Ten streets with highest frequency of the concerned crime: ')
    sl.write(unsafeStreets.iloc[:10])
    sl.write(alt.Chart(unsafeStreets.iloc[:10]).mark_bar(size=20).encode(x = alt.X('Street', sort = None), y = 'Frequency').properties(width = 600, height = 500))

#------------------------------------------------------------------------------
#Function for categorizing hour information in the part of the day format
def part_of_day(dataframe):
    hourList = dataframe['HOUR'].to_list()
    partList = []
    for i in hourList:
        if 5 <= i <= 11:
           partList.append('Morning')
        elif 12 <= i <= 17:
           partList.append('Afternoon')
        elif 18 <= i <= 22:
           partList.append('Evening')
        else:
           partList.append('Night')
    return partList
 
#------------------------------------------------------------------------------
#Function for analysis of crime part of the day-wise
def unsafeTiming(dataframe):
    dataframe['PART_OF_DAY'] = part_of_day(dataframe)
    unsafeTiming_dict = {dataframe['PART_OF_DAY'].unique()[i] :dataframe['PART_OF_DAY'].value_counts()[i] for i in range(len(dataframe['PART_OF_DAY'].unique()))}
    unsafeTimings = pd.DataFrame(unsafeTiming_dict, index = ['Frequency']).transpose()
    unsafeTimings.index.name = 'Timing'
    unsafeTimings.reset_index(level=0, inplace=True)
    mostUnsafeTiming = unsafeTimings['Timing'][0]
  
    sl.warning(f'The Timing associated with highest frequency of the concerned crime is {mostUnsafeTiming}.')
    sl.write('Timings with the concerned crime: ')
    sl.write(unsafeTimings)
    sl.write(alt.Chart(unsafeTimings).mark_bar(size=20).encode(x = alt.X('Timing', sort = None), y = 'Frequency').properties(width = 600, height = 500))

#------------------------------------------------------------------------------
#Function for analysis of crime day of the week-wise
def unsafeDay(dataframe):
    unsafeDay_of_Week_dict = {dataframe['DAY_OF_WEEK'].unique()[i] :dataframe['DAY_OF_WEEK'].value_counts()[i] for i in range(len(dataframe['DAY_OF_WEEK'].unique()))}
    unsafeDay_of_Weeks = pd.DataFrame(unsafeDay_of_Week_dict, index = ['Frequency']).transpose()
    unsafeDay_of_Weeks.index.name = 'Day of Week'
    unsafeDay_of_Weeks.reset_index(level=0, inplace=True)
    mostUnsafeDay_of_Week = unsafeDay_of_Weeks['Day of Week'][0]
  
    sl.warning(f'The Day of Week associated with highest frequency of the concerned crime is {mostUnsafeDay_of_Week}.')
    sl.write('Day of Weeks with the concerned crime: ')
    sl.write(unsafeDay_of_Weeks)
    sl.write(alt.Chart(unsafeDay_of_Weeks).mark_bar(size=20).encode(x = alt.X('Day of Week', sort = None), y = 'Frequency').properties(width = 600, height = 500))


#------------------------------------------------------------------------------                          
#Function for analysis of crime month-wise
def unsafeMonth(dataframe):
    unsafeMonths1 = pd.DataFrame(dataframe['MONTH'].value_counts())
    frequencyList = unsafeMonths1['MONTH'].to_list()
    monthNumList = unsafeMonths1.index.values.tolist()
    unsafeMonth_dict = {MONTHS[monthNumList[i]]:frequencyList[i] for i in range(len(frequencyList))} 
    unsafeMonths = pd.DataFrame(unsafeMonth_dict, index = ['Frequency']).transpose()
    unsafeMonths.index.name = 'Month'
    unsafeMonths.reset_index(level=0, inplace=True)
    mostUnsafeMonth = unsafeMonths['Month'][0]
  
    sl.warning(f'The Month associated with highest frequency of the concerned crime is {mostUnsafeMonth}.')
    sl.write('Months with the concerned crime: ')
    sl.write(unsafeMonths)
    sl.write(alt.Chart(unsafeMonths).mark_bar(size=20).encode(x = alt.X('Month', sort = None), y = 'Frequency').properties(width = 600, height = 500))
    

#------------------------------------------------------------------------------
#Function for analysis of crimes involving shooting 
def shooting(dataframe):
    shootingdf = dataframe[dataframe['SHOOTING']>0]
    shootingdf = shootingdf.drop(['NUMBER', 'INCIDENT_NUMBER', 'REPORTING_AREA', 'Location'], axis = 1)
    shootingdf['PART_OF_DAY'] = part_of_day(shootingdf)
    shootingdf.reset_index(level=0, inplace=True)
    sl.write(shootingdf.drop(['SHOOTING','OFFENSE_CODE', 'OCCURRED_ON_DATE','Lat', 'Long'], axis = 1))    
    
    shootingOffense_dict = {shootingdf['OFFENSE_DESCRIPTION'].unique()[i] :shootingdf['OFFENSE_DESCRIPTION'].value_counts()[i] for i in range(len(shootingdf['OFFENSE_DESCRIPTION'].unique()))}
    shootingOffense = pd.DataFrame(shootingOffense_dict, index = ['Frequency']).transpose()
    shootingOffense.index.name = 'Offense'
    shootingOffense.reset_index(level=0, inplace=True)
    
    shootingPart_dict = {shootingdf['PART_OF_DAY'].unique()[i] :shootingdf['PART_OF_DAY'].value_counts()[i] for i in range(len(shootingdf['PART_OF_DAY'].unique()))}
    shootingPart = pd.DataFrame(shootingPart_dict, index = ['Frequency']).transpose()
    shootingPart.index.name = 'Part of Day'
    shootingPart.reset_index(level=0, inplace=True)
    
    shootingDistrict = DISTRICTS[st.mode(shootingdf['DISTRICT'])]
    shootingMonth = MONTHS[st.mode(shootingdf['MONTH'])]
    shootingDay = st.mode(shootingdf['DAY_OF_WEEK'])
    
    sl.warning(f'The district with most number of shooting recorded is {shootingDistrict}.')
    sl.warning(f'The month with most number of shooting recorded is {shootingMonth}.')
    sl.warning(f'The day with most number of shooting recorded is {shootingDay}.')
    sl.write('The chart below shows the shooting related crime and their frequency.')
    sl.write(alt.Chart(shootingOffense).mark_bar(size=20).encode(x = alt.X('Offense', sort = None), y = 'Frequency').properties(width = 600, height = 500))
    sl.write('The chart below shows part of day associated with shooting related crimes and their frequency.')
    sl.write(alt.Chart(shootingPart).mark_bar(size=20).encode(x = alt.X('Part of Day', sort = None), y = 'Frequency').properties(width = 600, height = 500))
    
    
#------------------------------------------------------------------------------
#Function for analysis of common crimes such as assault, threats, verbal-dispute, etc.
def crimeProfile_common(dataframe):
    countlist = []
    offenselist = []
    monthlist = []
    districtlist = []
    assaultdf = dataframe[dataframe['OFFENSE_DESCRIPTION'].str.contains('ASSAULT')]
    acount = assaultdf.NUMBER.count()
    countlist.append(acount)
    offenselist.append('ASSAULT')
    monthlist.append(MONTHS[st.mode(assaultdf['MONTH'])])
    districtlist.append(DISTRICTS[st.mode(assaultdf['DISTRICT'])])
    harassmentdf = dataframe[dataframe['OFFENSE_DESCRIPTION'].str.contains('HARASSMENT')]
    hcount = harassmentdf.NUMBER.count()
    countlist.append(hcount)
    offenselist.append('HARASSMENT')
    monthlist.append(MONTHS[st.mode(harassmentdf['MONTH'])])
    districtlist.append(DISTRICTS[st.mode(harassmentdf['DISTRICT'])])
    threatsdf = dataframe[dataframe['OFFENSE_DESCRIPTION'].str.contains('THREATS')]
    tcount = threatsdf.NUMBER.count()
    countlist.append(tcount)
    offenselist.append('THREATS')
    monthlist.append(MONTHS[st.mode(threatsdf['MONTH'])])
    districtlist.append(DISTRICTS[st.mode(threatsdf['DISTRICT'])])
    verbal_disputedf = dataframe[dataframe['OFFENSE_DESCRIPTION'].str.contains('VERBAL DISPUTE')]
    vcount = verbal_disputedf.NUMBER.count()
    countlist.append(vcount)
    offenselist.append('VERBAL DISPUTE')
    monthlist.append(MONTHS[st.mode(verbal_disputedf['MONTH'])])
    districtlist.append(DISTRICTS[st.mode(verbal_disputedf['DISTRICT'])])
    kidnappingdf = dataframe[dataframe['OFFENSE_DESCRIPTION'].str.contains('KIDNAPPING')]
    kcount = kidnappingdf.NUMBER.count()
    countlist.append(kcount)
    offenselist.append('KIDNAPPING')
    monthlist.append(MONTHS[st.mode(kidnappingdf['MONTH'])])
    districtlist.append(DISTRICTS[st.mode(kidnappingdf['DISTRICT'])])
    theftdf = dataframe[dataframe['OFFENSE_DESCRIPTION'].str.contains('THEFT')]
    tfcount = theftdf.NUMBER.count()
    countlist.append(tfcount)
    offenselist.append('THEFT')
    monthlist.append(MONTHS[st.mode(theftdf['MONTH'])])
    districtlist.append(DISTRICTS[st.mode(theftdf['DISTRICT'])])
    sexdf = dataframe[dataframe['OFFENSE_DESCRIPTION'].str.contains('SEX')]
    scount = sexdf.NUMBER.count()
    countlist.append(scount)
    offenselist.append('SEX OFFENSE')
    monthlist.append(MONTHS[st.mode(sexdf['MONTH'])])
    districtlist.append(DISTRICTS[st.mode(sexdf['DISTRICT'])])
    common_offense = pd.DataFrame(list(zip(offenselist,countlist)),columns = ['OFFENSE', 'COUNT'])
    common_offense['MONTH'] = monthlist
    common_offense['DISTRICT'] = districtlist
                                  
    colors = ['b','g','r','c','m','y','w']
    explode = (0.1,0.1,0.1,0.1,0.1,0.1,0.1)
    patches = plt.pie(countlist, explode=explode, labels= offenselist, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
    plt.legend(patches, offenselist, loc="best")
    plt.title(f'Pie Distribution of Frequency of Common Crimes\n')
    plt.axis('equal')
    plt.tight_layout()
    sl.pyplot()
    sl.write(common_offense)
    

#------------------------------------------------------------------------------
#Function for geographical analysis of reported crimes and map plotting
def crimeProfile_Geographic(dataframe):
    Latitude = dataframe['Lat'].to_list()
    Longitude = dataframe['Long'].to_list()
    crimeMap_dict = {Latitude[i]: Longitude[i] for i in range(len(Latitude))}
    crimeMap = pd.DataFrame(crimeMap_dict, index = ['lon']).transpose()
    crimeMap.index.name = 'lat'
    crimeMap.reset_index(level=0, inplace=True)
    sl.write(crimeMap)
    #sl.map(crimeMap)
    sl.pydeck_chart(pdk.Deck(
       map_style="mapbox://styles/mapbox/bright-v8",
        initial_view_state=pdk.ViewState(
            latitude=42.32,
            longitude=-71.06,
            zoom=11.15,
            pitch=35,
        ), 
        layers=[
            pdk.Layer(
                'ScatterplotLayer',
                data=crimeMap,
                get_position="[lon, lat]",
                get_radius=50,
                get_fill_color='[245, 66, 75]',
                pickable=True,
                opacity=0.5,
                stroked=False,
                filled=True,
                wireframe=True,
                ),
            ],
        ))
    

#------------------------------------------------------------------------------   
#Creation of the list of possible analysis and then putting it in a drop down menu
crimeAnalysis_List  = ['Space 1: Crime Analysis - Area-wise', 'Space 2: Crime Analysis - Time-wise', 'Space 3: Crime Analysis - Crimes involving shooting', 'Space 4: Common Crimes Visualisation', 'Space 5: Geograpic Crime Profile Simulation']
crimeAnalysis_List.insert(0, 'Welcome')
analysisSelect = sl.selectbox('Select the specific analysis',([x for x in crimeAnalysis_List]))

#Creation of the list for all possible crimes and a general case conataining all crime
crimeCode_List = [x for x in frame1['Code']]
crimeCode_List.insert(0, 'General')

#Creation of segregated data as multiple dataframes 
grouped = frame.groupby(frame.CODE)
for i in crimeCode_List[1:115]:
    i = grouped.get_group(i)

#Driver of the whole program
#Each and every analysis has a diiferent name, task, description of the task and one or more dedicated functions to perform those tasks
if analysisSelect == 'Space 1: Crime Analysis - Area-wise':
    sl.write('The space deals with these specific crimes & in order to customize please refer to the table below to look for the suitable code and accordingly select the code from the dropdown menu.')
    sl.dataframe(frame1, width=625, height=400)
    crimeSelect = sl.selectbox('Select the crime to be analyzed',([x for x in crimeCode_List]))
    sl.header('Space 1: Crime Area Analysis')
    sl.info('This space has been divided into two subspaces, the prior one deals with district-wise\nanalysis while the later one focus on streets. Each analysis can be changed for specific\ncrime as per the user needs.')
    if crimeSelect == 'General':
        unsafeDistrict(frame)
        unsafeStreet(frame)
    else:
        for i in crimeCode_List[1:115]:
            if crimeSelect == i:
                i = grouped.get_group(i)
                unsafeDistrict(i)
                unsafeStreet(i)
elif analysisSelect == 'Space 2: Crime Analysis - Time-wise':
    sl.write('The space deals with these specific crimes & in order to customize please refer to the table below to look for the suitable code and accordingly select the code from the dropdown menu.')
    sl.dataframe(frame1, width=625, height=400)
    crimeSelect = sl.selectbox('Select the crime to be analyzed',([x for x in crimeCode_List]))
    sl.header('Space 2: Crime Time Analysis')
    sl.info('This space has been divided into three subspaces, the prior one deals with time & district\nanalysis. The second one analyzes crime frequency depoendent on day of the week, the last\none follow the monthly statistics.  Each analysis can be changed for specific crime.')
    if crimeSelect == 'General':
        unsafeTiming(frame)
        unsafeDay(frame)
        unsafeMonth(frame)
    else:
        for i in crimeCode_List[1:115]:
            if crimeSelect == i:
                i = grouped.get_group(i)
                unsafeTiming(i)
                unsafeDay(i)
                unsafeMonth(i)
elif analysisSelect == 'Space 3: Crime Analysis - Crimes involving shooting':
    sl.header('Space 3: Crimes involving Shooting')
    sl.info('This space deals with the crimes that involved shooting. Here the dataset below captures the necessary details of all the shooting involved crimes, followed by brief statistical statements regarding the same and specific frequency based visalusations.')
    shooting(frame)
elif analysisSelect == 'Space 4: Common Crimes Visualisation':
    sl.header('Space 4: Common Crimes Visualisation')
    sl.info('This space shows a pie distribution of the common classes of crimes with their respective percentages. The table following the pie chart reads the common classes of crime with their reported frequency. The table shows month and district of the highest number of recorded cases for each crime class.')
    crimeProfile_common(frame)
elif analysisSelect == 'Space 5: Geograpic Crime Profile Simulation':
    sl.write('The space deals with these specific crimes & in order to customize please refer to the table below to look for the suitable code and accordingly select the code from the dropdown menu.')
    sl.dataframe(frame1, width=625, height=400)
    crimeSelect = sl.selectbox('Select the crime to be analyzed',([x for x in crimeCode_List]))
    sl.header('Space 5: Geograpic Crime Profile Simulation')
    sl.info('This space puts the geo-coordinates of the crime in perception. (Note: if the crime has been reported more than once at a specific place then only first occurance has been marked. Overlaps, if any, have been not reorded on the map.) ')
    if crimeSelect == 'General':
        crimeProfile_Geographic(frame)
    else:
        for i in crimeCode_List[1:115]:
            if crimeSelect == i:
                i = grouped.get_group(i)
                crimeProfile_Geographic(i)
else: 
    sl.header('\n\nBoston')
    sl.success('Boston (US: /ˈbɔːstən/, UK: /ˈbɒstən/) is the capital and most populous city of the Commonwealth of Massachusetts in the United States, and the 21st most populous city in the United States. The city proper covers 49 square miles (127 km2) with an estimated population of 692,600 in 2019, also making it the most populous city in New England, and is the seat of Suffolk County (although the county government was disbanded on July 1, 1999). The city is the economic and cultural anchor of a substantially larger metropolitan area known as Greater Boston, a metropolitan statistical area (MSA) home to a census-estimated 4.8 million people in 2016 and ranking as the tenth-largest such area in the country. As a combined statistical area (CSA), this wider commuting region is home to some 8.2 million people, making it the sixth most populous in the United States.')
    sl.success('Boston is one of the oldest municipalities in the United States, founded on the Shawmut Peninsula in 1630 by Puritan settlers from the English town of the same name. It was the scene of several key events of the American Revolution, such as the Boston Massacre, the Boston Tea Party, the Battle of Bunker Hill, and the Siege of Boston. Upon gaining U.S. independence from Great Britain, it continued to be an important port and manufacturing hub as well as a center for education and culture. The city has expanded beyond the original peninsula through land reclamation and municipal annexation. Its rich history attracts many tourists, with Faneuil Hall alone drawing more than 20 million visitors per year. Boston\'s many firsts include the United States\' first public park (Boston Common, 1634), first public or state school (Boston Latin School, 1635) and first subway system (Tremont Street subway, 1897).')
    sl.success('Today, Boston is a thriving center of scientific research. The Boston area\'s many colleges and universities make it a world leader in higher education, including law, medicine, engineering, and business, and the city is considered to be a global pioneer in innovation and entrepreneurship, with nearly 5,000 startups. Boston\'s economic base also includes finance, professional and business services, biotechnology, information technology, and government activities. Households in the city claim the highest average rate of philanthropy in the United States; businesses and institutions rank among the top in the country for environmental sustainability and investment. The city has one of the highest costs of living in the United States as it has undergone gentrification, though it remains high on world livability rankings')
    sl.image('FD,Downtown_Boston.jpg', caption = 'Financial District Neighbourhood, Downtown', use_column_width=True)
    sl.image('MSH_Boston.jpg', caption = 'Massachusetts State House', use_column_width=True)
    sl.image('BB&CR_Boston.jpg', caption = 'Back Bay & the Charles River', use_column_width=True)
    sl.header('What is crime?')
    sl.error('A crime is an offence that merits community condemnation and punishment,\nusually by way of fine or imprisonment. This is different from a civil wrong (a tort),\nwhich is an action against an individual that requires compensation or restitution.\n\nCriminal offences are normally prosecuted by the State or the Commonwealth,\nwhereas it is usually up to an individual to take a civil action to court. It is also\npossible for an individual to begin criminal proceedings, but this is very rare')
    sl.error('Some matters, such as assault, can be both crimes and civil wrongs at the same\ntime. The police can prosecute for assault and the victim can take civil action to\nrecover money (or some other kind of compensation) for any injury suffered.\n\nIt is not always easy to tell when something is a crime. A person who takes money\nwithout permission commits a criminal offence, whereas a person who fails to\npay back money commits a civil wrong (not a crime). Although a civil action can be\ncommenced to recover the money, the borrower can only be prosecuted for a\ncriminal offence if fraud is involved.')
    sl.error('Whether or not the police decide to charge a wrongdoer with a criminal offence is\nentirely their decision. A victim of crime cannot force the police to prosecute an\noffender but it is possible, although not common, to make a private prosecution.\nIt is advisable to get legal advice if you are considering this\n\nThere are a range of sources of law which establish the existence of crimes.')
    sl.text('Source: New Mexico State Law Board')
    sl.image('crime.JPG',use_column_width=True)

#------------------------------------------------------------------------------

#This allows the user to rate the virtual space and enter a comment about the space
#Based on the rating the it displays a suitable message to the user 
sl.text('')
sl.text('')
sl.text('')
sl.text('')
sl.text('')
sl.text('')
sl.text('')
sl.text('')
sl.text('')
sl.text('')
sl.text('')
sl.text('')
sl.warning('Thanks a lot for visiting this space. Please leave a rating and comments, for us to make your future experiences more pleasurable.')
rating = sl.slider('Rating', 0.0, 5.0, 0.0, 0.5)
comment = sl.text_area('You valuable comments: ')
if rating > 0:
    sl.write(rating)
    if rating <= 2:
        sl.write('We are really sorry to hear that, please let us know how we can improve!')
    elif 2 < rating < 4:
        sl.write('Cheers')
    else:
        sl.write('We are so happy to hear that, please let us know what you liked the most. ')
if len(comment) != 0:
    sl.write('Thanks a lot for your valuable comment.')

#------------------------------------------------------------------------------

#The general disclaimer and thanking note for space visit
sl.text('')
sl.text('')
sl.text('')
sl.text('')
sl.text('')
sl.text('')
sl.text('')
sl.text('')
sl.markdown("<h6 style='text-align: right; color: black;'>©Thk Analytics</h6>",  unsafe_allow_html=True)
sl.text('')
sl.text('')
sl.text('')
sl.text('DISCLAIMER: PLEASE BE AWARE THAT ANY INFORMATION YOU MAY FIND IN HERE MAY BE INACCURATE,\nMISLEADING, DANGEROUS, ADDICTIVE, UNETHICAL OR ILLEGAL.')
sl.text('Some information here may create an unreasonable risk for readers who choose to use the\ninformation in their own activities or to promote information for use by third parties.')
sl.text('None of the authors, contributors, administrators, vandals, or anyone else connected with\nthe development of this space, in any way whatsoever, can be held responsible for your\nuse of the information contained in here.')
sl.text('Please take all steps necessary to ascertain that information you receive from concerned\nspace is correct and has been verified. Check your refernces and quote the presented\ninformation at your own risk. ')
sl.write('Thanks a lot for visiting this space and it will be very appreciated if you could refer this space to other people. Developers here have always taken pride in pleasing your senses and sparking the interest in the concerned topic.')

#------------------------------------------------------------------------------
