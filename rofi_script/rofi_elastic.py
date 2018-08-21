#!/usr/bin/python3
# -*- coding: utf-8 -*-
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

while i < 5 and search_value != "" and search_value != "Nothing found":
    i += 1
    search_value = create_search(searchrofi_input)
    print(search_value)
    res = es.search(
        index="read_uni",
        body={
            "query": {
                "multi_match": {
                    "fields": ["content", "title", "author", "Keywords"],
                    "query": search_value,
                    "fuzziness": "AUTO",
                }
            }
        },
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

                if hit["_source"]["meta"]["raw"]["title"] != "":
                    curtitle = hit["_source"]["meta"]["raw"]["title"]
                else:
                    curtitle = hit["_source"]["file"]["filename"]
                curtitle = str(curtitle) + " | "+ str(hit["_source"]["path"]["real"])
                all_files_title.append(curtitle)
                all_files[curtitle] = hit["_source"]["path"]["real"]
            except Exception as e:
                print(e)
                pass

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
