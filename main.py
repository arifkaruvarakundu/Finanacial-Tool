import streamlit as st
import pandas as pd
from financial_tool import extract_financial_data


col1,col2=st.columns([3,2])

finanacial_data_df = pd.DataFrame({
   "Measure": ["Company Name","Stock Symbol","Revenue","Net INcome","EPS"],
    "Value" : ["","","","",""]
})

with col1:
    st.title("Data Extraction Tool")
    news_article =st.text_area("Paste your financial news Articel here:",height=300)
    if st.button("Extract"):
        finanacial_data_df = extract_financial_data(news_article)

with col2:
    st.dataframe(finanacial_data_df)

    
