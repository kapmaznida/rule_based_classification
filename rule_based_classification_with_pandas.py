################################ RULE BASED CLASSIFICATION WITH PANDAS ########################################
import pandas as pd

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


df.columns
df['SOURCE'].unique()
#array(['android', 'ios']
df['SOURCE'].nunique()
#2
df['SOURCE'].value_counts()
"""
android    2974
ios        2026
"""


df['PRICE'].value_counts()
"""
29    1305
39    1260
49    1031
19     992
59     212
"""

df['COUNTRY'].value_counts()
"""
usa    2065
bra    1496
deu     455
tur     451
fra     303
can     230
"""

df.groupby("COUNTRY").agg({"PRICE": "sum"})
"""
         PRICE
COUNTRY       
bra      51354
can       7730
deu      15485
fra      10177
tur      15689
usa      70225
"""

df.groupby('SOURCE')["PRICE"].count()
#or
df.groupby('SOURCE').agg({"PRICE": "count"})
""" 
          PRICE
SOURCE        
android   2974
ios       2026
"""

df.groupby('COUNTRY')['PRICE'].mean()
#or
df.groupby('COUNTRY').agg({"PRICE": "mean"})
"""
             PRICE
COUNTRY           
bra      34.327540
can      33.608696
deu      34.032967
fra      33.587459
tur      34.787140
usa      34.007264

"""

df.groupby('SOURCE')['PRICE'].mean()
#or
df.groupby('SOURCE').agg({"PRICE": "mean"})
"""
             PRICE
SOURCE            
android  34.174849
ios      34.069102
"""

df.groupby(by=["COUNTRY","SOURCE"])["PRICE"].mean()
"""
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

df.groupby(['COUNTRY','SOURCE','SEX','AGE']).agg({'PRICE': 'mean'})

"""
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

agg_df = df.groupby(by=['COUNTRY','SOURCE','SEX','AGE']).agg({'PRICE': 'mean'}).sort_values("PRICE", ascending=True)
"""
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

bins = [0,19,24,31,41, agg_df["AGE"].max()]

labels = ["0_19","19_24","24_31","31_41","41_"+ str(agg_df["AGE"].max())]

agg_df["age_cat"] = pd.cut(agg_df["AGE"],bins,labels = labels)
agg_df[agg_df["AGE"] == 24 ]
agg_df.head(20)

"""
  COUNTRY   SOURCE     SEX  AGE  PRICE age_cat
0     deu  android    male   26    9.0   24_31
1     usa      ios  female   38   19.0   31_41
2     tur      ios    male   47   19.0   41_66
3     tur  android    male   21   19.0   19_24
4     fra  android    male   18   19.0    0_19
"""

for i in agg_df.values:
    print(i)

customer_level_based = [i[0].upper() + "_" + i[1].upper() + "_" + i[2].upper() + "_" + i[5].upper()for i in agg_df.values]

agg_df["customer_level_based"] = customer_level_based

agg_df.head()

agg_df = agg_df[["customer_level_based","PRICE"]]
agg_df.head()

agg_df = agg_df.groupby("customer_level_based").agg({"PRICE": "mean"})
agg_df.head()

agg_df = agg_df.reset_index()

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
agg_df[agg_df["SEGMENT"] == "C"]

#######################################################################################################################
new_user = "TUR_ANDROID_FEMALE_31_41"
agg_df[agg_df["customer_level_based"] == new_user]
"""
        customer_level_based  PRICE SEGMENT
72  TUR_ANDROID_FEMALE_31_41   43.0       A
"""

