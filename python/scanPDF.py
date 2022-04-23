import pdfplumber
from PyPDF2 import PdfFileWriter, PdfFileReader
import re, glob, os
import pandas as pd
folders = ['Z:\\zz\\']#['L:\\github\\']
out_folder_idx = 'Z:\\zz\\paper\\'#'L:\\github\\zz\\data\\'
out_folder_pdf = 'Z:\\zz\\paper\\' #'L:\\github\\zz\\data\\pdf\\'
paperList = pd.DataFrame([], columns= ["年", "月", "期","标题","栏目","栏目e","行业","作者","内容"])
out_pdf = False
method = 2
def firstP(author,p0=4):
    p1 = p0
    while (p1 < len(pdf.pages)):
        if re.search(author, pdf.pages[p1].within_bbox((50,50,590,400),False).extract_text()):
            paperPages.append(p1)
            txt = pdf.pages[p1].within_bbox((50,0,300,730),False).extract_text()
            idx = txt.find('◎')
            idx = idx + txt[idx:].find('\n')
            return [txt[idx+1:]+ ' ...',p1+1] 
        else:
            p1=p1+1
    return ['not found', p0]

for folder in folders:
    files = glob.glob(folder + r"*.pdf")
    files = sorted( filter(os.path.isfile, files )) #files.sort(key=os.path.getmtime) 
    paperPages = []
    if (1 == 0):
        files=[folder + r'中行2017.01月最终确定完整版.pdf']
    for file in files:
        paperPages = []
        p0=4
        with pdfplumber.open(file) as pdf:
            # ================================== page 1
            txt = pdf.pages[0].within_bbox((440,60,595,200),False).extract_text()
            [month, year, no] = ['M'+txt[0:2],'Y'+txt[3:7],'#'+re.search("第[ ]*([\d]*)[ ]*期",txt).group(1)]
            # ================================== page 2
            txt = pdf.pages[2].within_bbox((30,150,380,800),False).extract_text()
            if txt[3:7]+txt[0:2] < '201810':        # before 2018/10
                txt = re.sub("\nP\n[0-9]{,2}$", '',txt)   # before 2018/10
            if (year+month) == 'Y2019M04':
                txt = txt.replace('\n41','').replace('Market\n全球','Market\n41 全球')
            if method == 1:
                txt = re.sub("\n[0-9]{2}[ ]*", '|',txt)
            if method == 2:
                pgArea = pdf.pages[2].within_bbox((30,150,70,800),False).extract_text()
                pgs = list(filter(lambda x: (len(x.strip()) >= 2),pgArea.split('\n')     ))
                for pg in pgs:
                    txt = re.sub("\n"+ pg +"[ ]*", '|',txt)
            papers = re.findall("\|[^\|]*\/[^\|\n]*", txt) # re.findall("\n[0-9]{2}.*\n?.*\/[^\|\n]*", txt)                 
            columnTxt = txt                #栏目
            for paper in papers:
                columnTxt = columnTxt.replace(paper,'\n')        # remove papers' txt
            columns = list(filter(lambda x: (len(x.strip()) >= 3),columnTxt.split('\n')))    # remove empty
            idxColumn = [txt.find(column) for column in columns] 
            columnEng = [re.sub("[^A-z &/']+","",col).strip() for col in columns]
            columnChs = [columns[i].replace(columnEng[i],'').strip() for i in range(len(columns))]
            for i in range(len(columnChs)):
                if len(columnChs[i]) == 0:       # remove empty
                    del columnChs[i]
                    del columnEng[i]
                else:           
                    if len(columnEng[i]) == 0:   # empty english => __
                        columnEng[i] = '__' 
            # columnEng = list(filter(len,columnEng)) # remove empty line
            # columnChs = list(filter(len,columnChs)) # remove empty line            
            for paper in papers:           #文章
                [title,author] = re.sub("\|[ ]*", '',paper).replace('\n','').split('/')
                idxPaper = txt.find(paper)
                idx = sum(1 for x in idxColumn if x < idxPaper)-1
                columnC = columnChs[idx]
                columnE = columnEng[idx]
                [txt1, p0] = firstP(author.replace(' ','[ ]*'),p0)       #author.split(' ')[0]         
                paperList.loc[len(paperList)] =[year, month, no, title.strip(), columnC.replace(' ',''), columnE,'--', author,txt1]
            # ================================== page 3
            txt = pdf.pages[3].within_bbox((0,400,375,800),False).extract_text()
            # err1 =  (len(re.findall("Foresight[]*\n[0-9]{2}",txt)) == 0) & (len(re.findall("\n[0-9]{2}$",txt))==1) 
            # if err1:  # page off-line issue for 2019/01
            #     txt = re.sub("Foresight[]*\n[0-9]{0}", "Foresight \n76 ",txt)
            if (year+month) == 'Y2017M07':
                txt = txt.replace('\n32','\n').replace('课题组\n在','课题组\n32 在')
            elif (year+month) == 'Y2019M01':
                txt = txt.replace('\n76','\n').replace('\n70\n','\n76 ').replace('Foresight \n','Foresight \n70 ')
            if (method == 1):
                txt = re.sub("\n[0-9]{2}[ ]*", '|',txt)
            elif method == 2:
                pgArea = pdf.pages[3].within_bbox((30,150,70,800),False).extract_text()
                pgs = list(filter(lambda x: (len(x.strip()) >= 2),pgArea.split('\n')     ))
                for pg in pgs:
                    txt = re.sub("\n"+ pg +"[ ]+", '|',txt)
            papers = re.findall("\|[^\|]*\/[^\|\n]*", txt) # re.findall("\n[0-9]{2}.*\n?.*\/[^\|\n]*", txt)   
            columnTxt = txt                #栏目
            for paper in papers:
                columnTxt = columnTxt.replace(paper,'\n')        # remove papers' txt
            columns = list(filter(lambda x: (len(x.strip()) >= 3),columnTxt.split('\n')))    # remove empty
            idxColumn = [txt.find(column) for column in columns] 
            columnEng = [re.sub("[^A-z &/']+","",col).strip() for col in columns]
            columnChs = [columns[i].replace(columnEng[i],'').strip() for i in range(len(columns))]
            for i in range(len(columnChs)):
                if len(columnChs[i]) == 0:       # remove empty
                    del columnChs[i]
                    del columnEng[i]
                else:           
                    if len(columnEng[i]) == 0:   # empty english => __
                        columnEng[i] = '__' 
            for paper in papers:           #文章
                # print(paper)
                [title,author] = re.sub("\|[ ]*", '',paper).replace('\n','').split('/')
                idxPaper = txt.find(paper)
                idx = sum(1 for x in idxColumn if x < idxPaper)-1
                columnC = columnChs[idx]
                columnE = columnEng[idx]
                [txt1, p0] = firstP(author.replace(' ','[ ]*'),p0)  #author.split(' ')[0]
                paperList.loc[len(paperList)] =[year, month, no, title.strip(), columnC.replace(' ',''), columnE,'--', author,txt1]
            paperPages.append(len(pdf.pages)-2)
            if out_pdf:
                pdfOutName = out_folder_pdf + '_'.join(['gjjr', year,month])
                for i in range(len(paperPages)-1):                             # output paper PDF
                    input_pdf = PdfFileReader(file)
                    output = PdfFileWriter()
                    for j in range(paperPages[i],paperPages[i+1]):
                        output.addPage(input_pdf.getPage(j))
                    with open(pdfOutName + '_' +str(i+1).zfill(2) +".pdf", "wb") as output_stream:
                        output.write(output_stream)
            print('_'.join(['gjjr', year,month]), len(paperList))         
paperList.to_csv(out_folder_idx+ r'index.csv', index=True,index_label='#') # output CSV

