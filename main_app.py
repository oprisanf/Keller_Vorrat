import streamlit as st
import requests
import pandas as pd
import json
from datetime import date, timedelta


st.title("Basement Inventory App")


# Store the initial value of widgets in session state
if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False



def expired_column_color(val: date):
    today = pd.to_datetime(date.today())
    red_time = val-today
    if red_time.days<30:
        color = 'red'  
    elif red_time.days< 60:
         color = 'blue' 
    else:
        color = 'green'
    return f'color:{color}'

choice = st.selectbox("What operation do you want to run?",
                      ("Choose action","Gett all","Get by name", "Put","Post","Delete"))

if choice == "Get all":
    response = requests.get("http://fastapi_service:8000/items")
    data = response.json()
    df = pd.DataFrame(data)
    df.set_index('id',inplace=True)
    df['expiry_date'] = pd.to_datetime(df["expiry_date"])
    st.write(df.sort_values('expiry_date')
             .style.applymap(expired_column_color,subset=['expiry_date']))

if choice == "Get by name":
    item_name = st.text_input(label='Enter Item Name', value='Item Name')
    if st.button("Get Item"):
        response = requests.get(f"http://fastapi_service:8000/item/{item_name}")
        
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data)
            st.write(df)
        else:
            st.error(f"Failed to fetch Item with id {item_name}. Status code: {response.status_code}"
                     )

if choice == "Post":
    inputs = {
        "item_name": st.text_input(label='item_name'),
        "quantity": st.number_input(label='quantity',value=1),
        "description": st.text_input(label='description', value='some description'),
        "price": st.number_input(label='price', value=0),
        "expiry_date": st.date_input(label='expiration date', format="MM.DD.YYYY").strftime("%Y-%m-%d"),
        "tag": st.text_input(label='tag')
    }
    if st.button("Add Item"):
        response = requests.post("http://fastapi_service:8000/item/", json=inputs)
                
        st.write(response)# if response.status_code == 200 
        
if choice == "Delete":
    item_id = st.number_input(label="Enter product id")
    if st.button('Delete now product'):
        url = f"http://fastapi_service:8000/item/{item_id}"  # Properly format the URL
        response = requests.delete(url)            
        if response == 200:
            data = response.json
            st.write(data)
        else:
            st.error(response.status_code)



