from time import *
from bs4 import BeautifulSoup
import requests
from requests.exceptions import RequestException
#from reports.reports import *
from lxml import html
import tkinter as tk
from tkinter import ttk
from tkinter import *
import os


scrape_session_memory = []


directory = os.getcwd()


t = time()




def robots_report(title,request_code,request_reason,page_contents):
    with open(f"{title} robots.txt","w") as file:
        file.write(f"DOCUMENT TITLE = {title} robots.txt report\n\n")
        file.write(f"REQUEST CODE = {request_code}\n\n")
        file.write(f"REQUEST REASON = {request_reason}\n\n")
        file.write(f"\n\n*  *  *  *  *  *\n\nCODE RETRIEVED:\n\n*  *  *  *  *  *\n\n\n\n")
        file.write(f"\n\n{page_contents}\n\n")
        file.write(f"\n\n*  *  *  *  *  *\n\nEND OF DOCUMENT.\n\n*  *  *  *  *  *")




def scrape_report(title,request_code,request_reason,page_contents):
    with open(f"{title} scrape report.txt","w") as file:
        file.write(f"DOCUMENT TITLE = {title} web scraping session report\n\n")
        file.write(f"REQUEST CODE = {request_code}\n\n")
        file.write(f"REQUEST REASON = {request_reason}\n\n")
        file.write(f"\n\n*  *  *  *  *  *\n\nCODE RETRIEVED:\n\n*  *  *  *  *  *\n\n\n\n")
        file.write(f"\n\n{page_contents}\n\n")
        file.write(f"\n\n\n\n*  *  *  *  *  *\n\nEND OF DOCUMENT.\n\n*  *  *  *  *  *")




def display_message(x):

	try:
		status_message.delete(0,END)
		x_convert=str(x)
		status_message.insert(0,f"{x_convert}")

	except:
		status_message.insert(0,"Error: status message unavailable.")




def robots():

	try:

		url = str(base_url_entry.get())
		url_digest = url.split("/")

		session = requests.Session()
		site = session.get(f"{url}robots.txt",timeout=10)

		status_code = site.status_code
		status_reason = site.reason

		data = site.text
		convert = BeautifulSoup(data, features='lxml')
		search = convert.find_all
		result = str(search)

		try:
			robots_report(time(),status_code,status_reason,result)
			display_message(f"Success:  {url} robots.txt report created in current directory.")

		except:
			display_message(f"Error:  could not generate {url} robots.txt report.")

		try:
			session.close()

		except:
			display_message(f"Web session error:  exiting program.")
			quit()

	except requests.ConnectionError as e:
		display_message(f"Connection Error:  {url} robots.txt not found.")

	except requests.Timeout as e:
		display_message(f"Timeout Error:  {url} robots.txt not found.")

	except requests.RequestException as e:
		display_message(f"Unspecified Error:  {url} robots.txt not found.")




def scrape_page():

	try:

		url = str(webpage_entry.get())
		scrape_html = str(html_entry.get())
		scrape_class = str(class_entry.get())

		session = requests.Session()
		site = session.get(f"{url}",timeout=60)

		status_code = site.status_code
		status_reason = site.reason

		data = site.text
		convert = BeautifulSoup(data, features='lxml')
		search = convert.find_all(f"{scrape_html}",class_=f"{scrape_class}")
		result = list(search)

		for item in enumerate(result):
			scrape_session_memory.append(item)
			print(item)

		try:
			scrape_report(f"{time()}",status_code,status_reason,str_mem)
			display_message(f"Success:  {url} html + class report created in directory.")

		except:
			display_message(f"Error:  could not generate {url} scrape report.")

		try:
			session.close()
			display_message(f"Success:	web session successfully closed.")

		except:
			display_message(f"Connection Error:  Unable to close web session.")

		try:
			scrape_session_memory.clear()

		except:
			display_message(f"Memory Error:  please exit program.")

	except requests.ConnectionError as e:
		display_message(f"Connection Error:  {url} not found.")

	except requests.Timeout as e:
		display_message(f"Timeout Error:  {url} not found.")

	except requests.RequestException as e:
		display_message(f"Unspecified Error:  {url} not found.")




def close():
	quit()




def reset():

	try:

		robots_txt_entry.delete(0,END)
		robots_txt_entry.insert(0,"")
		webpage_entry.delete(0,END)
		webpage_entry.insert(0,"")
		html_entry.delete(0,END)
		html_entry.insert(0,"")
		class_entry.delete(0,END)
		class_entry.insert(0,"")
		status_message.delete(0,END)
		status_message.insert(0,"")

	except:

		display_message("Error:  could not clear widget contents.")




root = Tk()
root.wm_title("Distributed Financial Systems   |   Wishing Well")
root.geometry("600x250")
root.resizable(False,False)

set_cwd_entry = Entry(root)
set_cwd_entry.place(x=100,y=20,width=475)
set_cwd_entry.insert(0,f"{directory}")
set_cwd_label = Label(root,text="directory",fg="Blue")
set_cwd_label.place(x=20,y=20)

base_url_entry = Entry(root)
base_url_entry.place(x=100,y=60,width=475)
base_url_entry.insert(0,"https://example.com/")

base_url_label = Label(root,text="base URL",fg="Blue")
base_url_label.place(x=20,y=60)

webpage_entry = Entry(root)
webpage_entry.place(x=100,y=100,width=475)
webpage_entry.insert(0,"https://example.com/specific-page/within-website")

webpage_label = Label(root,text="target page",fg="Blue")
webpage_label.place(x=20,y=100)

html_entry = Entry(root)
html_entry.place(x=100,y=140,width=60)
html_label = Label(root,text="HTML",fg="Blue")
html_label.place(x=20,y=140)

class_entry = Entry(root)
class_entry.place(x=220,y=140,width=120)
class_label = Label(root,text="Class",fg="Blue")
class_label.place(x=170,y=140)

status_message = Entry(root)
status_message.place(x=20,y=205,width=540)

menu = Menu(root)
root.config(menu=menu)

file_menu = Menu(menu)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Close", command=close)
file_menu.add_command(label="Reset",command=reset)

base_url_menu = Menu(menu)
menu.add_cascade(label="base URL", menu=base_url_menu)
base_url_menu.add_command(label="robots.txt",command=robots)

target_page_menu = Menu(menu)
menu.add_cascade(label="target page", menu=target_page_menu)
target_page_menu.add_command(label="HTML and class",command=scrape_page)




if __name__ == "__main__":
	root.mainloop()
