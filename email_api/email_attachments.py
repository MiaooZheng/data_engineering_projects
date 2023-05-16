import os 
from io import StringIO, BytesIO
import csv
import json
import re
import requests
from imap_tools import MailBox
from imap_tools import AND,OR,NOT
import pandas as pd 
from bs4 import BeautifulSoup

# the following class is based on imap-tools 
class ImapDetect:
    def _init_(self, email, app_password):
        # you can generate your app password in google settings.
        self.mailbox = MailBox("imap.gmail.com").login(email, app_password)

    def get_unprocessed_email_from(self, sender, label="processed"):
        msgs=[]
        unread_msgs = self.mailbox.fetch(AND(NOT(gamil_label = label), from_ = sender))
        for unread_msg in unread_msgs:
            msgs.append(unread_msg)
        return msgs

    def get_email_processing_attachment(self, msg):
        global att
        global msg_with_att_uid
        msg_with_att_uid =[]
        for att in msg.attachments:
            if att.filename.endwith(".csv", ".xlsx"):
                msg_with_att_uid.append(msg.uid)
            print(msg.subject, att.filename)
        return msg_with_att_uid

    def override_email_att_type(get_email_processing_attachment, msg):
        # This is because when we return email with attachments, it also has html.
        if msg_with_att_uid:
            print(msg_with_att_uid)
            return "attachment"
        elif "some important keywords" in msg.html:
            return "url" 

    def process_attachment(self, att):
        if ".csv" in att.filemame:
            csv_str = str(att.payload, "utf-8")
            data = StringIO(csv_str)
            df = pd.read_csv(data)
        elif ".xlsx" in att.filename:
            byte_data = BytesIO(att,payload)
            df = pd.read_excel(byte_data)
        df.dropna(how = "all", implace = True)
        return df 

    def proess_excel_with_hyperlink(self, df):
        # here i'll put fake url and fake headers
        # and we assume the link here will be redirected to the true url -> all links in excel file and true urls are different
        import time 
        hyperlink_col_list = df["link_unique_code"].to_list()
        print(len(hyperlink_col_list))
        data_from_link=[]
        for key_code in hyperlink_col_list:
            original_url = f"https://www.heyimfakelink/{key_code}"
            headers = {
                "Accept": "application/xhtml+xml",
                "Connection": "keep-alive",
                "Host": "fake_host",
                "User-Agent": "Mozilla/5.0 (<system-information>) <platform> (<platform-details>) <extensions>"
            }
            response = requests.get(url = original_url, headers = headers)
            print(response.status_code)
            redirect_url = response.history[0].headers['Location']
            headers = {"User-Agent": "Mozilla/5.0 (<system-information>) <platform> (<platform-details>) <extensions>"}
            response = requests.get(url = redirect_url, headers=headers)
            html = response.text 
            soup = BeautifulSoup(html, features="lxml")
            # in my case, i want to extract info under the follwing class and formart
            title = soup.find_all("td", {"class": "fake-title"})
            value = soup.find_all("td", {"class": "fake-value"})
            cols = []
            col_values =[]
            for col in title:
                cols.append(col.text.replace(":", ""))
            # print(cols)
            for val in value:
                col_values.append(val.text.replace("\n", ""))
            doc = {cols[i]: col_values[i] for i in range(len(cols))}
            data_from_link.append(doc)
            time.sleep(60) # avoid error 429 - too many requests
        return data_from_link
         
         
    def process_unique_code_from_html(self, msg):
        # this is the second case where we extract unique code from msg.html as the part of url and then call api to extract detail we want 
        global unique_code 
        mail_with_link_list =[]
        suffix =[]
        mail_with_link = msg.html
        soup = BeautifulSoup(str(mail_with_link), features = "lxml")
        for link in soup.findAll(
            "a", attrs={"href": re.compile("https://base_url/","")}
        ):
            mail_with_link_list.append(link.get("href"))
            url_without_duplicate = list(set(mail_with_link_list))
            for url in url_without_duplicate:
                code = url.replace("https://base_url/", "")
                suffix.append(code)
            unique_code = list(set(suffix))
            return unique_code 

        # Then we can call api -> this is the case we only have 1 url and use http post method and send code we generate before as body 
    def get_data_from_url(self):
        url = "https://api.xxxxxx"
        for code in unique_code:
            payload = json.dumps(
                {
                    "code": code,
                    "extra_data":[
                        {
                            "user-agent": "Mozilla/5.0 (<system-information>) <platform> (<platform-details>) <extensions>"
                        }
                    ]
                }
            )
            headers = {
                "Accept": "application/json",
                "Connection": "keep-alive",
            }
            response = requests.post(url = url, headers=headers, data = payload)
            return response.json()


email = os.getenv("email")
app_password = os.getenv("app_password")   
sender = os.getenv("sender_email")


client = ImapDetect(email, app_password)
# we'll only detect unprocessed email (emails without label "processed")
client.mailbox.folder.set("INBOX") 
if not client.mailbox.folder.exists("processed"):
    client.mailbox.folder.create("processed")

messages = client.get_unprocessed_email_from(sender)
for unprocessed_message in messages:
    processing_type = client.get_email_processing_attachment(unprocessed_message)
    processing_type = client.override_email_att_type(client.get_email_processing_attachment, unprocessed_message)
    if processing_type == "attachment":
        for uid in msg_with_att_uid:
            df = client.process_attachment(att)
            if "Condition 1" in unprocessed_message.subject: # this is for special case
                df = df.drop(columns = ["Column1", "Column2", "Column5"])
                df = df.rename(columns = {"original_name", "new_name"})
                json_file = df.to_json(orient="records", lines = True)
                original_df = json.loads(json_file)
                detail_from_web = client.proess_excel_with_hyperlink(df)
                for doc in detail_from_web:
                    # add new json col 
                    doc["send_date"] = unprocessed_message.date_str
                result = [{**original_df_, **detail_from_web_} for original_df_, detail_from_web_ in zip(original_df, detail_from_web)]
                for res in result:
                    with open(f"json_data_{unprocessed_message.uid}.json", "a") as fp:
                        json.dump(res, fp, indent=2, default=str)
            else:
                json_file = df.to_json(orient="records", lines = True)
                with open(f"json_data_{unprocessed_message.uid}.json", "a") as fp:
                        json.dump(json_file, fp, indent=2, default=str)
    elif processing_type == "url":
        if "keyword in sender1's message" in unprocessed_message.html:
            unique_code = client.process_unique_code_from_html(unprocessed_message)
            if unique_code:
                json_file = client.get_data_from_url()
                for doc in json_file:
                    with open(f"json_data_{unprocessed_message.uid}.json", "a") as fp:
                        json.dump(doc, fp, indent=2, default=str)
        



        
