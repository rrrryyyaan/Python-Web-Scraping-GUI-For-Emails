
import re
import requests
import webbrowser
import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
from googlesearch import search

google_url = "https://www.google.com/search?q="
method_labels = [("Gsearch", "Opens a google search for each input based on input+keyword query."), ("Gpage", "Opens google's top result automatically for each input based on input+keyword query."), ("Gscrape", "Scrapes the webpage(s) found with Gpage for emails. Displays emails in 'Results'.")]
current_method = method_labels[0][0]
current_desc = method_labels[0][1]


def handle_button(method):
  """ Switches the current method """
  global current_method
  global current_desc
  current_method = method_labels[method][0]
  current_desc = method_labels[method][1]

  #Update the label showing which method is in use
  method_title.configure(text="Select a method: Current - "+ current_method)


def handle_submit(input_query):
  """ Submit button functionality """
  input_query = [x.strip() for x in input_query.split(',')]
  if input_query[0] != "":
    if current_method == "Gsearch":
      g_search(input_query)
    elif current_method == "Gpage":
      g_page(input_query)
    elif current_method == "Gscrape":
      g_scrape(input_query)
    else:
      messagebox.showerror("Error!", "Please select a method!")
  else:
    messagebox.showerror("Error!", "Please input a school name!")


def clear():
  """ Clears all input and result text """
  schools_entry.delete(1.0, 'end')
  result_display.delete(1.0, 'end')


def clear_results():
  """ Clears the results only """
  result_display.delete(1.0, 'end')


def export(quick):
  """ Exports the content from result_display """
  results = str(result_display.get(1.0, 'end'))
  if len(results) == 1:
    messagebox.showerror("Error!", "Results are empty! Did you click 'Submit'?")
    return
  if quick:
    f = open("ScrapedOutput.txt", "a")
    f.write(results)
    f.close()
    messagebox.showinfo("Success!", "Results have been exported to 'ScrapedOutput.txt'\nin your current directory!")
  else:
    f = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
    if f is None:
        return
    f.write(results)
    f.close()


def g_search(input_query):
  """ Opens a google search based on your input """
  clear_results()
  result_display.insert(1.0, "Opening google searches based on input + keywords.")
  for i in range(len(input_query)):
   search_query = input_query[i] + " " + keyword_entry.get()
   for i in search(query=search_query,tld='co.in',lang='en',num=1,stop=1,pause=2):
     webbrowser.open("https://google.com/search?q=%s" % search_query)


def g_page(input_query):
  """ Opens the first google search result webpage based on your input """
  clear_results()
  result_display.insert(1.0, "Opening webpages based on input + keywords.")
  for i in range(len(input_query)):
    search_query = input_query[i] + " " + keyword_entry.get()
    for i in search(query=search_query,tld='co.in',lang='en',num=1,stop=1,pause=2):
      webbrowser.open(i)


def g_scrape(input_query):
  """ Opens the first google search result webpage based on your input then gathers emails """
  clear_results()
  for index in range(len(input_query)):
    search_query = input_query[index] + " " + keyword_entry.get()
    for i in search(query=search_query,tld='co.in',lang='en',num=1,stop=1,pause=2):
      url = i
      try:
        emails = set()
        response = requests.get(url)
        new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text, re.I))
        emails.update(new_emails)
        result_display.insert('end', "Emails for "+ input_query[index] + ":\n")
        for j in emails:
          result_display.insert('end', "" + j + "\n")
        result_display.insert('end', "\n")
      except:
        result_display.insert('end', "Webpage error for "+ input_query[index] +"! Please try again with different keywords\n")


if __name__ == "__main__":
  input_query = ""

  window = tk.Tk()
  window.title("Email Scraper - Scrape emails from webpages based on your input + keywords")

  #Start initializing widgets
  step1_label = tk.Label(window, text="Step One >", font=("Arial", 14), justify="left")
  step2_label = tk.Label(window, text="Step Two >", font=("Arial", 14), justify="left")
  step3_label = tk.Label(window, text="Step Three >", font=("Arial", 14), justify="left")
  step4_label = tk.Label(window, text="Step Four >", font=("Arial", 14), justify="left")
  step5_label = tk.Label(window, text="Step Five >", font=("Arial", 14), justify="left")

  title_frame = tk.Frame(window, highlightbackground="black", highlightcolor="black", highlightthickness=1)
  title_title = tk.Label(title_frame, text="Welcome to Email Scraper!", font=("Arial", 14), justify="center")
  title_desc = tk.Label(title_frame, text="This tool utilizes Google to easily find/collect emails from webpages. Each method performs a google search of your input + keywords provided in Step Two and Three and utlizes this information based on method selected.", font=("Arial", 9), wraplength=750, justify="center")

  method_frame = tk.Frame(window, highlightbackground="black", highlightcolor="black", highlightthickness=1)
  method_title = tk.Label(method_frame, text="Select a method: Current - "+ current_method, font=("Arial", 12), justify="left")
  Gsearch_button = tk.Button(method_frame, text="Gsearch", bd=3, width=10, command= lambda: handle_button(0))
  Gpage_button = tk.Button(method_frame, text="Gpage", bd=3, width=10, command= lambda: handle_button(1))
  Gscrape_button = tk.Button(method_frame, text="Gscrape", bd=3, width=10, command= lambda: handle_button(2))
  desc1 = tk.Label(method_frame, text="" + method_labels[0][0] + " - " + method_labels[0][1], font=("Arial", 8), wraplength=250, justify="left")
  desc2 = tk.Label(method_frame, text="" + method_labels[1][0] + " - " + method_labels[1][1], font=("Arial", 8), wraplength=250, justify="left")
  desc3 = tk.Label(method_frame, text="" + method_labels[2][0] + " - " + method_labels[2][1], font=("Arial", 8), wraplength=250, justify="left")
  
  input_frame = tk.Frame(window, highlightbackground="black", highlightcolor="black", highlightthickness=1)
  school_title = tk.Label(input_frame, text="Input (Comma Separated):", font=("Arial", 12), wraplength=250)
  schools_entry = scrolledtext.ScrolledText(input_frame, bd=1, width=45, height=5)
  school_ex = tk.Label(input_frame, text="Example Input: bellville henderson, watertown high, adirondack", font=("Arial", 8), wraplength=500)
  
  button_frame = tk.Frame(window, highlightbackground="black", highlightcolor="black", highlightthickness=1)
  button_title = tk.Label(button_frame, text="Functions:", font=("Arial", 12), wraplength=250)
  submit_button = tk.Button(button_frame, text="Submit", bg="#00AB66", bd=3, width=15, command= lambda: handle_submit(schools_entry.get("1.0", 'end')))
  clear_button = tk.Button(button_frame, text="Clear", bg="#FF2251", bd=3, width=15, command=clear)
  button_desc1 = tk.Label(button_frame, text="Submit - Execute the method provided in Step One with the Input and Keywords.", font=("Arial", 8), wraplength=250, justify="left")
  button_desc2 = tk.Label(button_frame, text="Clear - Clear all inputted text and all results.", font=("Arial", 8), wraplength=250, justify="left")
  
  keyword_frame = tk.Frame(window, highlightbackground="black", highlightcolor="black", highlightthickness=1)
  keyword_title = tk.Label(keyword_frame, text="Search Keywords:", font=("Arial", 12), wraplength=250)
  keyword_desc = tk.Label(keyword_frame, text="Adds keywords to the end of the search query to narrow down results. The default keywords look for guidance/school counselor emails.", font=("Arial", 8), wraplength=350, justify="left")
  keyword_entry = tk.Entry(keyword_frame, bd=1)
 
  result_frame = tk.Frame(window, highlightbackground="black", highlightcolor="black", highlightthickness=1)
  result_title = tk.Label(result_frame, text="Results:", font=("Arial", 12))
  export_button = tk.Button(result_frame, text="Export", bd=3, width=15, command= lambda: export(False))
  export_quick_button = tk.Button(result_frame, text="Quick Export", bd=3, width=15, command= lambda: export(True))
  result_display = scrolledtext.ScrolledText(result_frame, bd=1, width=90, height=10)

  credits_label = tk.Label(window, text="Created by Ryan Bell - Email: astrasolutionswd@gmail.com", font=("Arial", 8), justify="left")
  #End initializing

  #Start packing widgets
  title_frame.grid(row=0, rowspan=2, column=0, columnspan=4, padx=5, pady=5, sticky="n s w e")
  title_title.grid(row=0, column=0, padx=5, pady=5, sticky="w e")
  title_desc.grid(row=1, column=0, padx=5, sticky="w e")

  step1_label.grid(row=2, column=0, sticky="w")
  step2_label.grid(row=2, column=2, sticky="w")
  step3_label.grid(row=7, column=0, sticky="w")
  step4_label.grid(row=7, column=2, sticky="w")
  step5_label.grid(row=11, column=0, sticky="w")

  method_frame.grid(row=3, rowspan=4, column=0, columnspan=2, padx=5, pady=5, sticky="n s w e")
  method_title.grid(row=0, columnspan=2, sticky="w", padx=5, pady=5)
  Gsearch_button.grid(row=1, column=0, padx=7, pady=2)
  Gpage_button.grid(row=2, column=0, padx=7, pady=2)
  Gscrape_button.grid(row=3, column=0, padx=7, pady=2)
  desc1.grid(row=1, column=1, padx=2, sticky="w")
  desc2.grid(row=2, column=1, padx=2, sticky="w")
  desc3.grid(row=3, column=1, padx=2, sticky="w")
  
  input_frame.grid(row=3, rowspan=3, column=2, columnspan=2, padx=5, pady=5, sticky="n s w e")
  school_title.grid(row=0, column=0, sticky="w", padx=5, pady=4)
  schools_entry.grid(row=1, column=0, sticky="w", padx=4)
  school_ex.grid(row=2, column=0, sticky="w")

  button_frame.grid(row=8, rowspan=3, column=2, columnspan=2, padx=5, pady=5, sticky="n s w e")
  button_title.grid(row=0, column=0, sticky="w", padx=5, pady=5)
  submit_button.grid(row=1, column=0, sticky="w", padx=7, pady=2)
  clear_button.grid(row=2, column=0, sticky="w", padx=7, pady=2)
  button_desc1.grid(row=1, column=1, padx=2, sticky="w")
  button_desc2.grid(row=2, column=1, padx=2, sticky="w")
  
  keyword_frame.grid(row=8, rowspan=3, column=0, columnspan=2, padx=5, pady=5, sticky="n s w e")
  keyword_title.grid(row=0, column=0, sticky="w", padx=5, pady=5)
  keyword_desc.grid(row=1, column=0, sticky="w", padx=6, pady=1)
  keyword_entry.insert('0', "school guidance counselors")
  keyword_entry.grid(row=2, column=0, sticky="w e", padx=6, pady=4)
  
  result_frame.grid(row=12, rowspan=2, column=0, columnspan=4, padx=5, pady=5, sticky="n s w e")
  result_title.grid(row=0, column=0, sticky="w", padx=5, pady=5)
  export_button.grid(row=0, column=0, sticky="e", padx=135, pady=2)
  export_quick_button.grid(row=0, column=0, sticky="e", padx=7, pady=2)
  result_display.grid(row=1, column=0, sticky="w", padx=4, pady=2)

  credits_label.grid(row=14, column=0, sticky="w", padx=4, pady=3)
  #End packing

  schools_entry.focus()
  window.mainloop()