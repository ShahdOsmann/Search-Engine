import os
import math

def count_words_in_file(file_path):
    word_count = 0
    with open(file_path, 'r') as file:
        for line in file:
            words = line.split()  # Split the line into words
            word_count += len(words)  # Increment word count by the number of words in the line
    return word_count

def count_words_in_folder(folder_path):
    word_counts = {}
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            word_counts[filename] = count_words_in_file(file_path)
    return word_counts

# Example usage:
folder_path = 'All files'
word_counts = count_words_in_folder(folder_path)

data = {}
idf = {}
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
                    # Check if the file_name exists in word_counts before accessing it
                    if file_name in word_counts:
                        tf = float(count)/word_counts[file_name]
                        files.append({'file': file_name, 'tf': float(tf)})
                    else:
                        print(f"File '{file_name}' from the data does not exist in the folder.")
            data[word] = files
            if(len(data[word])):idf[word] = math.log10(1000/len(data[word]))

# Sort files by TF-IDF for each word
sorted_files = {}
for word, files_info in data.items():
    sorted_files[word] = sorted(files_info, key=lambda x: x['tf'] * idf[word], reverse=True)

# Output sorted files for each word to a file
with open("tf-idf.txt", "w") as output_file:
    for word, files_info in sorted_files.items():
        file_names = ", ".join(file_info['file'] for file_info in files_info)
        output_file.write(f"{word}: {file_names}\n")
