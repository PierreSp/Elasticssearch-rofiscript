#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""rofi_elastic.py: Script for rofi which connects elasticsearch and rofi
   Author Pierre Springer
   Needs a working elasticsearch and 
"""
import subprocess
from elasticsearch import Elasticsearch
from subprocess import Popen, PIPE
import pprint


def create_search(searchrofi_input):
    # Create a terminal -i makes the search case insensitive
    rofi_search = Popen(
        args=["rofi", "-dmenu", "-i", "-p", "Search"], stdin=PIPE, stdout=PIPE
    )

    (stdout, stderr) = rofi_search.communicate(input=str.encode(searchrofi_input))
    search_value = stdout.decode("utf-8").replace("\n", "")
    return search_value


es = Elasticsearch()
searchrofi_input = ""
i = 0
search_value = "predefinednon"

# Stop when the user cancels the search, but continue, when nothing is found
while i < 5 and search_value != "" and search_value != "Nothing found":
    i += 1
    search_value = create_search(searchrofi_input)
    print(search_value)
    # Search with elasticnet. Fuzzy allows edit distance (e.g. typos),
    # fields are the fields to scan, source reduces the output
    res = es.search(
        index="read_uni",
        body={
            "query": {
                "multi_match": {
                    "fields": ["content", "title", "author", "Keywords"],
                    "query": search_value,
                    "fuzziness": "AUTO",
                }
            },
            "highlight": {"fields": {"content": {}}},
        },
        _source=[
            "file.filename",
            "path.real",
            "meta.raw.title",
            "meta.raw.description",
        ],
    )
    if res["hits"]["total"] == 0:
        searchrofi_input = "Nothing found"
        print("No results found")
    else:
        all_files = {}
        all_files_title = []
        for hit in res["hits"]["hits"]:
            pprint.pprint(hit)
            try:
                try:
                    curtitle = hit["_source"]["meta"]["raw"]["title"]
                except Exception as ex:  # only means that field does not exist
                    curtitle = hit["_source"]["file"]["filename"]
                try:
                    curdescr = hit["_source"]["meta"]["raw"]["description"]
                except Exception as ex:  # only means that field does not exist
                    curdescr = str(hit["highlight"]["content"][0]).replace("\n", "")
                curtitle = (
                    str(curtitle)
                    + " | "
                    + str(hit["_source"]["path"]["real"])[0:30]
                    + " | "
                    + str(curdescr)
                )
                all_files_title.append(curtitle)
                all_files[curtitle] = hit["_source"]["path"]["real"]
            except Exception as e:
                print(e)
                continue

        rofi_results = Popen(
            args=["rofi", "-dmenu", "-i", "-p", "Result"], stdin=PIPE, stdout=PIPE
        )
        (stdout, stderr) = rofi_results.communicate(
            input=str.encode("\n".join(all_files_title))
        )
        subprocess.call(
            ["xdg-open", all_files[stdout.decode("utf-8").replace("\n", "")]]
        )
        break
