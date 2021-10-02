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

## Plot of malaria_deaths Data Set

Firstly, I read in the data set by pandas using raw data url. And then, we can view first a few lines of the data set.
```python
url1 = "https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2018/2018-11-13/malaria_deaths.csv"
malaria_deaths = pd.read_csv(url1, index_col=0).reset_index()
# Quick View of Data Sets
malaria_deaths.head()
```
![image.png](https://i.loli.net/2021/10/02/QH3T6zGm5RnEAxK.png)  
As we can see in the table, the data cover the number of malaria deaths from 1990 to 2016 for different countries. 
