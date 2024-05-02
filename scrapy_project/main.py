from datetime import datetime

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#%%
dt = pd.read_csv("../scrapy_project/technologies.csv")

#%%

years = [2015, 2016, 2017, 2018, 2019]
population = [100, 120, 150, 180, 200]


plt.plot(years, population)
plt.title("Population Growth")
plt.xlabel("Year")
plt.ylabel("Population")


plt.show()

