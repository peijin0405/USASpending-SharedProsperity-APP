#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import streamlit as st
import numpy as np
import pandas as pd
import json
from pandas.core.frame import DataFrame

import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import country_converter as coco



st.set_page_config(layout="wide")

row0_spacer1, row0_1, row0_spacer2, row0_2, row0_spacer3 = st.columns((.1, 2.3, .1, 1.3, .1))
with row0_1:
    st.title('US Grants - Shared Prosperity Analyzer')
with row0_2:
    st.text("")
    st.subheader('Streamlit App by [Peijin Li](https://www.linkedin.com/in/peijin-li-a594a1149/)')
row3_spacer1, row3_1, row3_spacer2 = st.columns((.1, 3.2, .1))
with row3_1:
    st.markdown("This app presents the worldwide distribution of U.S. Grants spending from FY 2014 to FY 2022. Through this app, you could learn the distribution of U.S. Grants by continent and by country. Further, with the Shared Prosperity Index proposed by the World Bank, the app provides a chance to explore the relationship between U.S. Grants and Inclusive Growth.")
    st.markdown("You can find the source code in the [Peijin GitHub Repository](https://github.com/peijin0405/USASpending-SharedProsperity-APP)")
    
# About
expander_bar = st.expander("About")
expander_bar.markdown("""
* **Python libraries:** Pandas, Streamlit, Numpy, Plotly, BeautifulSoup, requests, json
* **Data source:** [USAspending API](https://www.usaspending.gov).USAspending is the official open data source of federal spending information. It tracks how federal maony is spent in communities accross America and beyond.[Shared Prosperity Data](https://www.worldbank.org/en/topic/poverty/brief/global-database-of-shared-prosperity).Shared prosperity focuses on the poorest 40 percent of the population in a country (the bottom 40) and is defined as the annualized growth rate of their mean household per capita consumption or income. It is an important indicator of inclusion and well-being that correlate with reductions in poverty and inequality (World Bank, 2022). 
* **Data collection:** For more information on how shared prosperity data is collected, please refer to [Global Database of Shared Prosperity](https://openknowledge.worldbank.org/bitstream/handle/10986/34496/9781464816024.pdf#page=106).
""") 
    
# Make selectbox a sidebar
st.markdown("") 
st.markdown("Which year of U.S. grants data you want to explore?")  
Select_year = st.selectbox('Select Year',['2022','2021','2020','2019','2018','2017','2016','2015','2014'])
                                      

### Data Import ###
# get grant data    
def get_grants_dataset(Select_year):
    if Select_year == "2022":
        grants_data = pd.read_csv("data/2022grants_withoutUSA.csv")
    elif Select_year == "2021":
        grants_data = pd.read_csv("data/2021grants_withoutUSA.csv")
    elif Select_year == "2020":
        grants_data = pd.read_csv("data/2020grants_withoutUSA.csv")
    elif Select_year == "2019":
        grants_data = pd.read_csv("data/2019grants_withoutUSA.csv")
    elif Select_year == "2018":
        grants_data = pd.read_csv("data/2018grants_withoutUSA.csv")
    elif Select_year == "2017":
        grants_data = pd.read_csv("data/2017grants_withoutUSA.csv")
    elif Select_year == "2016":
        grants_data = pd.read_csv("data/2016grants_withoutUSA.csv")
    elif Select_year == "2015":
        grants_data = pd.read_csv("data/2015grants_withoutUSA.csv")
    else:
        grants_data  = pd.read_csv("data/2014grants_withoutUSA.csv")
    return grants_data

# read in geojson
all_country = json.load(open("data/all_country.geojson","r"))
# load shared prosperity data
SSI = pd.read_csv("data/SSI.csv")
# load grants increase rate data
merge_grants2014_2019 = pd.read_csv("data/grants_rate_2014_2019.csv")
# load sp-grantrate data
grants2_inc_ssi_1 = pd.read_csv("data/grants2_inc_ssi.csv")
# load all year grants
all_year = pd.read_csv("data/all_year.csv")


### Recall ###
grants_data = get_grants_dataset(Select_year)

### present the raw data ###
row3_spacer1, row3_1, row3_spacer2 = st.columns((.2, 7.1, .2))
with row3_1:
    st.markdown("")
    see_data = st.expander('You can click here to see the raw data first 👉')
    with see_data:
        st.dataframe(data=grants_data.iloc[: , 1:].reset_index(drop=True))
st.text('')

### Grants Geo Map ###
row4_spacer1, row4_1, row4_spacer2 = st.columns((.2, 7.1, .2))
with row4_1:
    st.subheader('Distribution of U.S. Grants Spending in FY ' + Select_year)
row5_spacer1, row5_1, row5_spacer2, row5_2, row5_spacer3  = st.columns((.2, 2.3, .4, 4.4, .2))
with row5_1:
    st.markdown(""" 
    * **Grants Amount:** Refers to the sum of money given by a USA government to other countries to facilitate a goal or incentivize performance.""")   
    st.markdown("")
    st.markdown("""
* Each year, more than two hundred countries receive grants from the United States; however, grants disproportionately go to a few.
* Africa has long been the largest grants recipient continent.
* In recent years, there has been a significant increase in funding to East Asia (mainly Ukraine).
""") 
    
# prepare for plotting     

with row5_2:
    @st.cache(allow_output_mutation =True)
    def plot1(grants_data):
        country_id_map = {}
        for feature in all_country["features"]:
            feature["properties"]['name']= coco.convert(names=feature["properties"]['name'], to='name_short')
            feature["id"] = feature["properties"]['name']
            country_id_map[feature["properties"]['name']] = feature["id"]    
        list = []##list the countires in the gepjson file 
        list.extend(country_id_map)
        list_0 = {"geo_list_0": list}
        geo_list = DataFrame(list_0)    
        ## merge dfs
        merge7 = geo_list.merge(grants_data,how="left",left_on="geo_list_0",right_on="Country Name")
        merge8 = merge7.filter(["geo_list_0","Amount","UN Region","Total Population","Amount ","Population","Population ","Population Date"])
        merge9 = merge8.rename(columns={"geo_list_0":"Country Name"})
        merge9["id"] = merge9["Country Name"].apply(lambda x:country_id_map[x])
        # log the numbers
        merge9["log_Grants Amount"] = np.log10(merge9["Amount"])
        #st.dataframe(data=merge9)
        fig1 = px.choropleth_mapbox(merge9,
                            locations = "id",
                            geojson = all_country,
                            color="log_Grants Amount",
                           hover_name = "Country Name",
                           #hover_data = merge9.columns,
                            hover_data = {"id": False,
                                        "log_Grants Amount":False,
                                        "Amount ": True,
                                       "Population ": True,
                                        "Population Date": True},
                             mapbox_style = "carto-positron",
                            color_continuous_scale="magma",
                             zoom= 0.57,opacity = 0.3,
                            center = {"lat": 34.55,"lon":18.04},
                            title = "Distribution of USA Grants Spending around the world in FY" + Select_year 
                         ,labels={'log_Grants Amount': 'Grants Amount'}
                            )
        fig1.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
        return fig1
    fig1 = plot1(grants_data)
    st.plotly_chart(fig1)


### Grants Sunburst Map ###
row6_spacer1, row6_1, row6_spacer2 = st.columns((.2, 7.1, .2))
with row6_1:
    st.subheader('U.S. Grants Spending Proportion in FY ' + Select_year)
row7_spacer1, row7_1, row7_spacer2, row7_2, row7_spacer3  = st.columns((.2, 2.3, .4, 4.4, .2))
with row7_1:
    st.markdown("""
* The long-standing distribution pattern is that the African continent has the largest share, followed by Europe, then Asia and the Americas, with Australia having the smallest share.
* After 2020, the U.S. grants gradually tilted toward Europe. 
* European grants are mainly concentrated in two countries-Switzerland and Ukraine. In 2022, the sum of the two countries accounts for about 90% of the entire European grants.
""")    
    st.markdown("")   
    st.markdown(""" 
    * **Note:**  By clicking on the continent, you can explore the distribution of Grants of different countries within a continent.""")
    
with row7_2:
    fig2 = px.sunburst(grants_data,path=["UN Region","Country Name"],values = "Amount",hover_name = "UN Region",color = "log_Population"
                , title = "Distribution of US Grants Spending in FY" + Select_year 
                      ,color_continuous_scale="magma",
                      hover_data = {"Amount": False,
                                    "log_Population":False,
                                    "Amount ": True,
                                   "Population ": True}
               , labels={'log_Population': 'Population'})
    fig2.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
    st.plotly_chart(fig2)

### Grants per country ###
row12_spacer1, row12_1, row12_spacer2 = st.columns((.2, 7.1, .2))
with row12_1:
    st.subheader('U.S. Grants Spending Trends')
row13_spacer1, row13_1, row13_spacer2, row13_2, row13_spacer3  = st.columns((.2, 2.3, .4, 4.4, .2))
with row13_1:
    st.markdown('What is the grants trend by continent and country?  What is the share of grants by continent and country?')    
    plot_continent = st.selectbox ("Select the continent you want to see:", ['All continents','Africa','Americas','Asia','Europe','Oceania'])
       
    if plot_continent == "All continents":
        plot_country = st.selectbox ("Select the country you want to see:", [''])
    elif plot_continent == "Africa":
        plot_country = st.selectbox ("Select the country you want to see:", ['South Africa', 'Ethiopia', 'Kenya', 'Nigeria', 'Uganda',
       'Tanzania', 'South Sudan', 'Central African Republic', 'Sudan',
       'DR Congo', 'Mozambique', 'Ghana', 'Somalia', 'Egypt', 'Liberia',
       'Senegal', 'Zambia', 'Niger', 'Rwanda', 'Malawi', 'Zimbabwe',
       "Cote d'Ivoire", 'Burkina Faso', 'Mali', 'Chad', 'Benin',
       'Botswana', 'Angola', 'Namibia', 'Cameroon', 'Madagascar', 'Libya',
       'Sierra Leone', 'Tunisia', 'Congo Republic', 'Morocco', 'Guinea',
       'Eswatini', 'Mauritania', 'Lesotho', 'Burundi', 'Gabon', 'Algeria',
       'Djibouti', 'Guinea-Bissau', 'Gambia', 'Cabo Verde', 'Togo',
       'Equatorial Guinea', 'Comoros', 'Mauritius', 'Western Sahara',
       'Seychelles', 'Sao Tome and Principe', 'St. Helena', 'Eritrea'])
    elif plot_continent == "Americas":
         plot_country = st.selectbox ("Select the country you want to see:", ['Haiti', 'Colombia', 'Guatemala', 'Canada', 'El Salvador', 'Peru',
       'Nicaragua', 'Honduras', 'Mexico', 'Brazil', 'Dominican Republic',
       'Paraguay', 'Ecuador', 'Jamaica', 'Barbados', 'Bermuda',
       'Trinidad and Tobago', 'Belize', 'Panama', 'Costa Rica',
       'Venezuela', 'Argentina', 'Bahamas', 'Bolivia', 'Guyana', 'Chile',
       'Uruguay', 'Dominica', 'Grenada', 'Suriname', 'Cuba',
       'Cayman Islands', 'Antigua and Barbuda',
       'St. Vincent and the Grenadines', 'Falkland Islands', 'Greenland',
       'St. Lucia', 'Aruba', 'Turks and Caicos Islands', 'St. Barths',
       'Anguilla', 'St. Kitts and Nevis', 'Saint-Martin',
       'British Virgin Islands', 'Curacao'])
    elif plot_continent == "Asia":
        plot_country = st.selectbox ("Select the country you want to see:", ['Syria', 'Afghanistan', 'Jordan', 'Pakistan', 'Bangladesh',
       'India', 'Yemen', 'Philippines', 'Iraq', 'Lebanon', 'Thailand',
       'Nepal', 'Myanmar', 'Turkey', 'Cambodia', 'Indonesia', 'Israel',
       'Vietnam', 'Laos', 'China', 'Tajikistan', 'Georgia', 'Kazakhstan',
       'Armenia', 'Kyrgyz Republic', 'Sri Lanka', 'Timor-Leste',
       'Maldives', 'Azerbaijan', 'Singapore', 'Japan', 'Malaysia',
       'Mongolia', 'Uzbekistan', 'South Korea', 'Saudi Arabia', 'Cyprus',
       'Turkmenistan', 'Bahrain', 'Taiwan', 'Bhutan',
       'United Arab Emirates', 'Macau', 'Hong Kong', 'Palestine', 'Qatar',
       'Kuwait', 'Oman', 'Brunei Darussalam', 'North Korea', 'Iran'])
    elif plot_continent == "Europe":
        plot_country = st.selectbox ("Select the country you want to see:", ['Switzerland', 'Italy', 'Ukraine', 'United Kingdom', 'France',
       'Moldova', 'Bosnia and Herzegovina', 'Austria', 'Macedonia',
       'Czech Republic', 'Germany', 'Serbia', 'Netherlands', 'Albania',
       'Denmark', 'Belarus', 'Malta', 'Sweden', 'Bulgaria', 'Russia',
       'Iceland', 'Finland', 'Ireland', 'Croatia', 'Belgium', 'Spain',
       'Poland', 'Hungary', 'Portugal', 'Greece', 'Kosovo', 'Luxembourg',
       'Lithuania', 'Romania', 'Montenegro', 'Estonia', 'Latvia',
       'Slovenia', 'Norway', 'Vatican', 'Slovakia', 'Andorra']) 
    else:
        plot_country = st.selectbox ("Select the country you want to see:", ['Fiji', 'Australia', 'Papua New Guinea', 'New Zealand',
       'Solomon Islands', 'New Caledonia', 'Vanuatu', 'Tonga',
       'French Polynesia', 'Samoa', 'Kiribati', 'Tuvalu', 'Nauru',
       'Cook Islands', 'Niue'])
        
            
        
with row13_2:
    if plot_continent == "All continents":
        conti_mean = all_year.groupby(["UN Region","Year"])[["Amount"]].mean().reset_index()
        fig6 = px.line(conti_mean, x='Year', y='Amount', color='UN Region', symbol="UN Region")
        fig6.update_layout(
            showlegend=True,
            plot_bgcolor="rgb(240,240,240)",
            margin=dict(t=40,l=0,b=0,r=0),
            title_text='FY2014-FY2022 Grants Trands by Continent',
            #title_font_family='Times New Roman',
            #legend_title_text='Dollars Obligated',
            title_font_size = 17,
            title_font_color="black",
            title_x=0.5,
            xaxis=dict(
            tickfont_size=14,
            tickangle = 270,
            showgrid = True,
            zeroline = True,
            showline = True,
            showticklabels = True,
            dtick=1
            ),
            legend=dict(
            x=0.01,
            y=0.99,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
            ),
            bargap=0.15)
        fig6.update_xaxes(tickangle=0)
        fig6.update_traces(line=dict(width=2.7),
                    marker=dict(size=7,line=dict(width=1,color='white')))
        st.plotly_chart(fig6)
        
    else:
        # filter countires by continent
        all_year_eu = all_year.loc[all_year["UN Region"] == plot_continent].reset_index()
        # clean the dataset
        all_year_eu = all_year_eu.drop(['index', 'Unnamed: 0'],axis = 'columns')
        # select the country 
        eu_sw = all_year_eu.loc[all_year_eu["Country Name"] == plot_country]
        # calculate the ave on the continent level 
        eu_mean = all_year_eu.groupby(["Year"])[["Amount"]].mean()
        # plot
        ##create figure with secondary y-axis
        fig7 = make_subplots(specs=[[{"secondary_y": True}]])

        ## add traces
        fig7.add_trace(
            go.Scatter(
                x=[2014, 2015, 2016, 2017, 2018,2019, 2020, 2021, 2022],
                y=eu_mean['Amount'],
                name="Europe average grants",
                mode='lines+markers', 
                marker={'size':9},
                line = dict(color='firebrick', width=2.7)),
                secondary_y=True
            )

        fig7.add_trace(
            go.Bar(
                x=[2014, 2015, 2016, 2017, 2018,2019, 2020, 2021, 2022],
                y=eu_sw['Amount'],
                name= plot_country + " grants amount",
                #text = eu_sw['Year'],
                textposition='outside',
                textfont=dict(
                size=13,
                color='#1f77b4'),
                marker_color='rgb(158,202,225)', 
                marker_line_color='rgb(17, 69, 126)',
                marker_line_width=2, 
                opacity=0.7),
                secondary_y=False
            )

        # strip down the rest of the plot

        #fig.update_traces(texttemplate='%{y:$.2s}')
        fig7.update_traces(texttemplate='%{y:.2s}')

        fig7.update_layout(
            showlegend=True,
            plot_bgcolor="rgb(240,240,240)",
            margin=dict(t=40,l=0,b=0,r=0),
            title_text='FY 2014-2022 Grants Amount of '+ plot_country,
            #title_font_family='Times New Roman',
            legend_title_text='Dollars Obligated',
            title_font_size = 17,
            title_font_color="black",
            title_x=0.5,
            xaxis=dict(
            tickfont_size=14,
            tickangle = 270,
            showgrid = True,
            zeroline = True,
            showline = True,
            showticklabels = True,
            dtick=1
            ),
            legend=dict(
            x=0.01,
            y=0.99,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
            ),
            bargap=0.15)

        ## set y-axes titles
        fig7.update_yaxes(title_text='Total Dollars Obligated USD', 
                         titlefont_size=16, 
                         tickfont_size=14,
                         secondary_y=False)
        fig7.update_yaxes(title_text='Average Dollars Obligated USD)', 
                         titlefont_size=16, 
                         tickfont_size=14, 
                         secondary_y=True)
        fig7.update_xaxes(tickangle=0)


        st.plotly_chart(fig7)
        
### Shared Prosperity ###
row8_spacer1, row8_1, row8_spacer2 = st.columns((.2, 7.1, .2))
with row8_1:
    st.subheader('Shared Prosperity: Monitoring Inclusive Growth')    
    
row9_spacer1, row9_1, row9_spacer2 = st.columns((.2, 7.1, .2))
with row9_1:
    st.subheader('Annualized Growth Rate')
row10_spacer1, row10_1, row10_spacer2, row10_2, row10_spacer3  = st.columns((.2, 2.3, .4, 4.4, .2))
with row10_1:
    plot_x_per_type = st.selectbox ("Which annualized growth rate do you want to see?", ['Shared Prosperity','Annualized Grants Growth Rate (2014-2019)'])
    st.markdown(""" 
    * **Shared Prosperity Index:** Shared prosperity measures the extent to which economic growth is inclusive by focusing on household consumption or income growth among the poorest population rather than on total growth.""")   
    st.markdown("""
* The five countries with the highest annualized grants growth rates are: Slovenia(150.74%, Europe), Togo(149.88%, Africa), Estonia(136.29%, Europe), Cuba(123.85%, Americas), Kosovo(95.25%, Europe).
*  And the five countries with the lowest (negative) annualized grants growth rates are: Fiji(-50.60%, Oceania), New Caledonia(-38.87%, Oceania), Palestine(-36.28%, Asia), Sierra Leone(-35.91%, Africa), Bulgaria(-31.09%, Europe).
""") 
    
    
with row10_2: 
    if plot_x_per_type == "Shared Prosperity":
        @st.cache(allow_output_mutation =True)
        def plot3(SSI):
            country_id_map = {}
            for feature in all_country["features"]:
                feature["properties"]['name']= coco.convert(names=feature["properties"]['name'], to='name_short')
                feature["id"] = feature["properties"]['name']
                country_id_map[feature["properties"]['name']] = feature["id"]    
            list = []##list the countires in the gepjson file 
            list.extend(country_id_map)
            list_0 = {"geo_list_0": list}
            geo_list = DataFrame(list_0)    
            SSI["standerd_name"]= coco.convert(names=SSI["countryname"], to='name_short')
            ## merge dfs
            merge_ssi = geo_list.merge(SSI,how="left",left_on="geo_list_0",right_on="standerd_name")
            merge_ssi_1 = merge_ssi.filter(["geo_list_0","Bottom 40%"])
            merge_ssi_2 = merge_ssi_1.rename(columns={"geo_list_0":"Country Name"})
            merge_ssi_2["id"] = merge_ssi_2["Country Name"].apply(lambda x:country_id_map[x])
            # plot 
            fig3 = px.choropleth_mapbox(merge_ssi_2,
                                locations = "id",
                                geojson = all_country,
                                color="Bottom 40%",
                               hover_name = "Country Name",
                               #hover_data = merge9.columns,
                                hover_data = {"id": False,
                                            "Bottom 40%":True},
                                 mapbox_style = "carto-positron",
                                color_continuous_scale="magma",
                                 zoom= 0.57,opacity = 0.3,
                                center = {"lat": 34.55,"lon":18.04},
                                title = "Map of Shared Prosperity"
                                )
            fig3.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
            return fig3
        fig3 = plot3(SSI)
        st.plotly_chart(fig3)
            
    else:
        @st.cache(allow_output_mutation =True)
        def plot4(merge_grants2014_2019):
            country_id_map = {}
            for feature in all_country["features"]:
                feature["properties"]['name']= coco.convert(names=feature["properties"]['name'], to='name_short')
                feature["id"] = feature["properties"]['name']
                country_id_map[feature["properties"]['name']] = feature["id"] 
            merge_grants2014_2019["id"] =merge_grants2014_2019["Country Name"].apply(lambda x:country_id_map[x])
            # plot 
            fig4 = px.choropleth_mapbox(merge_grants2014_2019,
                                locations = "id",
                                geojson = all_country,
                                color="Annualized Growth Rate",
                               hover_name = "Country Name",
                               #hover_data = merge9.columns,
                                hover_data = {"id": False,
                                            "Annualized Growth Rate":True,
                                             "2014 Amount":True,
                                             "2019 Amount":True},
                                 mapbox_style = "carto-positron",
                                color_continuous_scale="magma",
                                 zoom= 0.57,opacity = 0.3,
                                center = {"lat": 34.55,"lon":18.04},
                                title = "Map of FY 2014-2019 Grants Annualized Growth Rate"
                                ,labels={'Annualized Growth Rate': 'Grants Growth Rate'})
            fig4.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
            return fig4
        fig4 = plot4(merge_grants2014_2019)
        st.plotly_chart(fig4)
    
### SP v. Grants rate ###
row11_spacer1, row11_1, row11_spacer2 = st.columns((.2, 7.1, .2))
with row11_1:
    st.subheader('Analysis U.S. Grants & Shared Prosperity')
row11_spacer1, row11_1, row11_spacer2, row11_2, row11_spacer3  = st.columns((.2, 2.3, .4, 4.7, .2))
with row11_1:
    st.markdown("""
* American countries generally have lower Shared Prosperity (negative). Asia countries: Kazakhstan, Mongolia, and Iran, have negative income increase for Bottom 40% population. European countries, except Norway, have positive Shared Prosperity.""")
    st.markdown("") 
    st.markdown("""
* Annualized grants growth rate and Shared Prosperity index are positively correlated. """)
    
    
with row11_2:
    fig5 = px.scatter(grants2_inc_ssi_1, x="Annualized Growth Rate", y="Bottom 40%",
         size="Total Population", color="UN Region",
                 hover_name="Country Name", log_x=True, size_max=107,
                 hover_data = {"Total Population": False,
                                "Annualized Growth Rate":False,
                                 "Bottom 40%":True,
                                 "Annualized Growth Rate(%)":True,
                              "Population" : True}
                )
    fig5.update_layout(
        title='Grants Annualized Growth Rate v. Shared Prosperity',
        title_x=0.5,
        xaxis=dict(
            title='Grants Annualized Growth Rate (FY 2014-2019)',
            gridcolor='white',
            type='log',
            gridwidth=2,
        ),
        yaxis=dict(
            title='Bottom 40% Annualized Growth Rate of Income',
            gridcolor='white',
            gridwidth=2,
        ),
        #paper_bgcolor='rgb(243, 243, 243)',
        plot_bgcolor='rgb(243, 243, 243)',
        margin=dict(t=40,l=0,b=0,r=0),
        title_font_size = 17,
        title_font_color="black",
        legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01
        ))
    st.plotly_chart(fig5)
    
    
 





