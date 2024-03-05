import json
from datetime import date
import streamlit as st
import requests
import pandas as pd
from streamlit_oauth import OAuth2Component
from src.utils.utils import *

with open('src/config/client_secret.json') as f:
   client_secrets = json.load(f)

   # Set the client ID and client secret
   CLIENT_ID = client_secrets['web']['client_id']
   CLIENT_SECRET = client_secrets['web']['client_secret']
   AUTHORIZE_URL = client_secrets['web']['auth_uri']
   TOKEN_URL = client_secrets['web']['token_uri']
# Define the scopes required for your app
SCOPE = 'openid email profile'

# Define the redirect URL after successful authentication
REDIRECT_URI = 'http://localhost:8501'




st.title("Basement Inventory App")

# Create OAuth2Component instance
oauth2 = OAuth2Component(CLIENT_ID, CLIENT_SECRET, AUTHORIZE_URL, TOKEN_URL,)



# Check if token exists in session state
if 'token' not in st.session_state:
    # If not, show authorize button
    result = oauth2.authorize_button("Google Login", REDIRECT_URI, SCOPE)
    if result and 'token' in result:
        # If authorization successful, save token in session state
        st.session_state.token = result.get('token')
        
else:
    # If token exists in session state, show the token
    token = st.session_state['token']
    st.json(token)
    if st.button("Refresh Token"):
        # If refresh token button is clicked, refresh the token
        token = oauth2.refresh_token(token)
        st.session_state.token = token
    id_token = token['id_token']
    email = extract_email_from_id_token(id_token)
    headers = {"Email": email}
    st.write(email)
    choice = st.selectbox(
        "What operation do you want to run?",
        ("Choose action",
        "Get all",
        "Get by name",
        "Put",
        "Post",
        "Delete"))
    if choice == "Get all":
        try:
            response = requests.get("http://localhost:8000/items", timeout=10, headers=headers)
            data = response.json()
            df = pd.DataFrame(data)
            df.set_index('id', inplace=True)
            df['expiry_date'] = pd.to_datetime(df["expiry_date"])
            st.write(df.sort_values('expiry_date')
                    .style.applymap(expired_column_color, subset=['expiry_date']))

        except requests.exceptions.Timeout:
            st.error('Timed out')
        
    if choice == "Get by name":
        item_name = st.text_input(label='Enter Item Name', value='Item Name')
        if st.button("Get Item"):
            try:
                response = requests.get(f"http://localhost:8000/item/{item_name}", timeout=10)
            

                if response.status_code == 200:
                    data = response.json()
                    df = pd.DataFrame(data)
                    st.write(df)
                else:
                    st.error(
                        f"Failed to fetch Item with id {item_name}. Status code: {response.status_code}")
            
            except requests.exceptions.Timeout:
                st.error('Timed out')


    if choice == "Post":
        inputs = {
            "item_name": st.text_input(
                label='item_name'),
            "quantity": st.number_input(
                label='quantity',
                value=1),
            "description": st.text_input(
                label='description',
                value='some description'),
            "price": st.number_input(
                label='price',
                value=0),
            "expiry_date": st.date_input(
                label='expiration date',
                format="MM.DD.YYYY").strftime("%Y-%m-%d"),
            "tag": st.text_input(
                label='tag')
            }
        
        if st.button("Add Item"):
            try:   
                response = requests.post("http://localhost:8000/item/", json=inputs, timeout=10)
                st.write(response)  # if response.status_code == 200
            except requests.exceptions.Timeout:
                st.error('Timed out')
            

    if choice == "Delete":
        item_id = st.number_input(label="Enter product id")

        if st.button('Delete now product'):
            # Properly format the URL
            try:
                url = f"http://localhost:8000/item/{item_id}"
                response = requests.delete(url)
                if response == 200:
                    data = response.json
                    st.write(data)
                else:
                    st.error(response.status_code)
            except requests.exceptions.Timeout:
                st.error('Timed out')