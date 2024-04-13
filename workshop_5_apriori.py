# -*- coding: utf-8 -*-
"""Workshop_5_Apriori.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1XmM5RuEm52hg-f03LA7qzgjJ4w6mNF3n
"""

from google.colab import drive
drive.mount('/content/drive')

import pandas as pd

import numpy as np
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

############### Write your code in this cell (If applicable) ##################

portugal_data = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/DATA MINING/Portugal_online_retail.csv')
sweden_data = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/DATA MINING/Sweden_online_retail.csv')
uk_data = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/DATA MINING/UK_online_retail.csv')

uk_data

"""## PORTUGAL DATASET"""

portugal_data.head(2)

portugal_data=portugal_data.drop('InvoiceNo',axis=1)

# Finding the frequent itemsets
port_frquent_items = apriori(portugal_data, min_support = 0.1, use_colnames = True)

port_frquent_items.sort_values(by=['support'],ascending=False)

# Collecting the inferred rules in a dataframe
port_rules = association_rules(port_frquent_items, metric ="confidence", min_threshold = 0.1)

port_rules = port_rules.sort_values(by=['support'],ascending=False)
port_rules.head(3)

"""######################## Write your report in this cell (if applicable) #############################

Note: Double click to write

## SWEDEN DATASET
"""

sweden_data.head(2)

sweden_data=sweden_data.drop('InvoiceNo',axis=1)

# Finding the frequent itemsets
swed_frquent_items = apriori(sweden_data, min_support = 0.05, use_colnames = True)

swed_frquent_items.sort_values(by=['support'],ascending=False)

# Collecting the inferred rules in a dataframe
swed_rules = association_rules(swed_frquent_items, metric ="support", min_threshold = 0.05)

swed_rules = swed_rules.sort_values(by=['support'],ascending=False)
swed_rules.head(3)

"""######################## Write your report in this cell (if applicable) #############################

Note: Double click to write

## UK DATASET
"""

uk_data.head(5)

uk_data=uk_data.drop('InvoiceNo',axis=1)

# Finding the frequent itemsets
uk_frquent_items = apriori(uk_data, min_support = 0.05, use_colnames = True)

uk_frquent_items.sort_values(by=['support'],ascending=False)

# Collecting the inferred rules in a dataframe
uk_rules = association_rules(uk_frquent_items, metric ="confidence", min_threshold = 0.03)

uk_rules = uk_rules.sort_values(by=['support'],ascending=False)
uk_rules.head(3)

"""######################## Write your report in this cell (if applicable) #############################

##Portugal Dataset:

Customers who purchase the BAKING SET 9 PIECE RETROSPOT are highly likely (confidence of 75%) to also buy the RETROSPOT TEA SET CERAMIC 11 PC. This suggests a strong association between baking and tea sets, indicating potential cross-selling opportunities or bundled promotions.

Conversely, customers who purchase the RETROSPOT TEA SET CERAMIC 11 PC are also highly likely (confidence of 64%) to buy the BAKING SET 9 PIECE RETROSPOT. This reciprocal association mirrors the previous rule and reinforces the potential for bundled sales or targeted marketing strategies.

Customers who purchase the JUMBO SHOPPER VINTAGE RED PAISLEY are highly likely (confidence of 82%) to also buy the JUMBO BAG PINK VINTAGE PAISLEY. This strong association suggests a consistent preference among customers for vintage-style shopper bags, presenting opportunities for targeted promotions or product bundling.

##Sweden Dataset:


Customers who purchase the GUMBALL COAT RACK are virtually certain (confidence of 100%) to also buy POSTAGE. This indicates a strong dependency between these items, suggesting that the GUMBALL COAT RACK is likely a small, add-on item often purchased with other products necessitating postage.


Customers who purchase POSTAGE are moderately likely (confidence of 23%) to also buy the RED TOADSTOOL LED NIGHT LIGHT. This association suggests a weak dependency between postage and this particular night light, indicating potential for targeted marketing efforts to increase sales of the latter.


Conversely, customers who purchase the RED TOADSTOOL LED NIGHT LIGHT are virtually certain (confidence of 100%) to also buy POSTAGE. This reciprocal association reinforces the previous rule, indicating a consistent pattern of purchasing these items together.


##UK Dataset:

There is an association between purchasing the JUMBO BAG RED RETROSPOT and the JUMBO BAG PINK POLKADOT, suggesting a potential cross-selling opportunity between these two product variants.

Customers who purchase the JUMBO BAG RED RETROSPOT are likely to also purchase the JUMBO BAG WOODLAND ANIMALS, indicating a preference for jumbo bags featuring different designs or themes.

Similarly, customers who purchase the JUMBO BAG STRAWBERRY are likely to also purchase the JUMBO BAG WOODLAND ANIMALS, suggesting a similar preference for jumbo bags with different thematic designs.


(233 words)
"""