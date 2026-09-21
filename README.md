## TED Talks Search Engine

A simple Python search engine that indexes and retrieves TED talk transcripts using **TF–IDF** scoring.

## Requirements
- **Python 3.13** or **Python 3.12.4**
- Standard libraries only (`csv`, `re`, `math`, `collections`)


## How to Run
1. download the repository.
2. Place the following files in the project folder:
   - `search_engine.py` (it's the main program)
   - `TED_transcripts.csv` (dataset with the transcripts and URLs)
   - `stop_words.txt` (list of stopwords)
   - `verb.csv` (verb conjugation mappings)
3. Open a terminal in the project folder and run:
   - python search_engine.py