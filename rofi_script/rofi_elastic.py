#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""rofi_elastic.py: Script for rofi which connects elasticsearch and rofi
   Author Pierre Springer
   Needs a working elasticsearch and 
"""
import subprocess
import re
import pprint
import argparse
from elasticsearch import Elasticsearch
from subprocess import Popen, PIPE


REMOVEHOME = re.compile("\/home\/.*?\/.*?\/(.*)")

parser = argparse.ArgumentParser(description="")
parser.add_argument(
    "--index", default="read_uni", type=str, help="Index to use for elastic search"
)

opt = parser.parse_args()

INDEX = opt.index


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
    # print(search_value)
    # Search with elasticnet. Fuzzy allows edit distance (e.g. typos),
    # fields are the fields to scan, source reduces the output
    res = es.search(
        index=INDEX,
        size=1000,
        # char_filter=[ "html_strip" ],
        body={
            "query": {
                "multi_match": {
                    "fields": ["content", "title", "author", "Keywords"],
                    "query": search_value,
                    "fuzziness": "AUTO",
                }
            },
            "highlight": {
                "pre_tags": ['<span foreground="CYAN">'],
                "post_tags": ["</span>"],
                "order": "score",
                "number_of_fragments": 1,  # How many phrases do we want to extract
                "fragment_size": 45,  # How long shall the phrases be
                "fields": {"content": {}},
            },
        },
        _source=[
            "file.filename",
            "path.real",
            "meta.raw.title",
            "meta.raw.description",
        ],
    )
    print(res["hits"]["total"])
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
                    curtitle = str(hit["_source"]["meta"]["raw"]["title"])
                except Exception as ex:  # only means that field does not exist
                    curtitle = str(hit["_source"]["file"]["filename"])
                try:
                    curdescr = hit["_source"]["meta"]["raw"]["description"]
                except Exception as ex:  # only means that field does not exist
                    curdescr = str(hit["highlight"]["content"][0]).replace("\n", "")
                # Cut or extend title to a length of 25
                if len(curtitle) > 22:
                    curtitle = curtitle[0:22] + "..."
                else:
                    curtitle = curtitle + " " * (25 - len(curtitle))

                filepath = str(REMOVEHOME.match(str(hit["_source"]["path"]["real"]))[1])
                # Cut or extend path to a length of 30
                if len(filepath) > 27:
                    filepath = filepath[0:27] + "..."
                else:
                    filepath = filepath + " " * (30 - len(filepath))

                curtitle = curtitle + " | " + filepath + " | " + str(curdescr)
                all_files_title.append(curtitle)
                all_files[curtitle] = hit["_source"]["path"]["real"]
            except Exception as e:
                print(e)
                continue
        print(len(all_files_title))
        rofi_results = Popen(
            args=["rofi", "-dmenu", "-i", "-p", "-markup-rows", "Result"],
            stdin=PIPE,
            stdout=PIPE,
        )
        (stdout, stderr) = rofi_results.communicate(
            input=str.encode("\n".join(all_files_title))
        )
        subprocess.call(
            ["xdg-open", all_files[stdout.decode("utf-8").replace("\n", "")]]
        )
        break
