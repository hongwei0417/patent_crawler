from tqdm import tqdm
import pandas as pd
import requests
import glob
import time
import os

def save_result_page():
    id_list = set([patent_id.strip() for patent_id in open("id/id_A", 'r')])
    
    for id_number in tqdm(id_list):
        result_url = "http://appft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&p=1&u=%%2Fnetahtml%%2FPTO" \
                     "%%2Fsearch-bool.html&r=1&f=G&l=50&co1=AND&d=PG01&s1=%s&OS=%s&RS=%s" % (id_number, id_number, id_number)
        
        r = requests.get(result_url)
        with open('result_id_A/%s.html' % id_number, 'w') as file:
            file.write(r.text)
        
        time.sleep(8)
        

def extract_data_from_page(filename, dataframe):
    files = "result_id_A/4922925.html"
    pattern1_start = "<BR><CENTER><B>Abstract</B></CENTER>"
    pattern2_start = "<CENTER><B><I>Claims</B></I></CENTER>"
    pattern_end   = "<HR>"

    with open(file, 'r') as f:
        content = [ line for line in f.readlines()]
        abstract = []
        claim = []

        i = 0 
        total_line = len(content)
        while i < total_line:
            if pattern1_start in content[i]:
                i += 1
                while pattern_end not in content[i]:
                    if "<P>" not in content[i] and "</P>" not in content[i]:
                        abstract.append(content[i])
                    i += 1

            if pattern2_start in content[i]:
                i += 2
                while pattern_end not in content[i]: 
                    claim.append(content[i])
                    i += 1
            i += 1
            
    abstract = ''.join(abstract)
    claim = ''.join(claim).replace("<BR>", "")

    basename = os.path.basename(file)
    results = {
        "patent_id": str(os.path.splitext(basename)[0]),
        "abstract": abstract,
        "claim"   : claim
    }

    dataframe = dataframe.append(results, ignore_index=True)
    return dataframe


if __name__ == "__main__":
    # save_result_page()

    files = [ i for i in glob.iglob("result_id_A/*.html")]
    data = pd.DataFrame(columns=["patent_id", "abstract", "claim"])
    
    for file in files:
        data = extract_data_from_page(file, data)
    
    data.to_csv("result/id_A.csv", index=False)