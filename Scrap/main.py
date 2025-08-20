import os
import requests
from bs4 import BeautifulSoup
import time

number_of_links = 1000
folder_path = "C:\\Users\\user\\PycharmProjects\\Scrap\\All files"

# Function to fetch content from a URL and write it to a file
def fetch_and_write_content(url, file_name):
    try:
        page = requests.get(url)
        src = page.content
        soup = BeautifulSoup(src, "html.parser")

        # Extract textual content
        text_content = soup.get_text()

        # Ensure folder exists
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        file_path = os.path.join(folder_path, f"{file_name}.txt")

        # Write content to file
        with open(file_path, "w", encoding="utf-8") as file:
            # Write URL to the first line
            file.write(url + "\n")

            # Write content to the rest of the file
            file.write(text_content)
    except requests.exceptions.RequestException as e:
        print(f"Failed to access {url}: {str(e)}")


# Start the timer
start_time = time.time()

# Dictionary to track visited URLs
visited = {}

# List to manage the queue of URLs to crawl
queue = ["https://www.wikipedia.org/"]

# Initialize visited dictionary
visited["https://www.wikipedia.org/"] = True

# Create a file to save the links
with open("links.txt", "w", encoding="utf-8") as file:
    # Write the GeeksforGeeks website as the first link
    file.write("https://www.wikipedia.org/\n")
    # Start crawling until the queue is empty or we have enough links
    while queue and len(visited) <= number_of_links:
        current_url = queue.pop(0)
        try:
            page = requests.get(current_url)
            src = page.content
            soup = BeautifulSoup(src, "html.parser")

            # Find all <a> tags to continue crawling
            links = soup.find_all('a')
            for link in links:
                href = link.get('href')
                if href and href.startswith("http"):  # Check if href is valid and absolute URL
                    if href not in visited:  # Only if the link has not been visited
                        visited[href] = True
                        if len(visited) >= number_of_links: break
                        queue.append(href)
                        # Write the link to the file
                        file.write(href.encode('utf-8').decode('utf-8') + "\n")
        except requests.exceptions.RequestException as e:
            print(f"Failed to access {current_url}: {str(e)}")
        print(len(visited))

# Read links from scraping.txt and create files for each link
with open("links.txt", "r", encoding="utf-8") as f:
    links = f.readlines()
    for i, link in enumerate(links):
        # Remove newline character from the end of the link
        link = link.strip()

        # Create file name based on link index
        file_name = f"file{i + 1}"

        fetch_and_write_content(link, file_name)


# End the timer
end_time = time.time()

# Calculate the total time taken
time_taken = end_time - start_time

# Print the number of unique visited URLs
print(f"Number of unique URLs visited: {len(visited)}")
print(f"Time taken in minutes: {time_taken / 60} minutes")
print(f"Time taken in seconds: {time_taken} seconds")
