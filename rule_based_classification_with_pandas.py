################################ RULE BASED CLASSIFICATION WITH PANDAS ########################################
import pandas as pd

# Question 1: Read the persona.csv file and show the general information about the dataset.
def load_persona():
    df =  pd.read_csv("/home/nida/PycharmProjects/DSMLBC/Hws/week2/persona.csv")
    return df

df = load_persona()
df.head()
df.tail()
df.describe().T
df.columns
df.index
df.shape
df.isnull().values.any()
df.isnull().sum()

# Question 2: How many unique SOURCE are there? What are their frequencies?
df.columns
df['SOURCE'].unique()
#array(['android', 'ios']
df['SOURCE'].nunique()
#2
df['SOURCE'].value_counts()
"""OUT:
android    2974
ios        2026
"""

#Question 3: How many unique PRICEs are there?
df['PRICE'].nunique()

# Question 4: How many sales were made from which PRICE?
df['PRICE'].value_counts()
"""OUT:
29    1305
39    1260
49    1031
19     992
59     212
"""

# Question 5: How many sales were made from which country?
df['COUNTRY'].value_counts()
"""OUT:
usa    2065
bra    1496
deu     455
tur     451
fra     303
can     230
"""

# Question 6: How much was earned in total from sales by country?
df.groupby("COUNTRY").agg({"PRICE": "sum"})
"""OUT:
         PRICE
COUNTRY       
bra      51354
can       7730
deu      15485
fra      10177
tur      15689
usa      70225
"""

# Question 7: What are the sales numbers by SOURCE types?
df.groupby('SOURCE')["PRICE"].count()
#or
df.groupby('SOURCE').agg({"PRICE": "count"})
"""OUT: 
          PRICE
SOURCE        
android   2974
ios       2026
"""

# Question 8: What are the PRICE averages by country?

df.groupby('COUNTRY')['PRICE'].mean()
#or
df.groupby('COUNTRY').agg({"PRICE": "mean"})
"""OUT:
             PRICE
COUNTRY           
bra      34.327540
can      33.608696
deu      34.032967
fra      33.587459
tur      34.787140
usa      34.007264

"""

# Question 9: What are the PRICE averages based on SOURCEs?
df.groupby('SOURCE')['PRICE'].mean()
#or
df.groupby('SOURCE').agg({"PRICE": "mean"})
"""OUT:
             PRICE
SOURCE            
android  34.174849
ios      34.069102
"""

# Question 10: What are the PRICE averages in the COUNTRY-SOURCE breakdown?
df.groupby(by=["COUNTRY","SOURCE"])["PRICE"].mean()
"""OUT:
COUNTRY  SOURCE 
bra      android    34.387029
         ios        34.222222
can      android    33.330709
         ios        33.951456
deu      android    33.869888
         ios        34.268817
fra      android    34.312500
         ios        32.776224
tur      android    36.229437
         ios        33.272727
usa      android    33.760357
"""

# What are the average earnings in COUNTRY, SOURCE, SEX, AGE breakdown?
df.groupby(['COUNTRY','SOURCE','SEX','AGE']).agg({'PRICE': 'mean'})

"""OUT:
                                PRICE
COUNTRY SOURCE  SEX    AGE           
bra     android female 15   38.714286
                       16   35.944444
                       17   35.666667
                       18   32.255814
                       19   35.206897
                               ...
usa     ios     male   42   30.250000
                       50   39.000000
                       53   34.000000
                       55   29.000000
                       59   46.500000
"""

# Sort the output by PRICE.
agg_df = df.groupby(by=['COUNTRY','SOURCE','SEX','AGE']).agg({'PRICE': 'mean'}).sort_values("PRICE", ascending=True)
"""OUT:
                            PRICE
COUNTRY SOURCE  SEX    AGE       
deu     android male   26     9.0
usa     ios     female 38    19.0
tur     ios     male   47    19.0
        android male   21    19.0
fra     android male   18    19.0
                           ...
deu     ios     male   20    49.0
usa     ios     male   32    54.0
bra     android male   46    59.0
fra     android female 24    59.0
usa     android male   36    59.0

"""

# Turn the names in the index into variable names
agg_df=agg_df.reset_index()
"""
    COUNTRY   SOURCE     SEX  AGE  PRICE
0       deu  android    male   26    9.0
1       usa      ios  female   38   19.0
2       tur      ios    male   47   19.0
3       tur  android    male   21   19.0
4       fra  android    male   18   19.0
..      ...      ...     ...  ...    ...
343     deu      ios    male   20   49.0
344     usa      ios    male   32   54.0
345     bra  android    male   46   59.0
346     fra  android  female   24   59.0
347     usa  android    male   36   59.0
"""

# Make age variables a categorical variable.
bins = [0,19,24,31,41, agg_df["AGE"].max()]

labels = ["0_19","19_24","24_31","31_41","41_"+ str(agg_df["AGE"].max())]

# divide age
agg_df["age_cat"] = pd.cut(agg_df["AGE"],bins,labels = labels)
agg_df[agg_df["AGE"] == 24 ]
agg_df.head(20)

"""OUT:
  COUNTRY   SOURCE     SEX  AGE  PRICE age_cat
0     deu  android    male   26    9.0   24_31
1     usa      ios  female   38   19.0   31_41
2     tur      ios    male   47   19.0   41_66
3     tur  android    male   21   19.0   19_24
4     fra  android    male   18   19.0    0_19
"""

# How do we access the observation values?
for i in agg_df.values:
    print(i)

# Let's perform the operation in such a way that we select the observation values in the loop above
customer_level_based = [i[0].upper() + "_" + i[1].upper() + "_" + i[2].upper() + "_" + i[5].upper()for i in agg_df.values]

agg_df["customer_level_based"] = customer_level_based

agg_df.head()

# Let's remove the unnecessary variables
agg_df = agg_df[["customer_level_based","PRICE"]]
agg_df.head()

# For this reason, after groupby according to the segments, we should get the price averages and deduplicate the segments.
agg_df = agg_df.groupby("customer_level_based").agg({"PRICE": "mean"})
agg_df.head()

# customer_level_based  is in the  index. Let's turn that into a variable.
agg_df = agg_df.reset_index()

# Segment by PRICE,
# add segments to agg_df with the naming "SEGMENT",
# describe the segments,
agg_df["SEGMENT"] = pd.qcut(agg_df["PRICE"],4,labels = ["D","C","B","A"])
agg_df.groupby("SEGMENT").agg({"PRICE":["mean","max","sum"]})
"""
             PRICE                        
              mean        max          sum
SEGMENT                                   
D        29.475143  32.244811   795.828862
C        33.358556  34.071905   900.681010
B        34.839110  35.718409   940.655963
A        38.540430  43.375000  1040.591614
"""

# Analyze the C segment.
agg_df[agg_df["SEGMENT"] == "C"]

# Classify the new customers and estimate how much income they can bring.
# Which segment does a 33-year-old Turkish woman using ANDROID belong to and how much income is expected to earn on average?
new_user = "TUR_ANDROID_FEMALE_31_41"
agg_df[agg_df["customer_level_based"] == new_user]

 """OUT:
        customer_level_based  PRICE SEGMENT
72  TUR_ANDROID_FEMALE_31_41   43.0       A
"""

