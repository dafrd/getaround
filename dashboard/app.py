import streamlit as st
import pandas as pd
import numpy as np
import os
import pip
pip.main(["install", "openpyxl"])
import plotly.express as px

# This dataframe has 244 lines, but 4 distinct values for `day`
df = px.data.tips()
fig = px.pie(df, values='tip', names='day')
fig.show()

st.title('GetAround Delay Analysis')

#json_file = 'espn_2022calendar.json'
#st.balloons()
#file = open(json_file)
#data = json.load(file)

#print(os.listdir())

#df = pd.read_json(json_file)
#print(df)

delay_df = pd.read_excel('get_around_delay_analysis.xlsx', engine='openpyxl')
delay_df['ontime']=delay_df['delay_at_checkout_in_minutes'].fillna(0).apply(lambda x: 1 if x <= 0 else 0)
#st.dataframe(delay_df)

late_global = delay_df[(delay_df['delay_at_checkout_in_minutes'] > 0) & (delay_df['delay_at_checkout_in_minutes'] < 720)]
#delay_df['ontime']=delay_df['delay_at_checkout_in_minutes'].apply(lambda x: 1 if x <= 0 else 0)

fig = px.pie(delay_df, names='ontime', title='Late returns versus on time')
fig2 = px.pie(delay_df, names='checkin_type', title='Checkin types')
fig3 = px.histogram(late_global, 'delay_at_checkout_in_minutes')
fig4 = px.histogram(late_global, 'delay_at_checkout_in_minutes', color = 'checkin_type')

#fig3 = px.bar(long_df, x="nation", y="count", color="medal", title="Long-Form Input")

st.plotly_chart(fig, use_container_width=True)
st.plotly_chart(fig2, use_container_width=True)
st.plotly_chart(fig3, use_container_width=True)
st.plotly_chart(fig4, use_container_width=True)
   