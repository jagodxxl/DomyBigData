#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
strona=requests.get('https://www.otodom.pl/sprzedaz/mieszkanie/pomorskie/?search%5Bregion_id%5D=11')


# In[2]:


print('Długość w znakach',len(strona.text))


# In[3]:


strona.text[:200]


# In[4]:


strony=[]

import time
for i in range(1,11):
    print('https://www.otodom.pl/sprzedaz/mieszkanie/pomorskie/?search%5Bregion_id%5D=11&page='+str(i))
    strony.append(
        requests.get(
            'https://www.otodom.pl/sprzedaz/mieszkanie/pomorskie/?search%5Bregion_id%5D=11&page='+str(i)))
    time.sleep(2.5)


# In[5]:


len(strony)


# In[6]:


from bs4 import BeautifulSoup


# In[7]:


import csv
with open('nieruchomosci.csv','w') as plik:
    writer=csv.writer(plik, delimiter=";")
    writer.writerow(['Opis','Metraż [m2]','Pokoje','Cena [PLN]','Cena/m2 [PLN]','Lokalizacja','Miasto'])
    for element in strony:
        znaczniki=BeautifulSoup(element.text,'html.parser')
        opisy=znaczniki.findAll('span', {'class': 'offer-item-title'})
        lokalizacje=znaczniki.findAll('p',attrs={'class':'text-nowrap'})
        pokoje=znaczniki.findAll('li',attrs={'class':'offer-item-rooms hidden-xs'})
        ceny=znaczniki.findAll('li',attrs={'class':'offer-item-price'})
        metraze=znaczniki.findAll('li',attrs={'class':'hidden-xs offer-item-area'})
        ceny_m=znaczniki.findAll('li',attrs={'class':'hidden-xs offer-item-price-per-m'})
        for opis, lokalizacja, pokoj, cena, metraz, cena_m in zip (opisy,lokalizacje,pokoje,ceny,metraze,ceny_m):
            print(opis.text.strip(),';',metraz.text.strip(),';',pokoj.text.strip(),';',cena.text.strip(),';',cena_m.text.strip(),';',lokalizacja.text.strip())
            txt1=opis.text.strip().encode('windows-1250', errors = 'ignore').decode('windows-1250')
            txt2=metraz.text.strip().encode('windows-1250', errors = 'ignore').decode('windows-1250').split(' ')[0].replace(',','.')
            txt3=pokoj.text.strip().split(' ')[0]
            txt4=cena.text.replace('zł','').strip().replace(' ','').replace(',','.')
            txt5=cena_m.text.replace('zł/m²','').strip().replace(' ','').replace(',','.')
            txt6=lokalizacja.text.strip().split(':')[1]
            txt7=txt6.split(',')[0].strip()
            if txt4.find('Zapytaj')<0:
                writer.writerow([txt1,txt2,txt3,txt4,txt5,txt6,txt7])


# In[8]:


import pandas as pd
df=pd.read_csv("nieruchomosci.csv",delimiter=";",encoding="windows-1250")


# In[9]:


df.shape


# In[10]:


df.head(10)


# In[11]:


df[10:21]


# In[12]:


df.dtypes


# In[13]:


print("Tabela sortowanie w/g ceny rosnąco:")
Sorted = df.sort_values(['Cena [PLN]'], ascending=True)
Sorted[0:10]


# In[33]:


print("Tabela sortowanie w/g ceny rosnąco w Gdańsku:")
df_gdansk = df[df['Miasto'].str.match('Gdańsk')]
Sorted = df_gdansk.sort_values(['Cena [PLN]'], ascending=True)
Sorted[0:10]


# In[25]:


print("Tabela sortowanie w/g ceny za metr malejąco:")
Sorted = df.sort_values(['Cena/m2 [PLN]'], ascending=False)
Sorted[0:10]


# In[15]:


print("Tabela sortowanie w/g metrażu malejąco:")
Sorted = df.sort_values(['Metraż [m2]'], ascending=False)
Sorted[0:10]


# In[16]:


print("Wykres rozkładu ceny:")
df["Cena [PLN]"].plot()


# In[26]:


print("Wykres rozkładu ceny za metr:")
df["Cena/m2 [PLN]"].plot()


# In[17]:


print("Maksymalna cena:")
df[df["Cena [PLN]"] == df["Cena [PLN]"].max()]


# In[27]:


print("Maksymalna cena za metr:")
df[df["Cena/m2 [PLN]"] == df["Cena/m2 [PLN]"].max()]


# In[18]:


print("Podstawowe statystyki:")
df.describe()


# In[35]:


print("Podstawowe statystyki w Sopocie:")
df_sopot = df[df['Miasto'].str.match('Sopot')]
df_sopot.describe()


# In[19]:


import matplotlib.pyplot as plt


# In[30]:


print("Ceny maksymalne:")
df.groupby('Miasto')['Cena [PLN]'].max().plot(kind='pie')
plt.show()


# In[31]:


print("Ceny maksymalne za metr:")
df.groupby('Miasto')['Cena/m2 [PLN]'].max().plot(kind='pie')
plt.show()


# In[ ]:




