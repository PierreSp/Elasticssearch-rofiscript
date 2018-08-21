# Elasticssearch-Desktop
Elasticsearch for desktop with rofi (here used to find text, pdf, code documents)

This script searches all documents on the computer for a specific keyphrase. For this [FSCrawler](https://github.com/dadoonet/fscrawler) is used to index all types of files (pdf, txt, py, c++, videos images, ...) and send it to elasticsearch, which runs in a docker container.
Rofi is then used as simple interface for opening the found files.

## How to run
Install docker and FSCrawler with my predefined setupscript.

### Setup Elasticsearch
Install Elastic search. Most easy way to to so is to get the official docker image:
```bash
docker pull docker.elastic.co/elasticsearch/elasticsearch:6.3.2
```

Elasticsearch is also available on AUR or with apt-get. Details can be found [here](https://www.elastic.co/guide/en/elasticsearch/reference/current/setup.html).

Just run the basic settings (here I assume elasticsearch uses port 9200)

```bash
docker run -d -p 9200:9200 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:6.3.2
```

### Setup Fscrawler
Get FScrawler
```bash
wget https://repo1.maven.org/maven2/fr/pilato/elasticsearch/crawler/fscrawler/2.5/fscrawler-2.5.zip
unzip fscrawler-2.5.zip
```
Follow [this](https://fscrawler.readthedocs.io/en/fscrawler-2.5/user/getting_started.html) very simple tutorial to crawl your data. 

After creating a job_name, make sure to define the correct path in *.fscrawler/job_name/_settings.json* and setup your time, bytesize if needed.


## Resources:
- [Jupyter Notebook for Python search](https://github.com/ernestorx/es-swapi-test/blob/master/ES%20notebook.ipynb)
- [Blog Python and elastic](https://tryolabs.com/blog/2015/02/17/python-elasticsearch-first-steps/)
