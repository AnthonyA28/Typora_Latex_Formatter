# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 16:38:26 2020

@author: antho
"""


file_name = "Manuscript_test.md"
title = ""
author = ""

import re

author = ""
title = ""

if "md" in file_name:


    f = open(file_name, "r", encoding="utf8")

    text = f.read()


    # identify the Manual Figure and Table captions
    lines = text.split("\n")
    figures = []
    tables = []
    i = 0
    while(i < len(lines)):
        if lines[i].strip().startswith("Figure:") or lines[i].strip().startswith("figure:"):
            print(lines[i])
            figures.append(lines[i])
        if lines[i].strip().startswith("Table:") or lines[i].strip().startswith("table:"):
            print(lines[i])
            tables.append(lines[i])
        i += 1

    table_labels = []
    for table in tables:
        split = table.split("((")[1].split("))")[0]
        table_labels.append(split)
        print("Table label: " + split)

    figure_labels = []
    for figure in figures:
        split = figure.split("((")[1].split("))")[0]
        figure_labels.append(split)
        print("Figure label: " + split)


    # now replace the figure and table labels
    text = ""
    for line in lines:
        if line.strip().startswith("Table:") or line.strip().startswith("table:"):
            n = 0
            for table_label in table_labels:
                n += 1
                if table_label in line:
                    line = line.replace("Table: ", "Table " + str(n) + ": ")
                    line = line.replace("table: ", "Table " + str(n) + ": ")
                    line = line.split("((")[0]
        if line.strip().startswith("Figure:") or line.strip().startswith("figure:"):
            n = 0
            for figure_label in figure_labels:
                n += 1
                if figure_label in line:
                    line = line.replace("Figure: ", "Figure " + str(n) + ": ")
                    line = line.replace("figure: ", "Figure " + str(n) + ": ")
                    line = line.split("((")[0]
        text += line + "\n"



    lines = text.split("\n")
    text = ""
    for line in lines:
        n = 1
        for table_label in table_labels:
            if table_label in line:
                line = line.replace("((" + table_label + "))", str(n) )
            n += 1
        n = 1
        for figure_label in figure_labels:
            if figure_label in line:
                line = line.replace("((" + figure_label + "))",  str(n) )
            n += 1
        text += line + "\n"


    # Find the references.. This will remove the reference section
    print("\nParsing the References Section..")
    refLabels = []
    refStrings = []
    lines = text.split("\n")
    text = ""
    atReferences = False
    for line in lines:
        if not atReferences:
            text += line + "\n"
        if len(line.replace(" ", "")) == 0 :
            continue
        if atReferences :
            refLabel = line.split("]:")[0].replace("[", "")
            print("\tref: " + line + "\n\t\tlabel: " + refLabel)
            refLabels.append(refLabel)
            refStrings.append(line)
        if "References" in line:
            atReferences = True


    print("\nDetermining the order of the references in the text")
    refsOrder = [0]*len(refLabels)
    lines = text.split("\n")
    refCount = 1
    l = 0
    for line in lines:
        l += 1
        words = line.split(" ")
        for word in words :
            n = 0
            for refLabel in refLabels:
                if "["+refLabel+"]" in word and refsOrder[n] == 0:
                    print(refLabel + " found at line " + str(l) )
                    refsOrder[n] = refCount
                    refCount += 1
                n += 1



    n = 1
    for refLabel in refLabels:
        text = text.replace("["+refLabel+"]", "[[" + str(refsOrder[n-1]) +"]]"+"["+refLabel+"]")
        n += 1


    unused = []
    r = 0
    while( r < len(refsOrder) ):
        if refsOrder[r] == 0:
            unused.append(refLabels[r])
        r += 1



    ors = 0
    used = [""]*len(refsOrder)
    while (ors < len(refsOrder)):
        if refLabels[ors] not in unused:
            used[refsOrder[ors]-1] = refLabels[ors]
        ors += 1

    text += "\n"
    # Now print the reference strings in the correct order
    print()
    n = 0
    for ref in used:
        for rs in refStrings:
            if "["+ref+"]:" in rs and not ref.replace(" ", "") == "":
                # Replace the pseudonym with the actual number
                print(rs)
                text += rs.replace("["+ref+"]:", "["+str(n+1)+"]:") + "\n\n"
                n += 1

    # Print the unused ones as well
    if len(unused) > 0:
        print("\nWARNING Some references were not used in text.")
        print("They will be commented out in the document")
        print("Unused References:")
    n = 0
    for us in unused:
        n += 1
        print("\t\t\t"  + str(n) + ". " + us)
        text += "WARN: Unused Reference " + us + "\n\n"



    f = open("_"+file_name, "w")
    f.write(text)
    f.close()






