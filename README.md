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

## Table of Contents
1. [Final Dashboard](#finaldashboard)
2. [Introduction](#introduction)
3. [Data Preprocessing](#datapreprocessing)
4. [Data Visualization](#datavisualization)
5. [Dashboard](#dashboard)
6. [Deploy Dashboard to Public Website](#deploy)

---


## [Final Dashboard](https://phdgraduates.herokuapp.com/)<a name="finaldashboard"></a>
The final Dashboard I created is placed [above](https://phdgraduates.herokuapp.com/). Feel free to explore in my website!!!  

---

## Introduction<a name="introduction"></a>
This blog use the data sets from [Science and Engineering PhDs awarded in the US](https://ncses.nsf.gov/pubs/nsf19301/data). You can access the full code of the work in my [github](https://github.com/Caihanwang/BIOS823_Assignments/tree/Assignment-4).  

I have been curious about several questions about PhDs awarded in the US for a long time. To be more specific, which state has the most PhD graduates of different fields in a year? Which university is the most prolific for doctoral students in each state? Which is the most popular major for PhD students in US? In different major, which university has the most PhD graduates?  

With all these questions in mind, I choose to explore the table 7 of these data sets, which is "Doctorate-granting institutions, by state or location and major science and engineering fields of study: 2017". You can easily find all answers of the questions after data visualization!

---

## Data Preprocessing<a name="datapreprocessing"></a>
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

## Data Visualization<a name="datavisualization"></a>

### Which state had the most PhD graduates of different fields in 2017?
To answer the question, I choose to draw a choropleth plot to show the distribution of number of PhD graduates in the US. The plot is as following. We can see that California had the most PhD graduates in all fields in 2017.  

![plot1.gif](https://i.loli.net/2021/10/26/ZuOWi3XwfFzjopG.gif)  

The figure plotting code is as following:
```python
# Plot1. State Map Plot
## Prepare the data
states = (
    df2.groupby(["State", "Code", "Field"]).
    sum().reset_index().
    pivot(index = ["State","Code"], columns = "Field", values = "Number").
    reset_index()
)
states["All Fields"] = states[["Engineering", "Other", "Science"]].sum(axis = 1)

## figs1 plotting
figs1 = []
for i in ['All Fields', 'Engineering', 'Science', 'Other']:
    fig = px.choropleth(states,  # Input Pandas DataFrame
                        locations="Code",  # DataFrame column with locations
                        color=i,  # DataFrame column with color values
                        hover_name="State", # DataFrame column hover info
                        color_continuous_scale="Reds",
                        locationmode = 'USA-states') # Set to plot as US States
    fig.update_layout(
        title_text = 'Number of PhD Graduates by State', # Create a Title
        geo_scope='usa',  # Plot only the USA instead of globe
        title_x = 0.5
    )
    figs1.append(fig)
```

<br>  


### Which university was the most prolific for doctoral students in each state in 2017?
To answer the question, I choose to draw a bar plot to show the number of PhD graduates in different institutions. The plot is as following. As I just mentioned above, California had the most PhD graduates in all fields. We can set the dropdown menu to California to see the breakdown. In California, UCB had the most PhD graduates in 2017.  
![plot2.gif](https://i.loli.net/2021/10/26/1JmRYjeOfoXaQkH.gif)

The figure plotting code is as following:
```python
# Plot2. Histogram by Institution
## Prepare the data
Institution = (
    df2.groupby(["Institution", "State","Code", "Field"]).
    sum().reset_index().
    pivot(index = ["Institution", "State","Code"], columns = "Field", values = "Number").
    reset_index()
)

## figs2 plotting
figs2 = []
for i in state_names:
    fig = px.histogram(Institution[Institution["State"] == i], 
                        x = "Institution", 
                        y = ["Engineering", "Science", "Other"])
    fig.update_layout(
        title_text = 'Breakdown of Institutions by State', 
        title_x = 0.5,
        yaxis_title = "Count by Fields",
        xaxis_title = None,
        margin=dict(l=100, r=100)
        )
    # fig.update_layout(
    #     {'plot_bgcolor': 'rgba(0, 0, 0, 0)'}
    # )
    figs2.append(fig)
```

<br>  

### Which is the most popular major for PhD students in US in 2017?
To answer the question, I choose to draw a bar plot to show the number of PhD graduates in different majors. The plot is as following. As we can see, there was the most PhD graduates in the biologcial and biomedical sciences in 2017.  
![plot3.gif](https://i.loli.net/2021/10/26/u9S5kpgKE3NcZe2.gif)  

The figure plotting code is as following:  
```python
# Plot3. different majors
## Prepare the data
specificity = df2.groupby("Specificity").sum().reset_index()
specificity = specificity[specificity["Specificity"] != "Other"]

## figs3 plotting
figs3 = px.bar(specificity, 
             y = "Specificity", x = "Number")
figs3.update_layout(
        title_text = 'Number of PhD Graduates Breakdown of Major', 
        title_x = 0.5,
        yaxis_title = None,
        xaxis_title = "Count",
        margin=dict(l=100, r=100)
        )
```        

<br>  


### In different major, which university had the most PhDs graduates in 2017?
To answer the question, I choose to draw a bar plot to show top 10 institutions with the most PhD graduates in different majors. The plot is as following. In biological and biomedical sciences, Harvard University had the most PhD graduates in 2017. In computer and information sciences, Carnegie Mellon University had the most PhD graduates in 2017.   
![plot4.gif](https://i.loli.net/2021/10/26/g9RCqs6TLxbf1EJ.gif)

The figure plotting code is as following:  
```python
# Plot4. Top 10 institutions in different major
## Prepare the data
majors = df2.groupby(["Institution", "Specificity"]).sum().reset_index()

## figs4 plotting
majorlist = sorted(list(set(df2["Specificity"])))
figs4 = []
for i in majorlist:
    major = (
        majors[majors["Specificity"] == i].
        sort_values(by = "Number", ascending = False).head(10)
    )
    fig = px.bar(major, 
             x = "Institution", y = "Number")
    fig.update_layout(
        title_text = f'Top 10 Institutions with the Most PhD Graduates in {i}', 
        title_x = 0.5,
        yaxis_title = "Count",
        xaxis_title = None,
        margin=dict(l=20, r=20)
        )
    figs4.append(fig)
```        

<br>  

---

## Dashboard<a name="dashboard"></a>

### Layout

I set the layout for the dashboard in this part.  

```python
app.layout = html.Div(children = [

    # Title
    html.H1(children='PhD Graduates for United States in 2017',
            style = {'font-family':'Helvetica',
                     'font-size': '50px',
                     # "font-color": "white",
                     'width':'100%',
                     'display': 'inline-block',
                     'textAlign': 'center',
                     #'background-image': 'url(https://i.loli.net/2021/10/25/YbNJ7aAvXMpwenu.png)',
                     "background": "#0040FF"}
                     ),

    # Anthor
    html.H2(children='Author: Caihan Wang',
            style = {'font-family':'Helvetica',
                     'font-size': '20px',
                     'width':'100%',
                     'display': 'inline-block',
                     'textAlign': 'center'}
                     ),

    # Subtitle 1
    html.H3(children='Which state had the most PhD graduates by field in 2017?',
            style = {'font-family':'Helvetica',
                     'font-size': '30px',
                     'width':'100%',
                     'display': 'inline-block',
                     'textAlign': 'center',
                     "background": "#5882FA"}
                     ),    
    # Figs1
    html.Div(children = [

        dcc.Graph(id='plot'),

        html.Div('Change Field: ',
                 style = {'font-family':'Helvetica',
                          'font-size': '15px',
                          'textAlign': 'right',
                          'width':'35%',
                          'display': 'inline-block'
                          }),

        html.Div('',
                 style = {'font-family':'Helvetica',
                          'font-size': '15px',
                          'textAlign': 'right',
                          'width':'5%',
                          'display': 'inline-block'
                          }),


        dcc.RadioItems(
            id='map',
            options=[{'label': i, 'value': i} for i in figs_map],
            value=figs_map[0],
            labelStyle = {'display': 'inline-block', 
                            'cursor': 'pointer', 
                            'margin-right': '20px',
                            },
            style = {'font-family':'Helvetica',
                     'font-size': '15px',
                     'width':'60%',
                     'textAlign': 'left',
                     'display': 'inline-block'})
                    ]),         

    

    # Subtitle 2
    html.H3(children='Which university was the most prolific for PhD students by state in 2017?',
            style = {'font-family':'Helvetica',
                     'font-size': '30px',
                     'width':'100%',
                     'display': 'inline-block',
                     'textAlign': 'center',
                     "background": "#5882FA"}
                     ),    

    # Figs2
    html.Div(children = [

        dcc.Dropdown(
            id = "institute",
            options = [{"label": i, "value": i} for i in state_names],
            value = state_names[0]
        ),

        dcc.Graph(id='histogram')
                # style={"height": "60%", 
                #         "width": "80%",
                #         "textAlign": "center"}),

        ]),

    # Subtitle 3
    html.H3(children='Which is the most popular major for PhD students in US in 2017?',
            style = {'font-family':'Helvetica',
                     'font-size': '30px',
                     'width':'100%',
                     'display': 'inline-block',
                     'textAlign': 'center',
                     "background": "#5882FA"}
                     ),     

    # Figs3
    html.Div(children = [
        dcc.Graph(figure = figs3)
        ]),

    # Subtitle 4
    html.H3(children='Which institution had the most PhD graduates by major in 2017?',
            style = {'font-family':'Helvetica',
                     'font-size': '30px',
                     'width':'100%',
                     'display': 'inline-block',
                     'textAlign': 'center',
                     "background": "#5882FA"}
                     ),                             

    # Figs4
    html.Div(children = [

        dcc.Dropdown(
            id = "major",
            options = [{"label": i, "value": i} for i in majorlist],
            value = "Anthropology"
        ),

        dcc.Graph(id='histogram2')
                # style={"height": "60%", 
                #         "width": "80%",
                #         "textAlign": "center"}),

        ])

    ])
```

### App Callback

Use app.callback to link the figure with the dashboard.  

```python
@app.callback(
    Output('plot', 'figure'),
    [Input('map', 'value')])

def update_graph1(fig_name):
    for i in range(len(figs_map)):
        if fig_name == figs_map[i]:
            return figs1[i]

@app.callback(
    Output('histogram', 'figure'),
    [Input('institute', 'value')])

def update_graph2(fig_name):
    for i in range(len(state_names)):
        if fig_name == state_names[i]:
            return figs2[i]

@app.callback(
    Output('histogram2', 'figure'),
    [Input('major', 'value')])

def update_graph3(fig_name):
    for i in range(len(majorlist)):
        if fig_name == majorlist[i]:
            return figs4[i]

```

---

## Deploy Dashboard to Public Website<a name="deploy"></a>

I used heraku to deploy my website ([tutorial](https://medium.com/analytics-vidhya/how-to-deploy-a-dashboard-to-heroku-3b458f321c93)).  
Firstly, I signed in my account on [heraku](https://dashboard.heroku.com/apps) and created an app in my account.  
Second, I created an empty folder in local machine and put app.py, requirement.txt and Procfile in it.  
Then, I initialized the folder and activated a virtual environment.  
Finally, I used git add, git commit, git push to deploy my app to Heroku.  
The final dashboard is [here](https://phdgraduates.herokuapp.com/).  

---



