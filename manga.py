import os
import re
import sys
import json 
import time 
import requests 
from bs4 import BeautifulSoup

def fetch_chapter_page_data(url):
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")
    script_tags = soup.find_all("script")
    content = str(script_tags)
    
    chapter_pattern = re.compile(r'vm\.CHAPTERS\s*=\s*(\[.*?\]);', re.DOTALL)
    manga_url = re.compile(r'vm\.CurPathName = "([^"]*)";')
    name_pattern = re.compile(r'vm\.IndexName = "([^"]*)";')
    
    chapter_match = chapter_pattern.search(content)
    url_match = manga_url.search(content)
    name_match = name_pattern.search(content)
    
    chapter_page_data = []
    if chapter_match and name_match:
        chapters_data = chapter_match.group(1)
        url_manga = url_match.group(1)
        name_data = name_match.group(1)
        chapters_list = json.loads(chapters_data)
        print(chapters_list)
        
        for chapter in chapters_list:
            raw_chapter = int(chapter["Chapter"][-1])
            if raw_chapter > 0:
                chapter_number = chapter["Chapter"][-5:-1]
                page_number = chapter["Page"]
                chapter_number = (chapter_number + "." + chapter["Chapter"][-1])
                chapter_dict = {"chapter": chapter_number, "page": page_number}
                chapter_page_data.append(chapter_dict)
            else:
                chapter_number = chapter["Chapter"][-5:-1]
                page_number = chapter["Page"]
                chapter_dict = {"chapter": chapter_number, "page": page_number}
                chapter_page_data.append(chapter_dict)
    return name_data, url_manga, chapter_page_data

def download_image(image_url, file_path):
    response = requests.get(image_url)
    time.sleep(10) 
    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            file.write(response.content)
            return True
    return False

def create_dir(dir):
    try:
        if not os.path.exists(dir):
            os.makedirs(dir)
            print(f"[ + ] Folder '{manga_name_data}' created successfully in Download folder.")
    except FileExistsError:
        print(f"[ - ] Folder '{manga_name_data}' already exists in Download folder.") 
    except Exception as e:
        print("[ - ] An error occurred:", e) 
        
#URL of the website
print("[ + ] System booting up...")
url = "https://www.manga4life.com/read-online/Toshiue-Elite-Onna-Kishi-ga-Boku-no-Mae-de-dake-Kawaii-chapter-0-page-1.html"
#url = "http://manga4life.com/read-online/Blazer-Drive-chapter-1-page-1.html"
#print("This is a url example: \n- https://manga4life.com/read-online/Onepunch-Man-chapter-1-page-1.html")
#url = input("Please insert the manga page url: \n")

# Call the function to fetch chapter page data
manga_name_data, url_manga, chapter_page_data = fetch_chapter_page_data(url)

# Create a directory to store the images
directory = f"/storage/emulated/0/Download/{manga_name_data}/" 
create_dir(directory)

# Define the filename for the log file
log_filename = directory + "logfile.txt"
print("[ + ] Creating logfile.")

try:
    while True:
        # Open the log file using a context manager
        with open(log_filename, "w") as log_file:
             sys.stdout = log_file  # Redirect standard output to the log file
             # Write initial message to the log file
             print("[ + ] Creating logfile successfully!\n", flush=True)
             log_file.write("[ + ] Creating logfile successfully!\n")
             time.sleep(2)
             # Print the fetched data and write it to the log file
             log_file.write(f"[ + ] System start...\n[ + ] Downloading from {url}\n")
             time.sleep(2)
             log_file.write(f"[ + ] Chapter Page Data\n{chapter_page_data}\n")
             log_file.write(f"[ + ] {manga_name_data}\n")
             log_file.write(f"[ + ] {url_manga}\n")
    
             base_url = f"https://{url_manga}/manga/"
             extension = ".png"
    
             for var_chapter in range(len(chapter_page_data)):
                 manga_chapter = chapter_page_data[var_chapter]["chapter"]
                 num_pages = chapter_page_data[var_chapter]["page"]
                 print(num_pages)
                 for var_page in range(1, int(num_pages) + 1):
                     if len(str(var_page)) == 3:
                         manga_page = str(var_page)
                     elif len(str(var_page)) == 2:
                        manga_page = "0" + str(var_page)
                     else:
                         manga_page = "00" + str(var_page)
                         
                     image_url = f"{base_url}{manga_name_data}/{manga_chapter}-{manga_page}{extension}"
                     file_path = f"/storage/emulated/0/Download/{manga_name_data}/{manga_name_data} {manga_chapter}-{manga_page}{extension}"
                         
                     # Try to download the image and retry if failed
                     retry_count = 3
                     while retry_count > 0:
                         success = download_image(image_url, file_path)
                         time.sleep(5)
                         if success:
                             print(f"[ + ] {manga_name_data} Chapter: {manga_chapter} Page: {manga_page} downloaded and saved to:", file_path, flush=True)
                             log_file.write(f"[ + ] {manga_name_data} Chapter: {manga_chapter} Page: {manga_page} downloaded and saved to: {file_path}")
                             break
                         else:
                             if retry_count == 0:
                                 print(f"[ - ] Failed to download {manga_name_data} {manga_chapter}-{manga_page}, \n[ - ] Please check your code again!", flush=True)
                                 log_file.write(f"[ - ] Failed to download {manga_name_data} {manga_chapter}-{manga_page}, \n[ - ] Please check your code again!")
                                 retry_count = 3
                                 break
                             else:
                                 print(f"[ - ] Failed to download {manga_name_data} {manga_chapter}-{manga_page}, Retrying...", flush=True)
                                 log_file.write(f"[ - ] Failed to download {manga_name_data} {manga_chapter}-{manga_page}, Retrying...")
                                 retry_count -= 1
                     time.sleep(3) # Add a small delay between each page download 
             time.sleep(6)
except KeyboardInterrupt:
    print("End")
finally:
    sys.stdout = sys.__stdout__    