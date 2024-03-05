from datetime import date
import jwt
import pandas as pd
def expired_column_color(val: date):
    """
    Attributes color to df cells

    Args:
        val (date): datetime

    Returns:
        string: color
    """
    today = pd.to_datetime(date.today())
    red_time = val - today
    if red_time.days < 30:
        color = 'red'
    elif red_time.days < 60:
        color = 'blue'
    else:
        color = 'green'
    return f'color:{color}'


def extract_email_from_id_token(id_token):
    decoded_token = jwt.decode(id_token, options={"verify_signature" : False})
    email = decoded_token["email"]

    return email
    
