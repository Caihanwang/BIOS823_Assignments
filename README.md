---
title: "BIOS 823 Homework 3: Data Visulization"
layout: post
date: 2021-10-01 22:48
# image: /assets/images/markdown.jpg
headerImage: false
tag:
- python
- BIOS823
category: blog
author: Caihan Wang
description: 823 HW3
---

# Data Visulization

## Introduction

This assignment use the data sets from [link](https://github.com/rfordatascience/tidytuesday/tree/master/data/2018/2018-11-13). All data sets are relevent to the malaria disease. In order to do a better interaction, I choose plotly to visulize data, because in this library, when we move our cursor over the plot, we can see the specific value of each point. And also, I choose scatter, line and violin plots to visulize the data comprehensively and set some buttons to make plots more interactive.

---

## Plot of malaria_deaths Data Set

Firstly, I read in the data set by pandas using raw data url. And then, we can view first a few lines of the data set.
```python
url1 = "https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2018/2018-11-13/malaria_deaths.csv"
malaria_deaths = pd.read_csv(url1, index_col=0).reset_index()
# Quick View of Data Sets
malaria_deaths.head()
```
![image.png](https://i.loli.net/2021/10/02/QH3T6zGm5RnEAxK.png)  
As we can see in the table, the data cover the number of malaria deaths from 1990 to 2016 for different countries. In order to show the number of malaria deaths for each country, I choose scatter plot to visualize (x axis is different countries and y axis is number of deaths) and add a animation bar of years under the plot so that the user can choose different year by themselves. In addition, the bar can go from 1990 to 2016 automatically, which can easily show the trend of number over years. Also, when moving cursor on points in the plot, we can also see the specifc value of the point. Because there are too many country codes on the x axis and it also shows some of them, we can zoom the plot (on the right up corner of the plot) to see the specific country.
```python
# Data Visulization for malaria_deaths data set
fig = px.scatter(malaria_deaths,
                ## set x and y
                x = "Code",
                y = "Deaths - Malaria - Sex: Both - Age: Age-standardized (Rate) (per 100,000 people)",
                
                ## make animation bar
                animation_frame="Year",
                 
                ## set color
                color = "Deaths - Malaria - Sex: Both - Age: Age-standardized (Rate) (per 100,000 people)",
                 
                ## rename labels
                labels = {
                         "Code": "Country Code",   
                         "Deaths - Malaria - Sex: Both - Age: Age-standardized (Rate) (per 100,000 people)": "Number of Deaths"
                     },
                
                ## set hover name and title
                hover_name = "Entity",
                title = "Number of Malaria Deaths over the world"
                )

# reset the size of plot and ylab name
fig.update_layout(margin=dict(l=20, r=20, t =30, b=100),
                 yaxis_title="Number of Deaths (per 100,000 people)")

fig.show()
```
The output is as following:
![plot1.gif](https://i.loli.net/2021/10/02/HX2Vm9fUkDthNSZ.gif)  


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
