# USASpending-SharedProsperity-APP
# Streamlit Cloud Link: 
[https://peijin0405-usaspending-sharedprosperity-app-app-code-r7n4tx.streamlit.app/](https://usaspending-sharedprosperity-app.streamlit.app/)

### US Grants - Shared Prosperity Analyzer
#### Executive summary
The data I employ for the final project comes from USAspending API  and Shared Prosperity data from the Global Database of Shared Prosperity . Firstly, I map the grant data from the fiscal year 2014 (from Oct. 2013 to Sep. 2014) to 2022 (from Oct. 2021 to Sep. 2022). This step explores how the U.S. has invested in Grants worldwide at different times. Next, I make a sunburst plot using the same dataset, which further shows the share of each continent and the share of different countries within the continent. After that, with the FY2014 and FY2019 grants data, I calculate the average annualized growth rate of U.S. grants to each country and further explore the distribution of average annualized grants growth rate and Shared Prosperity around the world. Last, I use a bubble chart to reveal the relationship between annualized grants growth rate and Shared Prosperity. Then I deploy the visualization on Streamlit Cloud , so it will be displayed as an application, and viewers can check out these charts with a click.

#### Data 
“Shared prosperity focuses on the poorest 40 percent of the population in a country (the bottom 40) and is defined as the annualized growth rate of their mean household per capita consumption or income”(World Bank, 2022). Shared prosperity measures the extent to which economic growth is inclusive, focusing on household consumption or income growth of the poorest rather than aggregate growth. It is an important indicator of inclusion and well-being that correlate with reductions in poverty and inequality. The baseline year of Shared Prosperity varies among countries, but the majority of them start around 2014 and end around 2019.  

In order to match the scale of Share Prosperity data, I use FY2014 and FY2019 grants data to calculate the annualized grants growth rate with the formula : 

$$
\text{CAGR}(t_0, t_n) = \left( \frac{V(t_n)}{V(t_0)} \right)^{\frac{1}{t_n - t_0}} - 1
$$

where V(tn) is the initial value, V(t0) is the end value, and tn-t0 is the number of years. In this case, V(tn) equals to Grants 2014, V(t0) equals to Grants 2019, and (tn-t0) equals to 5.

#### Trend 
![QQ图片20230105221330](https://user-images.githubusercontent.com/89746479/210922662-e2f99d39-863c-4167-aa16-d60d37f2f064.png)

#### Insights
First, with the choropleth chart of U.S. Grants spending from FY2014 to FY2022. We could find that each year, more than two hundred countries receive grants from the United States; however, grants disproportionately go to a few. And Africa has long been the largest grants recipient continent. In recent years, there has been a significant increase in funding to East Asia (mainly Ukraine). This may be related to the international political situation and international relations.

With the Sunburst Chart of U.S. Grants Spending, we can learn that The long-standing distribution pattern is that the African continent has the largest share, followed by Europe, then Asia and the Americas, with Australia having the smallest share. After 2020, the U.S. grants gradually tilted toward Europe. In European, the grants are mainly concentrated in two countries-Switzerland and Ukraine. In 2022, the sum of the two countries accounts for about 90% of the entire European grants. 

In the analysis of the Annualized Growth Rate of Shared Prosperity and the Annualized Grants Growth Rate (2014-2019), we observe that countries in the Americas, such as Colombia, Argentina, and Peru, generally experience lower Shared Prosperity, with the bottom 40% of the population showing little or no income growth. Similarly, in Europe, countries like Switzerland and Russia report negative growth for this segment, while most European countries, except Norway, show positive Shared Prosperity.

In contrast, most Asian countries report positive growth for the lower-income population, though there are exceptions such as Kazakhstan, Mongolia, and Iran, where income increases for the bottom 40% remain negative. Notably, Turkey also shows a decline in this group’s prosperity.

A significant insight from this analysis is the positive correlation between the Annualized Grants Growth Rate and the Shared Prosperity Index. Although this correlation does not necessarily imply a causal relationship, it opens up avenues for further research on the potential impact of U.S. grants on inclusive economic growth across different regions.

