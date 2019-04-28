# Final Project: Real Time Trending Twitter Analytics
Analyzing real time Twitter data with Microsoft Key Phrase Extraction and MapReduce aggregation to produce a word cloud of trending topics.

## Prerequisites
1) Microsoft Azure account & active subscription
2) Twitter developer account & active application
3) Cognitive Sciences service
4) Hadoop 3.7 cluster

## Dependencies
1) Python 3.X
2) Azure Blob Storage (azure-storage-blob)
3) tweepy
4) pandas
5) PIL
6) wordcloud
7) matplotlib
8) cv2

## Installation
1) Clone this repository and install the required dependencies using ```pip```
2) Replace lines 13-16 in ```scrape_twitter.py``` with your Twitter application keys
3) Replace lines 19-20 in ```scrape_twitter.py``` with your Microsoft Azure Cognitive Sciences service key and Azure Blob Storage account key, respectively
4) Replace lines 15-16 in ```generate_graph.py``` with the same Azure Blob Storage account name & key
5) Replace lines 3-4 of ```\mapreduce\download.py``` and ```\mapreduce\upload.py```with your Azure Blob Storage account name & key
6) Copy the files in ```\mapreduce``` to your running Hadoop cluster


## How to Run
1) Run ```python scrape_twitter.py``` to start streaming Twitter data and analyzing with Microsoft Azure Key Phrase Extraction
2) SSH into the Hadoop cluster and run ```bash run.sh``` on the Hadoop cluster to run the MapReduce framework
3) Run ```python generate_graph.py``` locally in another window to generate the final cloud graph

The cloud graph will update in real time (every minute) as it receives new data from the MapReduce framework running on the Hadoop cluster.
