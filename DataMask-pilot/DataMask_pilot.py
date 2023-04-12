import os
import hashlib
import pandas as pd
import streamlit as st
import math
import urllib.parse
import time
from functools import wraps
import re
from base64 import b64encode
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from azure.storage.blob import (
    BlobServiceClient,
    BlobClient,
    ContainerClient,
    generate_blob_sas,
    BlobSasPermissions,
)
import urllib
import datetime
import os
import os
from dotenv import load_dotenv
from DataMask_pilot.py import main, server

AZURE_CONNECTION_STRING = os.environ["AZURE_CONNECTION_STRING"]
STORAGE_ACCOUNT_KEY = os.environ["STORAGE_ACCOUNT_KEY"]
AZURE_CONTAINER_NAME = os.environ["AZURE_CONTAINER_NAME"]
STORAGE_ACCOUNT_NAME = os.environ["STORAGE_ACCOUNT_NAME"]

SENDGRID_API_KEY = os.environ["SENDGRID_API_KEY"]
SENDER_EMAIL = os.environ["SENDER_EMAIL"]
RECIPIENT_EMAIL = os.environ["RECIPIENT_EMAIL"]

USERNAME = os.environ["APP_USERNAME"]
PASSWORD = os.environ["APP_PASSWORD"]



# Configure authentication
USERNAME = "pharma1"
PASSWORD = "Parolamea123$"

# Add this function to hide the "Made with Streamlit" footer
def hide_streamlit_footer():
    hide_footer_style = """
    <style>
    .reportview-container .main .block-container { 
        padding-bottom: 5rem;
    }
    footer { 
        visibility: hidden;
    }
    </style>
    """
    st.markdown(hide_footer_style, unsafe_allow_html=True)

def validate_csv(df):
    errors = []

def validate_csv(df):
    errors = []

    # Example validation: check if values in 'Age' column are numeric
    for index, value in enumerate(df['Age']):
        numeric_value = pd.to_numeric(value, errors='coerce')
        if math.isnan(numeric_value):
            errors.append(f"Line {index + 1}, 'Age' column - value is not numeric.")

    return errors

def anonymize_column(df, columns_to_anonymize):
    for column_name in columns_to_anonymize:
        df[column_name] = df[column_name].apply(lambda x: hashlib.sha256((str(x) + str(x).zfill(10)).encode("utf-8")).hexdigest())
    return df

def upload_to_azure_and_generate_url(file_name):
    blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
    container_client = blob_service_client.get_container_client(AZURE_CONTAINER_NAME)

    # Add a timestamp to the end of the file name in case it already exists in the container
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    while container_client.get_blob_client(f"{timestamp}_{file_name}").exists():
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name_with_timestamp = f"{timestamp}_{file_name}"
    
    blob_client = container_client.get_blob_client(file_name_with_timestamp)

    with open(file_name, "rb") as data:
        blob_client.upload_blob(data)

    sas_token = generate_blob_sas(
        account_name=STORAGE_ACCOUNT_NAME,
        account_key=STORAGE_ACCOUNT_KEY,
        container_name=AZURE_CONTAINER_NAME,
        blob_name=file_name_with_timestamp,
        permission=BlobSasPermissions(read=True),
        start=datetime.datetime.utcnow(),
        expiry=datetime.datetime.utcnow() + datetime.timedelta(days=365 * 10),
        cache_control="no-cache",
        content_disposition=f"attachment; filename={file_name_with_timestamp}",
        content_encoding=None,
        content_language=None,
        content_type=None,
    )

    encoded_file_name = urllib.parse.quote(file_name_with_timestamp)
    return (
        f"https://{blob_service_client.account_name}.blob.core.windows.net/"
        f"{container_client.container_name}/{encoded_file_name}?{sas_token}"
    )

def send_email_notification(file_name, download_url):
    message = Mail(
        from_email=SENDER_EMAIL,
        to_emails=RECIPIENT_EMAIL,
        subject="Anonymized CSV file available",
        html_content=f"The anonymized CSV file '{file_name}' is ready for download. <a href='{download_url}'>Download the file here</a>."
    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        return response.status_code == 202
    except Exception as e:
        print(e)
        return False



def handle_exceptions(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            st.error(f"There is no column {str(e)} in the file. Please make sure the file is valid and upload it again..")
            return None
    return wrapped


def get_csv_download_link(csv_name):
    with open(csv_name, 'rb') as f:
        csv_bytes = f.read()
    b64 = b64encode(csv_bytes).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{csv_name}" target="_blank">Click here to download your anonymized copy.</a>'
    return href

@handle_exceptions
def main():
    st.set_page_config(page_title="Authentication", page_icon="??")
    hide_streamlit_footer()  

    if "is_logged_in" not in st.session_state:
        st.session_state.is_logged_in = False

    if st.session_state.is_logged_in:
        st.title("CSV Anonymization and Validation")
        
        uploaded_file = st.file_uploader("Upload your CSV file", type="csv")

        if uploaded_file is not None:
            file_details = {
                "FileName": uploaded_file.name,
                "FileType": uploaded_file.type,
                "FileSize": uploaded_file.size,
            }
            st.write(file_details)

            df = pd.read_csv(uploaded_file)

            st.write("Preview of uploaded data:")
            st.dataframe(df.head())

            # Validate data
            errors = validate_csv(df)
            if errors:
                st.write("The following errors were found in the CSV file:")
                for error in errors:
                    st.write(f"- {error}")
            else:
                columns_to_anonymize = st.multiselect("Select the columns to anonymize", df.columns)

                if st.button("Submit"):
                    # Anonymize the selected columns
                    anonymized_df = anonymize_column(df, columns_to_anonymize)

                    # Save the anonymized DataFrame as a .csv file
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    output_file_name = f"anonymized_{uploaded_file.name.split('.')[0]}_{timestamp}.csv"
                    anonymized_df.to_csv(output_file_name, index=False)

                    # Upload the file to Azure Blob Storage and generate a download URL
                    download_url = upload_to_azure_and_generate_url(output_file_name)

                    # Send an email notification
                    if send_email_notification(output_file_name, download_url):
                        st.success("The anonymized file was successfully sent.")
                        st.markdown(get_csv_download_link(output_file_name), unsafe_allow_html=True)
                    else:
                        st.error("Error sending the notification email.")
    else:
        st.title("Authentication")

        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")

            submitted = st.form_submit_button("Log in")
            if submitted:
                if username == USERNAME and password == PASSWORD:
                    st.session_state.is_logged_in = True
                    st.experimental_rerun()
                else:
                    st.error("Authentication failed!")


if __name__ == "__main__":
    load_dotenv(".env.production")
    main()
