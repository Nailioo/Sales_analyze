#!/usr/bin/env python
# coding: utf-8

# In[98]:


import pandas as pd
import numpy as np
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
import seaborn as sns

import plotly.express as px


# Тестовое задание на позицию “Аналитик данных”
#  
# Имеется набор данных. Необходимо проанализировать его и представить ответы на вопросы с визуализацией каждого пункта.
#  Ссылка: https://docs.google.com/spreadsheets/d/1DkdhWMrVjtflQfmCIKl8hCjSlIxph1L42_fgyFo0QPs/edit?usp=sharing
#  
# Задание 1
#  а) Какие подгруппы товаров наиболее часто покупают за все время продаж (минимум 4 группы)?
#  б) Какие подгруппы товаров наиболее часто покупают за последние два года (минимум 4 группы)?
#  в) Какие подгруппы товаров наиболее часто покупают за последний год(минимум 4 группы)?
# 
#  Подгруппа – Sub-Category
#  Дата – Order_date
#  Сделать вывод на основе полученных результатов.
# 
#  Задание 2
#  Построить boxplot («Ящик с усами») на основе продаж (Sales). Найти мажоритарную черту (т.е. избавиться от аномалий и представить четкую картину распределения величин).
#  Можно использовать правило трех сигм. Однако любые другие решения приветствуются.
# 
#  Задание 3
#  Для этого задания необходимо разбить все покупки на энное количество групп “Sale_group” (Допустим маленькие продажи, средние и высокие) на основе Sales
# Сгруппировать данные на основе региона и группы продаж (Region, Sale_group). Определить основные тенденции и паттерны. Выделить наиболее «прибыльную» группу.
# 
#  Замечания: Работу лучше выполнить в jupyter и там же написать выводы по каждому заданию. После выполнения загрузите код на github.
# 

# In[99]:


gsheetid = '1DkdhWMrVjtflQfmCIKl8hCjSlIxph1L42_fgyFo0QPs' 
sheet_name = 'Sheet1'
gsheet_url = f'https://docs.google.com/spreadsheets/d/{gsheetid}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
df = pd.read_csv(gsheet_url)
df.head()


# In[100]:


# проверяем типы данных
df.dtypes


# In[101]:


# проверяем на наличие пустых значений - их нет
df.isna().sum()


# In[103]:


# Переименуем столбцы для удобства
df = df.rename(columns={"Order Date": "Order_Date", "Sub-Category": "Sub_Category"})


# In[104]:


# Преобразуем типы данных для дальнейшей работы
df['Order_Date'] = pd.to_datetime(df['Order_Date'], format='%d/%m/%Y')
df['Sales'] = df['Sales'].str.replace(',', '.')
df['Sales'] = df['Sales'].astype(float)


# ### Задание 1
# - а) Какие подгруппы товаров наиболее часто покупают за все время продаж (минимум 4 группы)? 
# - б) Какие подгруппы товаров наиболее часто покупают за последние два года (минимум 4 группы)? 
# - в) Какие подгруппы товаров наиболее часто покупают за последний год(минимум 4 группы)?

# а) Какие подгруппы товаров наиболее часто покупают за все время продаж (минимум 4 группы)?

# In[105]:


df[['ID','Sub_Category']].groupby('Sub_Category', as_index = False)                         .count().sort_values(by='ID', ascending=False)                         .head(4)


# - б) Какие подгруппы товаров наиболее часто покупают за последние два года (минимум 4 группы)? 
# - в) Какие подгруппы товаров наиболее часто покупают за последний год(минимум 4 группы)?

# In[106]:


##Отфильтруем датасет,оставив только покупки за последние 2 года


# In[115]:


max_date = df['Order_Date'].max()


# In[110]:


start_date_2_years = max_date - pd.DateOffset(years=2)
print(start_date_2_years)
start_date_1_year = max_date - pd.DateOffset(years=1)
print(start_date_1_year)


# In[111]:


### отфильрованный датасет
df_last_2_years = df[(df['Order_Date'] >= start_date_2_years) & (df['Order_Date'] <= max_date)]
df_last_1_year = df[(df['Order_Date'] >= start_date_1_year) & (df['Order_Date'] <= max_date)]


# Какие подгруппы товаров наиболее часто покупают за последние два года (минимум 4 группы)? 

# In[113]:


df_last_2_years[['ID','Sub_Category']].groupby('Sub_Category', as_index = False)                                      .count().sort_values(by='ID', ascending=False).head(4)


# Какие подгруппы товаров наиболее часто покупают за последний год(минимум 4 группы)?

# In[114]:


df_last_1_year[['ID','Sub_Category']].groupby('Sub_Category', as_index = False)                                       .count().sort_values(by='ID', ascending=False).head(4)


# ### Выводы
# - 1. Самыми популярными подгруппами за все время продаж являются: Binders, Paper, Furnishings, Phones
# - 2. Самыми популярными подгруппами за 2 последних года продаж являются: Binders, Paper, Furnishings, Phones
# - 3. Самыми популярными подгруппами за все время продаж являются: Binders, Paper, Furnishings, Phones

# ### Задание 2
# Построить boxplot («Ящик с усами») на основе продаж (Sales). Найти мажоритарную черту (т.е. избавиться от аномалий и представить четкую картину распределения величин). Можно использовать правило трех сигм. Однако любые другие решения приветствуются

# In[51]:


df


# Построим боксплот для исходных данных

# In[52]:


plt.figure(figsize=(10, 6))
sns.boxplot(x=df['Sales'])
plt.title('Boxplot of Sales (Original)')
plt.xlabel('Sales')
plt.show()


# In[53]:


df['Sales'].describe()


# In[54]:


# Очистка данных по правилу трех сигм
mean_sales = df['Sales'].mean()
std_sales = df['Sales'].std()

# Определение границ для выбросов
lower_bound = mean_sales - 3 * std_sales
upper_bound = mean_sales + 3 * std_sales


# In[55]:


# Фильтрация данных для удаления выбросов
df_cleaned = df[(df['Sales'] >= lower_bound) & (df['Sales'] <= upper_bound)]

# Проверка очищенных данных
print(df_cleaned.describe())


# In[56]:


# Построение Boxplot для очищенных данных
plt.figure(figsize=(10, 6))
sns.boxplot(x=df_cleaned['Sales'])
plt.title('Boxplot of Sales (Cleaned)')
plt.xlabel('Sales')
plt.show()


# ### Задание 3 
# Для этого задания необходимо разбить все покупки на энное количество групп “Sale_group” (Допустим маленькие продажи, средние и высокие) на основе Sales Сгруппировать данные на основе региона и группы продаж (Region, Sale_group). Определить основные тенденции и паттерны. Выделить наиболее «прибыльную» группу

# In[116]:


# Определяем границы для групп по 33 и 67 квартилю
sales = df['Sales']
quantiles = sales.quantile([0.33, 0.67])

def sale_group(amount):
    if amount <= quantiles[0.33]:
        return 'Low'
    elif amount <= quantiles[0.67]:
        return 'Medium'
    else:
        return 'High'

df['Sale_group'] = df['Sales'].apply(sale_group)


# In[117]:


quantiles


# In[118]:


df


# In[119]:


grouped_data = df.groupby(['Region','Sale_group'],as_index=False).agg({'Sales': ['sum', 'mean', 'count']})


# In[120]:


grouped_data.columns = ['Region', 'Sale_group', 'Total_Sales', 'Average_Sales', 'Count']


# In[121]:


grouped_data


# In[122]:


grouped_data.groupby('Sale_group')['Total_Sales'].sum().idxmax()


# In[123]:


group_sales = df['Sale_group'].value_counts()
plt.figure(figsize=(8, 8))
plt.pie(group_sales, labels=group_sales.index, autopct='%1.1f%%', startangle=140)
plt.title('Распределение по группам продаж')
plt.show()


# In[125]:


plt.figure(figsize=(12, 8))
sns.barplot(x='Region', y='Total_Sales', hue='Sale_group', data=grouped_data)
plt.title('Суммарные продажи по регионам и группам продаж')
plt.xlabel('Регион')
plt.ylabel('Суммарные продажи')
plt.xticks(rotation=45)
plt.legend(title='Группа продаж')
plt.show()

region_sales = df['Region'].value_counts()
plt.figure(figsize=(8, 8))
plt.pie(region_sales, labels=region_sales.index, autopct='%1.1f%%', startangle=140)
plt.title('Распределение по регионам')
plt.show()


# Лидером по суммарным продажам является Калининград

# In[88]:


plt.figure(figsize=(12, 8))
sns.barplot(x='Region', y='Average_Sales', hue='Sale_group', data=grouped_data)
plt.title('Средние продажи по регионам и группам продаж')
plt.xlabel('Регион')
plt.ylabel('Средние продажи')
plt.xticks(rotation=45)
plt.legend(title='Группа продаж')
plt.show()


# По графику видно, что средние продажи во всех регионах примерно одинаковые

# ### Выводы:
#      1. Лидером по продажам является Калиниград
#      2. Средние продажи по группам во всех регионах практические одинаковые
#      3. Распределение числа продаж по группам равное 

# In[ ]:




