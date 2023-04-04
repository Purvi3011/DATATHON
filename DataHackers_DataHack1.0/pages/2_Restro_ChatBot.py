import streamlit as st
st.set_page_config(layout="wide")

import re
import pandas as pd
import datetime as dt

import numpy as np
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders
import smtplib

print("***************************")

def sendmail(receiver,c_name):
    msg = MIMEMultipart()
    msg['From'] = "vartakdyuti@gmail.com" 
    password= "bemk xums wakw hwbw"
    msg['To']= receiver
    msg['Subject'] = 'Discount Coupon'

    msg.attach(MIMEText(f"""
    <p>We hope this message finds you well! As a token of appreciation for your continued support.
    We would like to offer you a free coupon that you can redeem on your next purchase with us.
    
    <br><br>This coupon will give you a discount of 20% off your total purchase. 
    Simply enter the coupon code CUST20 at checkout to apply the discount. 
    
    <br/><br/>We value your loyalty and look forward to continuing to serve you. 
    Thank you for choosing us as your preferred snack provider.

    <br><br>Thanking you in anticipation,
    <br>Best Regards,
    <br>Data Hackers</p>""", 'html'))
    
    # open the file to be sent  
    filename = "Coupon.pdf"
    attachment = open("./" + filename, "rb") 

    # instance of MIMEBase and named as p 
    p = MIMEBase('application', 'octet-stream') 

    # To change the payload into encoded form 
    p.set_payload((attachment).read()) 

    # encode into base64 
    encoders.encode_base64(p) 

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 

    # attach the instance 'p' to instance 'msg' 
    msg.attach(p) 

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(msg['From'],password)
    s.sendmail(msg['From'],msg['To'],msg.as_string())
    s.quit()


data = pd.read_csv("data.csv")
# data['date'] = pd.to_datetime(data['date'])
# print(data.head())
data['year'] = pd.DatetimeIndex(data['date']).year
data['month'] = pd.DatetimeIndex(data['date']).month
# print(data.info())
by_year = list(data.groupby(['year'])['price'].sum())
# print(by_year)
by_month = list(data.groupby(['month'])['price'].sum())
# print(by_month)
months = ['January', 'February', 'March', 'April', 'May', 'June', 
          'July', 'August', 'September', 'October', 'November','December']

ap_data = pd.read_csv("Apriori_Dataset_final.csv")
ap_data['antecedents'] = ap_data['antecedents'].apply(lambda x:re.sub("frozenset", "", x))
ap_data['antecedents'] = ap_data['antecedents'].apply(lambda x:re.sub('[^0-9a-zA-Z]+', "", x))
ap_data['consequents'] = ap_data['consequents'].apply(lambda x:re.sub("frozenset", "", x))
ap_data['consequents'] = ap_data['consequents'].apply(lambda x:re.sub('[^0-9a-zA-Z]+', "", x))

ap_data.sort_values(by=["confidence"], inplace = True, ascending=False)

st.title("Restro Bot")
question = st.text_input("", placeholder="Type your question here..")
if st.button("Ask"):
    if question == "":
        st.write("Please enter a question")
    
    elif question == "What are yearly sales?":
        # st.write(question)
        annual_sales = {}
        for i in range(len(by_year)):
            annual_sales[f'{2021+i}'] = round(by_year[i])

        df = pd.DataFrame(annual_sales, index=[0])
        st.dataframe(df)
    
    elif question == "What are monthly sales?":

        monthly_sales = {}
        for i in range(len(by_month)):
            monthly_sales[months[i]] = round(by_month[i])

        df = pd.DataFrame(monthly_sales, index=[0])
        st.dataframe(df)
        # st.line_chart(df.transpose())
    
    elif question == "What are quarterly sales?":
        quarterly_sales = pd.DataFrame()
        quarterly_sales["Q1"] = [round(by_month[0]+by_month[1]+by_month[2]+by_month[3])]
        quarterly_sales["Q2"] = [round(by_month[4]+by_month[5]+by_month[6]+by_month[7])]
        quarterly_sales["Q3"] = [round(by_month[8]+by_month[9]+by_month[10]+by_month[11])]
        
        df = pd.DataFrame(quarterly_sales, index=[0])
        st.dataframe(df)

    elif question == "Give a list of most active customers":
        data5 = data.groupby('client_id')['order_id'].apply(list).reset_index(name="order_id")
        data5['Values'] = data5['order_id'].apply(lambda x: len(x))
        data5.sort_values(by='Values',inplace=True,ascending=False)
        data5 = data5.reset_index()
        st.dataframe(data5[["client_id", "Values"]].iloc[:5, :])
        # for i in range(10):
            # st.write(data5['client_id'][i])
    
    elif question == "Give a list of least active customers":
        data5 = data.groupby('client_id')['order_id'].apply(list).reset_index(name="order_id")
        data5['Values'] = data5['order_id'].apply(lambda x: len(x))
        data5.sort_values(by='Values',inplace=True,ascending=True)
        emails = ["sample1email456@gmail.com", "pushkarwaykole123@gmail.com", "lodayaumang71@gmail.com", "purviparmar3011@gmail.com",
                  "vartakdyuti@gmail.com"]
        for i in range(5):
            sendmail(emails[i],'Customer')
        
        for i in range(5):
            st.write(data5['client_id'][i])
    
    elif question == "List frequently ordered items":
        st.write(data['item_name'].value_counts(ascending=False).to_frame().iloc[:5, :])
    
    elif question == "What are the frequently bought food combos?":
        new = ap_data.reset_index()
        new = new[["consequents", "antecedents"]]
        new.columns = ["Item 1", "Item 2"]
        st.write(new.iloc[:5, :])
    
    elif question == "How to increase my profit?":
        st.write("There are several strategies that a restaurant owner can use to increase profits. Some of these include:")
        st.write("1. Optimizing the menu: Assessing the menu to ensure every item is bringing profits to the restaurant. Focus more on items that build your margins and remove those draining profits")
        st.write("2. Cashing in on customer preferences: Analyzing customers' orders, inquiries and recommendations should unlock fresh ideas for your restaurant's menu")
        st.write("3. Partnering with a food delivery service: Restaurant owners can increase sales by partnering with third-party delivery platforms")
        st.write("4. Using technology: Incorporating modern systems into your restaurant business will increase your profits dramatically")
        st.write("5. Marketing your restaurant: Promoting your restaurant through various marketing channels can help attract more customers")
        
    else:
        st.write("Poor internet connection!")
