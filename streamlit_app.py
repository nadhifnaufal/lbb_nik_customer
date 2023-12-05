import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(layout= 'wide')

# ----- Read Data -----
customer_merge = pd.read_pickle('data/customer_merge.pkl')
coord = pd.read_csv('data/coordinate.csv')


## ----- Row 1 -----
# ----- Summary -----
st.write('# Customer Demography Dashboard')
st.write('''A "Customer Demography Dashboard" is a visual representation of various demographic aspects of a company's customer base. 
         It provides a comprehensive overview of the characteristics of customers, 
         helping businesses gain insights into the composition of their clientele. 
         This type of dashboard is valuable for marketing, sales, and product development teams, among others, 
         as it aids in making data-driven decisions and tailoring strategies to better meet customer needs.''')

## ----- Row 1.2 -----

# data: map
prov_gender = pd.crosstab(index=customer_merge['province'],
                          columns=customer_merge['gender'],
                          colnames=[None]
                          )

prov_gender['Total'] = prov_gender['Female'] + prov_gender['Male']

df_map = prov_gender.merge(right=coord, on='province')

# plot: map
plot_map = px.scatter_mapbox(data_frame=df_map, lat='latitude', lon='longitude',
                             mapbox_style='carto-positron', zoom=3,
                             size='Total',
                             hover_name='province',
                             hover_data={'Male': True,
                                         'Female': True,
                                         'latitude': False,
                                         'longitude': False}
                             )

st.write('### Customer Count across Indonesia')
st.plotly_chart(plot_map, use_container_width=True)

## ----- Row 2 -----
# ----- Visualization -----
col1, col2 = st.columns(2)

# data: Customer Profession
df_profesi = pd.crosstab(index=customer_merge['Profession'],
                      columns='Jumlah Customer',
                      colnames=[None])
df_profesi = df_profesi.reset_index()

# plot: Customer Profession
plot_prof_gender = px.bar(data_frame= df_profesi.sort_values(by='Jumlah Customer', ascending=False), 
                          x= 'Profession', y= 'Jumlah Customer')

col1.write('### Customer Count per Profession')
col1.plotly_chart(plot_prof_gender, use_container_width=True)

### BarPlot
# data: barplot
cust_age = customer_merge[customer_merge['age'].between(left=21, right=60)]

profesi_gender = pd.crosstab(index=cust_age['Profession'],
                            columns=cust_age['gender'],
                            colnames=[None])

profesi_gender_melt = profesi_gender.melt(ignore_index=False, var_name='gender', value_name='num_people')

profesi_gender_melt = profesi_gender_melt.reset_index()

# plot: barplot
plot_prof_gender = px.bar(data_frame= profesi_gender_melt.sort_values(by='num_people'), 
                          x= 'num_people', y= 'Profession',
                          color='gender', barmode='group',
                          labels={'gender':'Gender',
                                  'num_people':'Customer Count'})

col2.write('### Gender per Profession')
col2.plotly_chart(plot_prof_gender, use_container_width=True)

## ----- Row 3 -----
st.divider()
col3, col4 = st.columns(2)

### Input Select Department
input_select = col3.selectbox(label= 'Select Profession', 
                              options= customer_merge['Profession'].unique().sort_values()
                              )

col4.write('')

# ### Input Multi Select Generation Group
# input_multiselect = col4.selectbox(label= 'Select Age Category', options= customer_merge['Age_Category'].unique().sort_values())

# input_multiselect = col4.select_slider(label= 'Select a color of the rainbow', 
#                                      options= customer_merge['Age_Category'].unique().sort_values(),
#                                      value=('Teen', 'Elderly')
#                                      )

# ### Input Slider Age
# input_slider = col4.slider(label= 'Select Age Range', 
#                                    min_value= employ_merge['age'].min(), 
#                                    max_value=employ_merge['age'].max(), 
#                                    value=[20,50]
#                                    )

# min_slider = input_slider[0]
# max_slider = input_slider[1]

## ----- Row 4 -----
col5, col6 = st.columns(2)

# data: Customer Profession Artis
cust_profesi =  customer_merge[customer_merge['Profession']==input_select]

profesi_gen = pd.crosstab(index= cust_profesi['generation'], 
                          columns= cust_profesi['gender'],
                          colnames=[None])

profesi_gen_metl = profesi_gen.melt(ignore_index=False, var_name='gender', value_name='num_people')


profesi_gen_metl = profesi_gen_metl.reset_index()

# plot: Customer Profession Artis
plot_bar_gen = px.bar(data_frame=profesi_gen_metl.sort_values(by='num_people', ascending=False), 
                      x= 'generation', y= 'num_people',
                      color='gender', barmode='group',
                      labels={'generation':'Generation',
                              'num_people':'Customer Count'})

col5.write(f'### Customer with {input_select} Profession per Generation Group')
col5.plotly_chart(plot_bar_gen, use_container_width=True)


### Multivariate
# data: multivariate
profesi_age = pd.crosstab(index=customer_merge['Profession'],
                          columns=customer_merge['Age_Category'],
                          colnames=[None])

profesi_age_melt = profesi_age.melt(ignore_index=False , var_name='age_category', value_name='count')
profesi_age_melt = profesi_age_melt.reset_index()

# plot: multivariate
plot_prof_gender = px.bar(data_frame=profesi_age_melt.sort_values(by='count', ascending=False), 
                          x='Profession', y='count', 
                          color='age_category', barmode='group',
                          labels = {'count' : 'Customer Count', 
                                    'Profession' : 'Profession', 
                                    'age_category': 'Age Category'}
                          )

col6.write(f'### Customer Profession per Generation Group')
col6.plotly_chart(plot_prof_gender, use_container_width=True)

