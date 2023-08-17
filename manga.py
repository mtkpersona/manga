import os
import re
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
        
        prev = ""
        for chapter in chapters_list:
            chapter_number = chapter["Chapter"][-5:-1]
            page_number = chapter["Page"]
            
            
            if chapter_number == prev:
                chapter_number = (chapter_number + "." + chapter["Chapter"][-1])
                chapter_dict = {"chapter": chapter_number, "page": page_number}
                chapter_page_data.append(chapter_dict)
            else:
                prev = chapter_number
                chapter_dict = {"chapter": chapter_number, "page": page_number}
                chapter_page_data.append(chapter_dict)
    
    return name_data, url_manga, chapter_page_data

# URL of the website
url = "https://manga4life.com/read-online/Blazer-Drive-chapter-1-page-1.html"
#print("This is a url example: \n- https://manga4life.com/read-online/Onepunch-Man-chapter-1-page-1.html")
#url = input("Please insert the manga page url: \n")

# Call the function to fetch chapter page data
manga_name_data, url_manga, chapter_page_data = fetch_chapter_page_data(url)

# Print the fetched data
print(chapter_page_data)
print(len(chapter_page_data))
print(url_manga)
#print(chapter_page_data[0]["chapter"]) # Output: 0001
#print(chapter_page_data[0]["page"]) # Output: 56
#print(manga_name_data) # Output: Blazer-Drive

#####################################################################
var_chapter = 0
var_page = 0
manga_chapter = chapter_page_data[var_chapter]["chapter"]
manga_page = chapter_page_data[var_page]["page"]


base_url = f"https://{url_manga}/manga/"
extension = ".png"


#for chapter in range(1, int(manga_chapter)):
#    print(len(manga_chapter))
#    
#    for page in range(1, int(manga_page)):
#        print(len(manga_page))
#        image_url = f"{base_url}{manga_name_data}/{manga_chapter}-{manga_page}{extension}"
#        file_path = f"/storage/emulated/0/Download/{manga_name_data}/{manga_chapter}-{manga_page}{extension}"
#        response = requests.get(image_url)
#        
#        if response.status_code == 200:
#            
#            with open(file_path, 'wb') as file:
#                file.write(response.content)
#                print(f"{manga_name_data} {manga_chapter}-{manga_page} downloaded and saved to:", file_path)
#                if 
#        else:
#            print(f"Failed to download {manga_name_data} {manga_chapter}-{manga_page}")

#time.sleep(30)  # Delay for 30 seconds before requesting the next URL


# Create a directory to store the images
directory = f"/storage/emulated/0/Download/{manga_name_data}/"
try:
    if not os.path.exists(directory):
        os.makedirs(directory)
    print(f"Folder '{manga_name_data}' created successfully in Download folder.")
except FileExistsError:
    print(f"Folder '{manga_name_data}' already exists in Download folder.")
except Exception as e:
    print("An error occurred:", e)

for var_chapter in range(len(chapter_page_data)):
    manga_chapter = chapter_page_data[var_chapter]["chapter"]
    num_pages = chapter_page_data[var_chapter]["page"]
    
    for var_page in range(1, int(num_pages) + 1):
        manga_page = "00" + str(var_page)
        image_url = f"{base_url}{manga_name_data}/{manga_chapter}-{manga_page}{extension}"
        file_path = f"/storage/emulated/0/Download/{manga_name_data}/{manga_name_data}{manga_chapter}-{manga_page}{extension}"
        
        response = requests.get(image_url)
        time.sleep(10)
        
        if response.status_code == 200:
            with open(file_path, 'wb') as file:
                file.write(response.content)
                print(f"{manga_name_data} {manga_chapter}-{manga_page} downloaded and saved to:", file_path)
        else:
            print(f"Failed to download {manga_name_data} {manga_chapter}-{manga_page}")
        
        time.sleep(10)  # Add a small delay between each page download
        
    time.sleep(10)  # Add a longer delay between chapters
