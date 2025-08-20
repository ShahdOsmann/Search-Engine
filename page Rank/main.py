import os
import requests
from bs4 import BeautifulSoup
import time
import numpy as np

damping_factor = 0.85
tolerance = 1e-6
max_iterations = 5


def page_rank(graph, rank):
    N = len(graph)

    # Initialize the rank vector with 1/N for all pages
    for i in range(N):
        rank[i] = 1.0 / N

    # Pre-compute the cumulative sum of each row
    pre = [list(row) for row in graph]
    for i in range(N):
        for j in range(1, N):
            pre[i][j] += pre[i][j - 1]


    for _ in range(max_iterations):
        new_rank = [0.0] * N

        # Calculate the new rank for each page
        for i in range(N):
            # Update the new rank for the current page based on incoming links
            for j in range(N):
                if graph[j][i] == 1:
                    new_rank[i] += rank[j] / pre[j][-1]

            # Apply the damping factor and add the random jump probability
            new_rank[i] = damping_factor * new_rank[i] + (1.0 - damping_factor) / N

        # Check for convergence
        converged = all(abs(rank[i] - new_rank[i]) <= tolerance for i in range(N))
        if converged:
            break

        # Update the rank vector for the next iteration
        rank[:] = new_rank
    return rank


links=[]
cnt=0
with open("links.txt", "r") as f:
    lines = f.readlines()
f.close()
for link in lines:
    link = link.strip()
    links.append(link)
nodes=[]
for link in links:
    link = link.strip()
    try:
        page = requests.get(link)
        src = page.content
        soup = BeautifulSoup(src, "html.parser")
        all_links = soup.find_all('a')
        can=0
        for sub_link in all_links:
            href = sub_link.get('href')
            if (href and href.startswith("http") and href in links and href not in nodes):
                can = 1; nodes.append(href)
        if can==1 and link not in nodes:
            nodes.append(link)
        cnt+=1 ; print(cnt)
    except requests.exceptions.RequestException as e:
        print(f"Failed to access {link}: {str(e)}")
n = len(nodes)
matrix = [[0 for _ in range(n)] for _ in range(n)]
map={}
idx=0 ; cnt=1
for node in nodes:
    map[node] = idx ; idx+=1

for node in nodes:
    try:
        page = requests.get(node)
        src = page.content
        soup = BeautifulSoup(src, "html.parser")
        all_links = soup.find_all('a')
        for sub_link in all_links:
            href = sub_link.get('href')
            if (href and href.startswith("http") and  href  in nodes):
                matrix[map[node]][map[href]] = 1
        cnt+=1; print(cnt);

    except requests.exceptions.RequestException as e:
        print(f"Failed to access {link}: {str(e)}")

num_zeros = sum(row.count(0) for row in matrix)

#print("Number of zeros in the matrix:", num_zeros)

N = len(matrix)
rank = [0.0] * N

rank = page_rank(matrix, rank)


#print("\nPageRank Scores:")
#for i, score in enumerate(rank):
 #   print(f"Page {i}: {score:.6f}")

map_page_rank={}
for i, score in enumerate(rank):
    map_page_rank[f"file{i+1}.txt"]= score

#print(map_page_rank)

map_files = {}
for i in range(1000):
    map_files[f"file{i+1}.txt"] = 1


data={}
with open('out-invert.txt', 'r') as file:
    for line in file:
        line = line.strip().split('\t')
        if len(line) >= 2:  # Check if line has at least two elements
            word = line[0]
            files = []
            for item in line[1].split(';'):  # Split by ';' to get each file info
                file_info = item.split(':')
                if len(file_info) == 2:  # Ensure correct format
                    file_name, count = file_info
                    file_name = f"{file_name}.txt"
                    if file_name in map_files:
                        files.append(file_name)
                    else:
                        print(f"File '{file_name}' from the data does not exist in the folder.")
            data[word] = files

sorted_data = {}
for word, files in data.items():
    # Sort files based on PageRank scores
    sorted_files = sorted(files, key=lambda x: map_page_rank.get(x, 0), reverse=True)
    sorted_data[word] = sorted_files

# Display sorted data
#for word, files in sorted_data.items():
 #   print(f"{word}: ", files)

# Output sorted files for each word to a file
with open("page-rank.txt", "w") as output_file:
    for word, files in sorted_data.items():
        output_file.write(f"{word}: {', '.join(files)}\n")






