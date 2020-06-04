file_name = "Manuscript-4.tex"
title = ""
author = ""

import re

author = ""
title = ""

if "tex" in file_name:


    f = open(file_name, "r")

    text = f.read()
    # print(text)
    text = text.replace('\\[', '\\begin{equation}')
    text = text.replace('\\]', '\\end{equation}')


    # parse for title information in the following after \\maketitle
    # title
    # author

    if author == "" and title == "":
        lines = text.split("\n")
        foundTitle = False
        for line in lines:
            if "\\maketitle" in line:
                foundTitle = True
                continue
            if foundTitle:
                if len(line) > 0 :
                    if author == "" and title != "":
                        author = line
                        break
                    if title == "" :
                        title = line

    # Set the author and title information
    lines = text.split("\n")
    text = ""
    foundTitle = False
    for line in lines:
        if "\\maketitle" in line:
            foundTitle = True
            text += line + "\n"
            continue
        elif "\\title" in line:
            line = "\\title{" + title + "}"
        elif "\\author" in line:
            line = "\\author{" + author + "}"
        elif foundTitle :
            if "\\tableofcontents" in line:
                foundTitle = False
            else:
                continue
        text += line + "\n"




    # Find the captions
    fig_captions = []
    images = text.split("end{figure}");
    i=0
    while(i < len(images)-1):
        split_1 = images[i+1].split("\n")
        caption = ''
        start = False
        for j in range(len(split_1)-1):
            split_1[j] = split_1[j].strip()
            if split_1[j].startswith("figure:") or split_1[j].startswith("Figure:"):
                  start = True
            if start == True:
                  caption += (split_1[j] + " ")
                  if(split_1[j] == ""):
                      break;
        fig_captions.append(caption.split(":")[1].strip())
        i += 1


    # Find the tables
    table_captions = []
    regexp = "end{longtable}|end{table}"
    tables = re.split(regexp, text);
    i=0
    while(i < len(tables)-1):
        split_1 = tables[i].split("\n")
        caption = ''
        start = False
        for j in range(len(split_1)-1):
            split_1[j] = split_1[j].strip()
            if split_1[j].startswith("table:") or split_1[j].startswith("Table:"):
                 start = True
            if start == True:
                 caption += (split_1[j] + " ")
                 if(split_1[j] == ""):
                     break;
        table_captions.append(caption.split(":")[1].strip())
        i += 1



    # Remove the Manual Figure and Table captions
    lines = text.split("\n")
    text = ""
    i=0
    start = False
    while(i < len(lines)):
        if lines[i].strip().startswith("Figure:") or lines[i].strip().startswith("figure:") or lines[i].strip().startswith("Table:") or lines[i].strip().startswith("table:"):
            start = True
        if start and lines[i].strip() == "":
            start = False
        if not start:
            text += lines[i] + "\n"
        i += 1


    # Get the labels for the figures and the tables
    fig_labels = []
    c = 0
    for caption in fig_captions:
        split = caption.split("((")
        fig_captions[c] = split[0]
        c += 1
        label = split[1].split("))")[0]
        fig_labels.append(label)


    table_labels = []
    c = 0
    for caption in table_captions:
        split = caption.split("((")
        table_captions[c] = split[0]
        c += 1
        label = split[1].split("))")[0]
        table_labels.append(label)


    # Display the Captions and the labels
    print("Captions:")
    i = 0
    for caption in fig_captions:
        i += 1
        print("\tFigure " + str(i) + " " + caption)
    print("\t-------------------------------------------------------------------------------")
    i = 0
    for caption in table_captions:
        i += 1
        print("\tTable " + str(i) + " " + caption)
    i = 0
    print("labels: ")
    for fig_label in fig_labels:
        i += 1
        print("\t Figure " + str(i) + " " + fig_label)
    i = 0
    print("\t-------------------------------------------------------------------------------")
    for table_label in fig_labels:
        i += 1
        print("\t Table " + str(i) + " " + table_label )



    # Place the captions in for the tables
    i = 0
    for caption in fig_captions:
        text = text.replace('\\caption{}', '\\caption{'+ str(caption) +'} \n \\label{fig:' + fig_labels[i] + '} ' , 1)
        i += 1


    # Place the captions in for the figures
    i=0
    c=0
    lines = text.split("\n")
    text = "";
    while (i < len(lines)):
        text += lines[i]
        text +="\n"
        if "begin{longtable}" in lines[i]:
            text += "\\caption{" + table_captions[c] + "} \\label{table:" + table_labels[c] + "} \\\\"
            c += 1
        i += 1


    for label in fig_labels:
        text = text.replace("((" + label + "))", "\\ref{fig:" + label + "}")
    for label in table_labels:
        text = text.replace("((" + label + "))", "\\ref{table:" + label + "}")


    # Check if there are any extra references
    print("\nParsing For errors in Figure and Table References:")
    print("..")
    l = 0
    lines = text.split("\n")
    for line in lines:
        l += 1
        if "((" in line:
            print("\nWARNING: Extra '(('' Characters at line " + str(l) + "!\n")
        if "))" in line:
            print("\nWARNING: Extra '))'' Characters at line " + str(l) + "!\n")
    print("Done Parsing For Reference Errors\n")











    # Time to do the bibliography
    print("Parsing the Reference section:")
    startRef = False
    atRef = False
    refs = []

    r = 0
    for line in lines:
        line = line.replace("{","").replace("}", "").replace("\\emph", "")
        if "References" in line or "references" in line:
            startRef = True
        if startRef and "]:" in line:
            r += 1
            refName = line.split("]:")[0].split("[")[1]
            print("\t" + refName + ":\t\t" + line.split("]:")[1] + "..")
            refs.append(refName)




    # Have to search for citations word by word because there may be multiple citations in a single line and the ordering will be
    # messed up if we just parse line by line
    print("\nDetermining citation order by parsing text.")
    refsOrder = [0]*len(refs)
    lines = text.split("\n")
    l = 0
    refsCount = 1
    for line in lines:
        l += 1
        if "References" in line or "references" in line:
            break
        words = line.split(" ")
        for word in words:
            word = word.replace("}","").replace("{","").replace("\\","").replace("(","").replace(","")","").replace("/","").replace("\n","")
            r = 0
            while r < len(refs):
                if str( "[" + refs[r] +"]") in word and refsOrder[r] == 0: # gotta make sure it hasnt already been found
                    print("\tFound ref number "  + str(refsCount) + " labeled " + refs[r] + " at line  " + str(l))
                    if not word.startswith("["):
                        print("\nWARNING: There may be a spacing issue with the reference at line " + str(l) + "!")
                        print("Context: " + line + "\n")
                    refsOrder[r] = refsCount
                    refsCount += 1
                r += 1



    # Now actually Create the Bibliography Section
    for ref in refs:
        text = text.replace("{[}" + ref + "{]}", "\\cite{" + ref + "}")

    lines = text.split("\n")
    text = ""
    startRef = False
    refStrings = []
    l = 0
    r = -1
    for line in lines:
        l += 1
        if "References" in line or "references" in line:
            lineRef = l
            startRef = True
            # We dont actually need a References section
            # because it will be included automatically when a bib is created
            # but there is still the section  that we have to close
            line = "}\n \\begin{thebibliography}{" + str(len(refs)) + "}"
            text += line + "\n";
        elif startRef:
            temp = line.replace("}:", "}")
            temp = temp.replace("cite", "bibitem")
            if 'bibitem' in temp:
                r += 1
                refStrings.append(temp)
            elif len(temp.replace(' ', '')) > 0 :
                refStrings[r] += temp.replace("\\end{document}", "")
        else:
            text += line + "\n";


    unused = []
    r = 0
    while( r < len(refsOrder) ):
        if refsOrder[r] == 0:
            unused.append(refs[r])
        r += 1



    ors = 0
    used = [""]*len(refsOrder)
    while (ors < len(refsOrder)):
        if refs[ors] not in unused:
            used[refsOrder[ors]-1] = refs[ors]
        ors += 1

    # Now print the reference strings in the correct order
    for ref in used:
        for rs in refStrings:
            if "{"+ref+"}" in rs and not ref.replace(" ", "") == "":
                text += rs + "\n"

    # Print the unused ones as well
    if len(unused) > 0:
        print("\nWARNING Some references were not used in text.")
        print("They will be commented out in the document")
        print("Unused References:")
    n = 0
    for us in unused:
        n += 1
        print("\t\t\t"  + str(n) + ". " + us)
        text += "%" + us + "\n"


    text += ("\\end{thebibliography} \n \\end{document}")

    print("\nParsing For errors in citations:")
    print("..")
    lines = text.split("\n")
    beganDocument = False
    l = 0
    for line in lines:
        l += 1
        if "\\begin{document}" in line :
            beganDocument = True
        if not beganDocument:
            continue
        if re.search("\\[([A-Z]|[a-z]|[0-9]|}|{)+\\]", line):
            print("\nWARNING: Line " + str(l) + " May to have an invalid references. !")
            print("Context: " + line + "!\n")

    print("Done parsing For errors in citations:")


    #Miscelaneous fixes
    # Add some hardcoded margins otherwise the page numbers will overlap the text
    text = text.replace("\\begin{document}", "\\usepackage[a4paper, total={6in, 8in}]{geometry} \n\n \\begin{document}")
    #Fix figures and tables floating around
    text = text.replace("\\begin{figure}", "\\begin{figure}[h]")
    text = text.replace("\\begin{longtable}[]", "\\begin{longtable}[h]")



    f = open("_"+file_name, "w")
    f.write(text)
    f.close()






