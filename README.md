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

This assignment use the data sets from [link](https://github.com/rfordatascience/tidytuesday/tree/master/data/2018/2018-11-13). All data sets are relevent to the malaria disease. In order to do a better interaction, I choose plotly to visulize data, because it is more interactive, which means in this library, when we move our cursor over the plot, we can see the specific value of each point. And also, I choose scatter, line and violin plots to visulize the data comprehensively and set some buttons to make plots more interactive.

## Plot of malaria_deaths Data Set

Firstly, I read in the data set by pandas using raw data url. And then, we can view first a few lines of the data set.
```python
url1 = "https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2018/2018-11-13/malaria_deaths.csv"
malaria_deaths = pd.read_csv(url1, index_col=0).reset_index()
# Quick View of Data Sets
malaria_deaths.head()
```
![image.png](https://i.loli.net/2021/10/02/QH3T6zGm5RnEAxK.png)  
As we can see in the table, the data cover the number of malaria deaths from 1990 to 2016 for different countries. In order to show the number of malaria deaths for each country, I choose scatter plot to visualize (x axis is different countries and y axis is number of deaths) and add a animation bar of years under the plot so that the user can choose different year by themselves. In addition, the bar can go from 1990 to 2016 automatically, which can easily show the trend of number over years. Also, when moving cursor on points in the plot, we can also see the specifc value of the point.  
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

## Plot of malaria_deaths Data Set
Firstly, I read in the data set by pandas using raw data url. And then, we can view first a few lines of the data set.
```python
url2 = "https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2018/2018-11-13/malaria_deaths_age.csv"
malaria_deaths_age = pd.read_csv(url2, index_col=0)
# Quick View of Data Sets
malaria_deaths_age.head()
```
![image.png](https://i.loli.net/2021/10/02/pTYkIg3jfcONDPn.png)
As we can see in the table, the data cover the number of malaria deaths from 1990 to 2016 for different countries. In order to show the number of malaria deaths for each country, I choose scatter plot to visualize (x axis is different countries and y axis is number of deaths) and add a animation bar of years under the plot so that the user can choose different year by themselves. In addition, the bar can go from 1990 to 2016 automatically, which can easily show the trend of number over years. Also, when moving cursor on points in the plot, we can also see the specifc value of the point.  
