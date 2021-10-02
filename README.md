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

## Plot of malaria_deaths Data Set

Firstly, I read in the data set by pandas using raw data url. And then, we can view first a few lines of the data set.
```python
url1 = "https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2018/2018-11-13/malaria_deaths.csv"
malaria_deaths = pd.read_csv(url1, index_col=0).reset_index()
# Quick View of Data Sets
malaria_deaths.head()
```
