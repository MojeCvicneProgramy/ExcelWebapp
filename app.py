import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image

# zobrazenie nadpisu a nadpisu pomocou streamlit:
st.set_page_config(page_title='Survey results')
st.header('Survey Results 2021')
st.subheader('Was the tutorial helpful?')

# !! aby sa to spustilo v prehliadači: v Terminále napísať: Streamlit run app.py
# vypíše:
# You can now view your Streamlit app in your browser.
# Local URL: http://localhost:8501
# Network URL: http://192.168.1.128:8501
# a otvorí lokálnu stránku s nadpisom 'Survey Results 2021'
# a podnadpisom 'Was the tutorial helpful?'

# zmeny sa tam budú zobrazovať automaticky bez spúčťania RUN v Pythone, stačí aktualizovať stránku

# načítanie excelu pomocou Pandas:
excel_file = 'Survey_Results.xlsx'
sheet_name = 'DATA'

df = pd.read_excel(excel_file,
                   sheet_name=sheet_name,
                   usecols="B:D",
                   header=3)

df_participants = pd.read_excel(excel_file,
                                sheet_name=sheet_name,
                                usecols="F:G",
                                header=3)

# zmazanie všetkých N/A hodnôt z tabuľky:
df_participants.dropna(inplace=True)

# filtrovanie podľa oddelenia a podľa veku pomocou Streamlit:
department = df['Department'].unique().tolist()  # zoznam oddelení
ages = df['Age'].unique().tolist()  # zoznam vekových kategórií

# streamlit slider s minimálnou a maximálnou hodnotou:
age_selection = st.slider('Age:',
                          min_value=min(ages),
                          max_value=max(ages),
                          value=(min(ages), max(ages)))

# streamlit výber oddelení:
department_selection = st.multiselect('Department:',
                                      department,
                                      default=department)

# filtrovanie dát na základe toho, čo užívateľ vybral:
# * zmení text na Italic
mask = (df['Age'].between(*age_selection)) & (df['Department'].isin(department_selection))
number_of_result = df[mask].shape[0]  # vypíše v jednom riadku celkový počet výsledkov
st.markdown(f'*Available results: {number_of_result}*')  # vypše text sformátovaný ako Markdown

# zoskupenie po filrovaní
df_grouped = df[mask].groupby(by=['Rating']).count()[['Age']]
# premenovanie stĺpca na Votes:
df_grouped = df_grouped.rename(columns={'Age': 'Votes'})
df_grouped = df_grouped.reset_index()


# vytlačenie stĺpcového grafu:
bar_chart = px.bar(df_grouped,
                   x='Rating',
                   y='Votes',
                   text='Votes',
                   color_discrete_sequence=['#F63366']*len(df_grouped),
                   template='plotly_white')
st.plotly_chart(bar_chart)

# ----zobrazenie tabuľky a obrázka pod sebou -------
st.subheader('zobrazenie tabuľky a obrázka pod sebou:')
# zobrazenie tabuľky:
st.dataframe(df)
# st.dataframe(df_participants)  # toto vypíše rovnako dlhú tabuľku ako je prvá
# lepšie je zobraziť tieto dáta ako koláčový graf nižšie

# zobrazenie obrázku zo súboru:
image = Image.open('images/logo.png')
st.image(image,
         caprion='Designed by Renata',
         # use_column_width=True)  # celá šírka stĺpca
         width=200)

# ----zobrazenie tabuľky a obrázka vedľa seba -------
st.subheader('zobrazenie tabuľky a obrázka vedľa seba:')
col1, col2 = st.beta_columns(2)
# zobrazenie tabuľky:
col2.dataframe(df)
# st.dataframe(df_participants)  # toto vypíše rovnako dlhú tabuľku ako je prvá
# lepšie je zobraziť tieto dáta ako koláčový graf nižšie

# zobrazenie obrázku zo súboru:
image = Image.open('images/logo.png')
col1.image(image,
         caprion='Designed by Renata',
         # use_column_width=True)  # celá šírka stĺpca
         width=200)
# -------------------------------------------------------

# vytvorenie koláčového grafu pomocou Plotly.express:
pie_chart = px.pie(df_participants,
                   title='Total No. of Participants',
                   values='Participants',
                   names='Departments')

# zobrazenie pie_chart pomocou Streamlit metódy plotly_chart
st.plotly_chart(pie_chart)






