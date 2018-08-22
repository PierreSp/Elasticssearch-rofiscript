# Elasticssearch-Desktop
Elasticsearch for desktop with rofi (here used to find text, pdf, code documents)

This script searches all documents on the computer for a specific keyphrase. For this [FSCrawler](https://github.com/dadoonet/fscrawler) is used to index all types of files (pdf, txt, py, c++, videos images, ...) and send it to elasticsearch.
Rofi is then used as simple interface for opening the found files.

## How to run
Install docker and FSCrawler with my predefined setupscript.

### Setup Elasticsearch
Elasticsearch is available on AUR or with apt-get. Details can be found [here](https://www.elastic.co/guide/en/elasticsearch/reference/current/setup.html).

Just run the basic settings (here I assume elasticsearch uses port 9200)

Alternatively it is possible to run elasticsearch withhin a docker. For this a permanant storage is needed.
To use the official docker image with persistent storage run:
```bash
docker pull docker.elastic.co/elasticsearch/elasticsearch:6.3.2
docker volume create --name elasticdata

```
Now elasticsearch can be started by (or use -d for detached/background mode):
```bash
docker  --rm -ti -p 9200:9200 -v elasticdata:/usr/share/elasticsearch/data elasticsearch
```

### Setup Fscrawler
Get FScrawler
```bash
wget https://repo1.maven.org/maven2/fr/pilato/elasticsearch/crawler/fscrawler/2.5/fscrawler-2.5.zip
unzip fscrawler-2.5.zip
```
Follow [this](https://fscrawler.readthedocs.io/en/fscrawler-2.5/user/getting_started.html) very simple tutorial to crawl your data. 

After creating a job_name, make sure to define the correct path in *.fscrawler/job_name/_settings.json* and setup your time, bytesize if needed.

### Usage with rofi:
in *rofiscripts/rofi_elastic.py* replace the default parameter for the argparser with your index (job_name). Alternatively the index can be submitted with the --index parameter.
Install the requirements.txt and run the script to use rofi with elastic search. This can also easily be used with i3.

## Resources:
- [Jupyter Notebook for Python search](https://github.com/ernestorx/es-swapi-test/blob/master/ES%20notebook.ipynb)
- [Blog Python and elastic](https://tryolabs.com/blog/2015/02/17/python-elasticsearch-first-steps/)
