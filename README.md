---
title: "BIOS 823 Homework 4: Is there life after graduate school?"
layout: post
date: 2021-10-25 22:48
image: https://i.loli.net/2021/10/26/TBdMjnNcIeS7oKW.png
headerImage: true
tag:
- python
- BIOS823
category: blog
author: Caihan Wang
description: 823 HW3
---

# Is there life after graduate school?


## [Dashboard](https://phdgraduates.herokuapp.com/)
The final Dashboard I created is placed [above](https://phdgraduates.herokuapp.com/). Feel free to explore in my website!!!  

---

## Introduction
This blog use the data sets from [Science and Engineering PhDs awarded in the US](https://ncses.nsf.gov/pubs/nsf19301/data). In order to explore the data of PhDs awarded in the US by different locations and majors, I choose the table 7 of these data sets to do some analysis and visualization, which is "Doctorate-granting institutions, by state or location and major science and engineering fields of study: 2017". You can access the full code of the work in my [github](https://github.com/Caihanwang/BIOS823_Assignments/tree/Assignment-4).  

I have been curious about several questions about PhDs awarded in the US for a long time. To be more specific, which state has the most PhD graduates of different fields in a year? Which university is the most prolific for doctoral students in each state? Which is the most popular major for PhD students in US? In different major, which university is the best?  

With all these questions in mind, I choose to explore the table 7 of these data sets, which is "Doctorate-granting institutions, by state or location and major science and engineering fields of study: 2017". You can easily find all answers of the questions after data visualization!

---

## Data Preprocessing
Firstly, I read in the data set by pandas using raw data url. The data is multi-index and it is xlsx, so I use read_excel function.
```python
# Read in data
with warnings.catch_warnings(record=True):
    warnings.simplefilter("always")
    df = pd.read_excel("https://ncses.nsf.gov/pubs/nsf19301/assets/data/tables/sed17-sr-tab007.xlsx",
     engine="openpyxl", header = [3,4,5])
     
df.head()
```
The raw data looks like:  
![image.png](https://i.loli.net/2021/10/26/krn8mGHA5xsDi29.png)  

Secondly, I use functions in pandas library to clean the data.  
```python
# create a state names list by us packages
state_names = [state.name for state in us.states.STATES_AND_TERRITORIES]
state_names = state_names + ["District of Columbia"]

# Add two columns: State, Code
df["State"] = df[df.columns[0]][df[df.columns[0]].isin(state_names)]
df["State"] = df["State"].fillna(method = "ffill")
df = df.dropna()
df["Code"] = [us.states.lookup(i).abbr for i in df["State"]]

# Add one columns: Other
cols = []
for i in list(df.columns):
    if i[2] == "Total":
        cols.append(i)
df[("Other", "Other", "Other")] = df[df.columns[1]] - df[cols].sum(axis = 1)

# Melt and clean data
df2 = pd.melt(df, 
        id_vars = [('State or location and institution',
                     'Unnamed: 0_level_1',
                     'Unnamed: 0_level_2'), "State", "Code"],
        value_name = "Number",
        var_name = ["Field", "Major", "Specificity"]
       )
df2 = df2.rename(columns = {
        ('State or location and institution', 'Unnamed: 0_level_1', 'Unnamed: 0_level_2'): "Institution"
        })

## Delete "All fields"
df2 = df2.loc[df2['Field'] != "All fields" ]
## Delete "All institutions"
df2 = df2.loc[df2['Institution'] != "All institutions"]
## Delete "Total"
df2 = df2.loc[df2['Specificity'] != "Total"]
## Delete States
df2 = df2.loc[~df2['Institution'].isin(state_names)]
## Rename unnamed rows
Unname_list = [f"Unnamed: 2{a}_level_1" for a in range(1,10)]
df2["Major"][df2["Major"].isin(Unname_list)] = "Engineering"
df2["Major"][df2["Major"] == "Unnamed: 1_level_1"] = "All majors"
df2["Specificity"][df2["Specificity"] == "Unnamed: 1_level_2"] = "All specificity"
## Reset index
df2 = df2.reset_index(drop = True)
## df2 is the clean version of the data
df2.head()
```
The clean data is as following:  
![image.png](https://i.loli.net/2021/10/26/wgOS4kMpZGIJUhl.png)


---


## Plot of malaria_deaths_age Data Set
Firstly, I read in the data set by pandas using raw data url. And then, we can view first a few lines of the data set.
```python
url2 = "https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2018/2018-11-13/malaria_deaths_age.csv"
malaria_deaths_age = pd.read_csv(url2, index_col=0)
# Quick View of Data Sets
malaria_deaths_age.head()
```
![image.png](https://i.loli.net/2021/10/02/pTYkIg3jfcONDPn.png)  
As we can see in the table, the data cover the number of malaria deaths from 1990 to 2016 for 5 age groups. In order to show the difference in deaths between each group and trend of all years, I choose line plot to visualize (x axis is years, y axis is number of deaths and age groups are in different colors). And also, I add a interactive button over the plot so that users can choose different country by themselves. In addition, when moving cursor on points in the plot, we can also see the specifc value of the point. However, there are some countries that number of malaria deaths is zero in all years. For this condition, I consider it as missing value and I will not plot the data of these countries.  
```python
# Data Visulization for malaria_deaths_age data set
def death_age(Country):
    ## select country
    country_data = malaria_deaths_age[malaria_deaths_age["entity"] == Country]
    
    ## If the data is all 0, we will not use it to plot
    if set(country_data["deaths"]) == {0.0}:
        print(f"We have no data for {Country}")
        
    else:
        fig = px.line(country_data, 
                      ## set x, y and color
                          x = "year", 
                          y = "deaths",
                     color = 'age_group',
                      
                    ## set title and rename labels
                     title = f"Number of Deaths for Malaria over years by age groups in {Country}",
                     labels = {
                         "year": "Year",
                         "deaths": "Number of Deaths (per 100,000 people)"
                     })

        fig.show()
        
## use widgets interaction       
widgets.interact(death_age, Country = sorted(set(malaria_deaths_age["entity"])))
```  
The output is as following:  
![plot2.gif](https://i.loli.net/2021/10/02/VlGMSoIxD4zbLph.gif)  
If there is only missing data of that country, we will not plot it. The result will be like:  
![image.png](https://i.loli.net/2021/10/02/Ww8lPT4DjbzQYNX.png)  

---

## Plot of malaria_inc data set
Firstly, I read in the data set by pandas using raw data url. And then, we can view first a few lines of the data set.
```python
url3 = "https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2018/2018-11-13/malaria_inc.csv"
malaria_inc = pd.read_csv(url3, index_col=0).reset_index()
# Quick View of Data Sets
malaria_inc.head()
```
![image.png](https://i.loli.net/2021/10/02/Sz7vT3wRldmXBaq.png)  
As we can see in the table, the data cover the incidence of malaria in 2000, 2005, 2010, 2015 for different countries. In order to show the distribution of makaria incidence in different years and calculate the median incidence of all years, I choose violin plot with all points besides (x axis is years, y axis is incidence of malaria). In addition, when moving cursor on points in the plot, we can also see the specifc value of the point. Also, when moving cursor on the violin, we can see the min, max. 1st quarter, 3rd quarter and median on the plot.  
```python
# Data Visulization for malaria_inc data set
fig = px.violin(malaria_inc,
             ## set x and y
             x = "Year",
             y = "Incidence of malaria (per 1,000 population at risk) (per 1,000 population at risk)",
                
             ## show all the points
             points = "all",
                
             ## rename label and hover name
             labels = {
                         "Incidence of malaria (per 1,000 population at risk) (per 1,000 population at risk)": "Incidence"
                     },
             hover_name = "Entity"
               )

## rename y axis and title
fig.update_layout(yaxis_title="Incidence of malaria (per 1,000 population at risk)", 
                  title = "Violin Plot of Incidence of Malaria over years")

fig.show()
```
The output is as following:  
![plot3.gif](https://i.loli.net/2021/10/02/yFcM69BLiC2PU8z.gif)  

---
