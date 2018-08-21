# Elasticssearch-Desktop
Elasticsearch for desktop with rofi (here used to find text, pdf, code documents)
## How to run
1. Run ´´´docker pull docker.elastic.co/elasticsearch/elasticsearch:6.3.2´´´ to get elasticsearch in docker
2. For now development mode is fine, so *docker run -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:6.3.2* starts docker and opens port 9200 and 9300
3. Get [FSCrawler](https://fscrawler.readthedocs.io/en/fscrawler-2.5/user/getting_started.html) and crawl the documents you want (Tutorial follows)
4. 


## Resources:
[Jupyter Notebook for Python search](https://github.com/ernestorx/es-swapi-test/blob/master/ES%20notebook.ipynb)
[Blog Python and elastic](https://tryolabs.com/blog/2015/02/17/python-elasticsearch-first-steps/)
