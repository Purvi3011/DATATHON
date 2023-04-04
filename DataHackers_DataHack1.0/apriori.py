import re
import pandas as pd
import streamlit as st

data = pd.read_csv("Apriori_Dataset_final.csv")

print("*****************")
data['antecedents'] = data['antecedents'].apply(lambda x:re.sub("frozenset", "", x))
data['antecedents'] = data['antecedents'].apply(lambda x:re.sub('[^0-9a-zA-Z]+', "", x))
data['consequents'] = data['consequents'].apply(lambda x:re.sub("frozenset", "", x))
data['consequents'] = data['consequents'].apply(lambda x:re.sub('[^0-9a-zA-Z]+', "", x))

data.sort_values(by=["confidence"], inplace = True, ascending=False)

unique_foods = list(set(list(data["antecedents"])))

st.title("Recommendations")

antecedent = st.selectbox("Your interest", unique_foods)
if st.button("Recommend"):
    # st.write(antecedent)
    new = data[data["antecedents"] == antecedent]
    # for i in list(new["consequents"])[:5]:
    #     st.write(i)
    # pass
    st.write(new.reset_index()[["consequents", "confidence"]])

# st.dataframe(data)