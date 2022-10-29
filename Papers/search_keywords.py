# import packages
import fitz
import json
import csv

apparatus_keyword = ("apparatus", "implementation", "hardware","setup")
participant_keywords = ("participant", "subjects", "paid", "given", "compensated", "reward", "gift")

years = [1983, 1987, 1991, 1996, 1999, 2001, 2004, 2007, 2011, 2016, 2017, 2018, 2019, 2020, 2021, 2022]


with open("doi_authors.json", 'r') as f:
    json_decoded = json.load(f)

failed_papers = []
apperances = []

for i in range(0, 5):


    #year = json_decoded[i]['Year']


    # Only for the Participant_keyword
    #if year in years:
    key_results = {}
    doc_name = str(i) + ".pdf"
    try:
        doc = fitz.open(doc_name)
        for page in doc:
            words = [w[4].lower() for w in page.get_text("words")]
            for sword in apparatus_keyword:
                for word in words:
                    if sword in word:  # search word is *part* of a word on the page
                        pages = key_results.get(sword, set())
                        pages.add(page.number)
                        key_results[sword] = pages

        for word in key_results:
            result = list(map(str, key_results[word]))
            year = json_decoded[i]['Year']
            page_list = ", ".join(result)
            print(doc_name)
            #print("Word '%s' occurs on pages %s." % (word, page_list))                                
            apperances.append(i)
            break

        
        #print("\n ##################################################")
    except:
        failed_papers.append(i)
        #print("Error in paper with index = " + str(i))
        error = 1


print("\n#####################################")
print("Failed papers[" + str(len(failed_papers)) + "] = ")
print("apperances[" + str(len(apperances)) + "] = ")
    

#results = {}
#doc = fitz.open("1.pdf")
#for page in doc:
#    words = [w[4].lower() for w in page.get_text("words")]
#    for sword in search_words:
#        for word in words:
#            if sword in word:  # search word is *part* of a word on the page
#                pages = results.get(sword, set())
#                pages.add(page.number)
#                results[sword] = pages

#for word in results:
#    result = list(map(str, results[word]))
#    page_list = ", ".join(result)
#    print("Word '%s' occurs on pages %s." % (word, page_list))