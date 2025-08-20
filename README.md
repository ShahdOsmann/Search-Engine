# Search Engine Project

This project is a **mini search engine** implementation built from scratch.  
It demonstrates the full pipeline of how search engines work:
- **Web crawling & scraping**  
- **Inverted indexing** (using Hadoop MapReduce in Java)  
- **TF-IDF ranking** (Python)  
- **PageRank ranking** (Python)  

The final system allows ranking of documents both by **content relevance** (TF-IDF) and **link importance** (PageRank).

---

## Project Workflow

### 1. Scraper (Python)
- Starts crawling from a seed link (`https://www.wikipedia.org/`).  
- Collects up to `N` links (default: 1000).  
- Saves each page into a `.txt` file under `data/files/`.  
  - **First line** of each file: the URL.  
  - **Rest of file**: raw text content from the page.  
- Also writes all visited links to `links.txt`.
---

### 2. Inverted Index (Hadoop MapReduce, Java)
- Input: the text files scraped in Step 1.  
- Mapper:
  - Emits `<word@filename, 1>` for each token.  
- Combiner:
  - Aggregates counts per file → `<word, filename:count>`.  
- Reducer:
  - Combines postings across files into inverted index:
    ```
    word   file1:3;file2:5;file7:1;
    ```
- Output: `out-invert.txt`  
---

### 3. PageRank (Python)
- Builds a **graph** of web pages from `links.txt`.  
- Computes PageRank scores using power iteration with damping factor (default: 0.85).  
- Maps each file (`fileX.txt`) to its PageRank score.  
- Re-orders inverted index results based on PageRank importance.  
- Output: `page-rank.txt`  
### 4. TF-IDF Ranking (Python)
- Reads word frequencies from `out-invert.txt`.  
- Calculates:
- **TF (Term Frequency):**  
  ```
  tf = count(word in file) / total words in file
  ```
- **IDF (Inverse Document Frequency):**  
  ```
  idf = log10(N / df)
  ```
  where `N` = total docs, `df` = number of docs containing the word.  
- Computes **TF-IDF = TF × IDF**.  
- Ranks files per word by TF-IDF score.  
- Output: `tf-idf.txt`

## Technologies Used
- **Python** (Scraper, PageRank, TF-IDF)
  - `requests`, `beautifulsoup4`, `numpy`
- **Java + Hadoop MapReduce** (Inverted Index)
- **Mathematics**
  - TF-IDF weighting  
  - PageRank algorithm (power iteration)

---

##  How to Run

1. **Scrape pages**
   ```bash
   python Scrap/main.py
   Output → links.txt / All files (folder)
2. **Build inverted index (Hadoop)**
   ```bash
   hadoop jar search-index.jar DriverIndex data/files/ data/out/
   Output → out-invert.txt
3. **Run PageRank**
   ```bash
   python pagerank/main.py
   Output → page-rank.txt
4. **Run TF-IDF**
   ```bash
   python TF-IDF/main.py
   Output → tf-idf.txt
