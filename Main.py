import GmailAPI as ml
import FileManagement as fl
import EmailAssistant as astn
import json
import os

def main():
  labels = ['INBOX'] # this line specifies the label of the emails to be read
  state = "is:unread" # this line specifies the state of the emails to be read
  emails = ml.getEmails(labels, state)
  
  if not emails:
    print("No emails found.")
  else:
    for email in emails:
      message = email.pop('Message')
    # Save the email message as an html file
      with open(str(email['MessageID'])+'.html', 'w', encoding='utf-8') as file:
        file.write(message)
        print("Email saved as " + str(email['MessageID']) + ".html")
        #save the file link in the email data
        email['MessageFile'] = os.getcwd() + "\\" +str(email['MessageID']) + ".html"
      # generate prompts for wach email, get output and save it in a new df to later safe to excel
      prompt = astn.gen_prompt(message)
      response = astn.generate(prompt)
      # print(response)
      json_string = response.split("json")[1]
      # Remove any leading or trailing whitespace
      json_string = json_string.strip()[:-3]
      # save the response in a new file with same message id summary as name and .txt extension
      filename = str(email['MessageID']) + "_summary.txt"
      with open(filename, 'w', encoding='utf-8') as file:
        file.write(json_string)
        print("Summary saved as " + filename)
        email['SummaryFile'] = os.getcwd() + "\\" + filename 
      
      # Parse the JSON string into a dictionary
      print(json_string)
      try:
        res = json.loads(json_string)
        # email['Filtered_Message'] = res['Filtered_Message']
        email['Summary'] = res['Summary']
        email['Category'] = res['Category'] 
      except:
        print("Error in processing response.") 
    # save the rest of the emails data in a text file
    fl.save_to_excel(emails, "emails.xlsx")
    print("Email data saved in emails.xlsx.")

if __name__ == "__main__":
  main()