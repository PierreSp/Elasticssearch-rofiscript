#!/usr/bin/python3
# -*- coding: utf-8 -*-
from elasticsearch import Elasticsearch

from subprocess import Popen, PIPE
import subprocess

# Create a terminal -i makes the search case insensitive
rofi_search = Popen(
    args=["rofi", "-dmenu", "-i", "-p", "Search"], stdin=PIPE, stdout=PIPE
)
(stdout, stderr) = rofi_search.communicate(input="")
word_to_search = stdout.decode("utf-8").replace("\n", "")
es = Elasticsearch()
res = es.search(
    index="read_uni", body={"query": {"match": {"content": word_to_search}}}
)
# print("Got %d Hits:" % res["hits"]["total"])
if res["hits"]["total"] == 0:
    print("No results found")
else:
    all_files = []
    for hit in res["hits"]["hits"]:
        try:
            print(hit["_source"]["path"]["real"])
            all_files.append(hit["_source"]["path"]["real"])
        except Exception as e:
            pass

    rofi_results = Popen(
        args=["rofi", "-dmenu", "-i", "-p", "Result"], stdin=PIPE, stdout=PIPE
    )
    (stdout, stderr) = rofi_results.communicate(input=str.encode("\n".join(all_files)))
    subprocess.call(["xdg-open", stdout])
