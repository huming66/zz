import pdfplumber
import re, glob
import pandas as pd
folders = ['L:\\github\\']
out_folder = 'L:\\github\\zz\\data\\'
paperList = pd.DataFrame([], columns= ["年", "月", "期","标题","栏目","栏目e","行业","作者"])
# file=r'中行2019.01月刊完整版.pdf'
# file= folder + file
# print(file)
for folder in folders:
    files = glob.glob(folder + r"*.pdf")
    for file in files:
        with pdfplumber.open(file) as pdf:
            # page 1
            txt = pdf.pages[0].within_bbox((440,50,595,200),False).extract_text()
            [month, year, no] = ['M'+txt[0:2],'Y'+txt[3:7],'#'+re.search("第[ ]*([\d]*)[ ]*期",txt).group(1)]
            # page 2
            txt = pdf.pages[2].within_bbox((50,150,380,800),False).extract_text()
            txt = re.sub("\n[0-9]{2}[ ]*", '|',txt)
            papers = re.findall("\|[^\|]*\/[^\|\n]*", txt) # re.findall("\n[0-9]{2}.*\n?.*\/[^\|\n]*", txt)    
            columnTxt = txt                #栏目
            for paper in papers:
                columnTxt = columnTxt.replace(paper,'\n')        # remove papers' txt
            columns = list(filter(len,columnTxt.split('\n')))    # remove empty
            idxColumn = [txt.find(column) for column in columns] 
            columnEng = [re.sub("[^A-z &/']+","",col).strip() for col in columns]
            columnChs = [columns[i].replace(columnEng[i],'').strip() for i in range(len(columns))]
            for paper in papers:           #文章
                [title,author] = re.sub("\|[ ]*", '',paper).replace('\n','').split('/')
                idxPaper = txt.find(paper)
                idx = sum(1 for x in idxColumn if x < idxPaper)-1
                columnC = columnChs[idx]
                columnE = columnEng[idx]
                paperList.loc[len(paperList)] =[year, month, no, title, columnC, columnE,'--', author]
            # page 3
            txt = pdf.pages[3].within_bbox((0,400,375,800),False).extract_text()
            err1 =  (len(re.findall("Foresight[]*\n[0-9]{2}",txt)) == 0) & (len(re.findall("\n[0-9]{2}$",txt))==1) 
            if err1:
                txt = re.sub("Foresight[]*\n[0-9]{0}", "Foresight \n00 ",txt)
            txt = re.sub("\n[0-9]{2}[ ]*", '|',txt)
            papers = re.findall("\|[^\|]*\/[^\|\n]*", txt) # re.findall("\n[0-9]{2}.*\n?.*\/[^\|\n]*", txt)   
            columnTxt = txt                #栏目
            for paper in papers:
                columnTxt = columnTxt.replace(paper,'\n')        # remove papers' txt
            columns = list(filter(lambda x: (len(x) >= 3),columnTxt.split('\n')))    # remove empty
            idxColumn = [txt.find(column) for column in columns] 
            columnEng = [re.sub("[^A-z &/']+","",col).strip() for col in columns]
            columnChs = [columns[i].replace(columnEng[i],'').strip() for i in range(len(columns))]
            for paper in papers:           #文章
                [title,author] = re.sub("\|[ ]*", '',paper).replace('\n','').split('/')
                idxPaper = txt.find(paper)
                idx = sum(1 for x in idxColumn if x < idxPaper)-1
                columnC = columnChs[idx]
                columnE = columnEng[idx]
                paperList.loc[len(paperList)] =[year, month, no, title.strip(), columnC, columnE,'--', author]
            paperList.to_csv(out_folder+ r'index.csv', index=False)