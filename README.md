#LEVEL BASED PERSONA IDENTIFICATION, SIMPLE SEGMENTATION, and RULE-BASED CLASSIFICATION

# Project Purpose:
# - Thinking about the concept of persona.
# - LEVEL BASED PERSONA DEFINITION: To be able to define new customers according to category levels (Level).
# - SIMPLE SEGMENTATION: Simply segment new customer definitions using the qcut function.
# - RULE-BASED CLASSIFICATION: When a new customer arrives, to classify this customer by segments.

################# Before #####################

# PRICE SOURCE SEX COUNTRY AGE
# 0 39 android male bra 17
#1 39 android male bra 17
#2 49 android male bra 17
# 3 29 android male tour 17
# 4 49 android male tur 17

################# After #####################

# customers_level_based PRICE SEGMENT
# 0 BRA_ANDROID_FEMALE_0_18 1139.800000 A
#1 BRA_ANDROID_FEMALE_19_23 1070.60000 A
#2 BRA_ANDROID_FEMALE_24_30 508.142857 A
# 3 BRA_ANDROID_FEMALE_31_40 233.166667 C
# 4 BRA_ANDROID_FEMALE_41_66 236.666667 C

############################################
#Variables
#PRICE – Customer's spending amount
#SOURCE – The type of device the customer is connecting to
#SEX – Gender of the client
#COUNTRY – Customer's country
#AGE – Age of the customer
