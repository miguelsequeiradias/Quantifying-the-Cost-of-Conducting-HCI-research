# import packages
import fitz
import json
import csv

search_words = ("hardware", "specification", "software", "price", "material", "materials" , "replication", "reproducibility", "prototypes", "value", "device","controller",\
     "grant ", "smartphone", " ios ", "android", "participant", "gift", "apparatus", " hp ", " intel ", "samsung", "apple", "huawei", " oppo ", "vivo", " lg ", "xiaomi", "lenovo", \
        "dell", "toshiba", "motorola", "nokia", "sony", "ericsson", " htc ", "blackberry", " amd ", "asus", "acer", " msi ", "microsoft", " ibm ", "desktop", "phone", \
            "virtual reality", "augmented reality", "head-mounted displays", "hdr", "displays", "projectors", \
                "sensors", "system", "interview", "ghz", " cpu ", " gpu ", "nvidia", " ram ", "headset")

key_search_words = ("hardware", "participant", "subjects" "apparatus" , "hp", "intel", "samsung", "apple", "huawei", "oppo", "vivo", "lg", "xiaomi", "lenovo", \
    "dell", "toshiba", "motorola", "nokia", "sony", "ericsson", "htc", "blackberry", "amd", "asus", "acer", "msi", "microsoft", "ibm", "desktop", "phone", \
        "virtual reality", "augmented reality", "head-mounted displays", "hdr", "displays", "projectors", \
            "sensors", "interview", "ghz", "cpu", "gpu", "nvidia", "ram", "headset", "lcd")


test_word = ("apparatus", "setup")
test_word2 = ("participant", "subjects", "paid", "given", "compensated", "reward", "gift")

years = [1983, 1987, 1991, 1996, 1999, 2001, 2004, 2007, 2011, 2016, 2017, 2018, 2019, 2020, 2021, 2022]


with open("doi_authors.json", 'r') as f:
    json_decoded = json.load(f)

failed_papers = []
apperances = []

for i in range(0, 9688):


    year = json_decoded[i]['Year']
    #if year in years:
    key_results = {}
    doc_name = str(i) + ".pdf"
    try:
        doc = fitz.open(doc_name)
        for page in doc:
            words = [w[4].lower() for w in page.get_text("words")]
            for sword in test_word2:
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