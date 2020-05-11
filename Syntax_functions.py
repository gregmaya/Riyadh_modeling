import geopandas as gpd
import pandas as pd
from numpy import log

def Syntax_normalizer(df):
    """
    This function returns normalised Choice and Integration values based on Space Syntax literature.
    
    NaCH = logCH+1/logTD+3
    NaIN =  NC^1.2/TD
    
    """
    #extracting the useful columns
    useful_cols = [i[6:] for i in df.columns if (i[:5]=="T1024")]
    
    #extracting the radii that need to be calculated
    radii = [int(r.split()[1][1:]) for r in useful_cols if r[:6]=="Choice"]

    #creating the column names
    NaCh_colnames = ["NaCh_"+str(r) for r in radii]
    NaIn_colnames = ["NaIn_"+str(r) for r in radii]
    
    # empty dictionary to store all calculation with their keys
    normalized_dct = {}
    for rad, NaCh_col_name, NaIn_col_name in zip(radii, NaCh_colnames, NaIn_colnames):
        #slice the dataframe with relevant columns
        choice = df["T1024 Choice R%s metric" % str(rad)]
        tdepth = df["T1024 Total Depth R%s metric" % str(rad)]
        ncount = df["T1024 Node Count R%s metric" % str(rad)]

        NaCh_vals = log(choice+1) / log(tdepth+3)
        NaIn_vals = ncount**1.2 / tdepth

        normalized_dct[NaCh_col_name] = NaCh_vals
        normalized_dct[NaIn_col_name] = NaIn_vals
    
    #convert dictionary to dataframe 
    newdf = pd.DataFrame(normalized_dct)
    #join the new dataframe with the input DataFrame (based on index)
    df = df.join(newdf)
    
    print("The following columns have been added successfully:\n",NaCh_colnames,"\n",NaIn_colnames,"\n")
    return df