#matplotlib

import matplotlib.pyplot as plt

#data
months=[1,2,3,4,5,6]
rent=[12000,13000,140000,15000,16000,17000]

#creating graph
plt.plot(months, rent)

plt.xlabel('Months')
plt.ylabel('rent')
plt.title('rent increase over 6 months!')

#show grph
plt.show()