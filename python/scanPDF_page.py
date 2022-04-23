import pdfplumber
from PyPDF2 import PdfFileWriter, PdfFileReader
import re, glob, os
import pandas as pd
folders = ['Z:\\zz\\']#['L:\\github\\']
out_folder_idx = 'Z:\\zz\\test\\'#'L:\\github\\zz\\data\\'
out_folder_pdf = 'Z:\\zz\\test\\' #'L:\\github\\zz\\data\\pdf\\'
paperList = pd.DataFrame([], columns= ["年", "月", "期","标题","栏目","栏目e","行业","专栏","作者","内容"])
out_pdf = False

for folder in folders:
    files = glob.glob(folder + r"*.pdf")
    files = sorted( filter(os.path.isfile, files )) #files.sort(key=os.path.getmtime) 
    if (1 == 0):
        files=[folder + r'中行2022.01月最终完整版.pdf']
    for file in files:
        paperPages = []
        with pdfplumber.open(file) as pdf:
            # ================================== page 1
            txt = pdf.pages[0].within_bbox((440,60,595,200),False).extract_text()
            [month, year, no] = ['M'+txt[0:2],'Y'+txt[3:7],'#'+re.search("第[ ]*([\d]*)[ ]*期",txt).group(1)]            
            for i in range(len(pdf.pages[4:-2])):
                txt = pdf.pages[4+i].within_bbox((0,0,585,600),False).extract_text()
                if txt.find('◎') > 0:
                    paperPages.append(i+4)
                    n1 = txt.find('\n')
                    if not re.search("[A-z]{4,6}",txt[:n1]): # without eng
                        n1 = n1+txt[n1+1:].find('\n')
                    column = txt[:n1].replace('\n','')
                    # column = re.search("^(.*)\n",txt).group(1)
                    columnEng = re.sub("[^A-z &/']+","",column).strip() 
                    columnChs = column.replace(columnEng,'').strip().replace(' ','')  
                    if txt.find('张公权金融言论集》（马学斌编著）摘登') > 0:  #张公权
                        txt = txt.replace('\n','ZzZ')
                        g = re.search("ZzZ(\[按\].*。)ZzZ(.*ZzZ.*张公权金融言论集》（马学斌编著）摘登.*)ZzZ◎张公权",txt)
                        title = g.group(2).replace('ZzZ','\n')
                        author = '张公权'
                        txt1 = g.group(1).replace('ZzZ','\n')        
                    elif txt.find('编者按') > 0:  #张公权
                        txt = txt.replace('\n','ZzZ')
                        g = re.search("ZzZ[ ]{0,2}([\[]?编者按[\]]?.*。)ZzZ(.*)ZzZ◎([^Zz]*)",txt)
                        title = g.group(2).replace('ZzZ','\n')
                        author = g.group(3)
                        txt1 = g.group(1).replace('ZzZ','\n')                      
                    # if (year=='Y2021' and month=='M08' and i== 73):
                    #     title = '一切事业成功的基础\n—— 《张公权金融言论集》（马学斌编著）摘登（6）'
                    #     author = '张公权'
                    #     txt1 = txt[19:740]
                    # elif (year=='Y2021' and month=='M08' and i== 75):
                    #     title = '怎样做一个成功的银行员\n—— 《张公权金融言论集》（马学斌编著）摘登（7）'
                    #     author = '张公权'
                    #     txt1 = txt[19:808]    
                    # elif (year=='Y2021' and month=='M09' and i== 76):
                    #     title = '国民对于国家经济现状应有之觉悟\n—— 《张公权金融言论集》（马学斌编著）摘登（8）'
                    #     author = '张公权'
                    #     txt1 = txt[19:186]   
                    # elif (year=='Y2021' and month=='M08' and i== 75):
                    #     title = '我国实业开发之先决条件\n—— 《张公权金融言论集》（马学斌编著）摘登（9）'
                    #     author = '张公权'
                    #     txt1 = txt[19:808]    
                    else:  #      
                        # n1 = txt.find('\n')
                        # if not re.search("[A-z]{4,6}",txt[:n1]): # without eng
                        #     n1 = n1+txt[n1+1:].find('\n')
                        title = txt[n1+1: txt.find('◎')-1]
                        author = re.search("◎(.*)\n",txt).group(1)
                        txt = pdf.pages[4+i].within_bbox((50,0,300,730),False).extract_text()
                        idx = txt.find('◎')
                        idx = idx + txt[idx:].find('\n')
                        txt1 = txt[idx+1:]+ ' ...'
                    if '专栏' in columnChs.replace(' ',''):
                        nn = title.find('\n')
                        title1 = title if nn<0 else  title[0:nn]
                        title1=title1[0:-2]
                        txt = pdf.pages[2].within_bbox((30,100,380,800),False).extract_text().replace('\t','')
                        if title1.replace(' ','') not in txt.replace(' ',''):
                            txt = pdf.pages[3].within_bbox((0,400,375,800),False).extract_text().replace('\t','')
                        txt = txt.replace('\n','ZzZ')    
                        nn = txt.find(title1) 
                        txt = txt[0:nn]
                        if txt.find('专栏') > 0: #  
                            column2 = re.search("ZzZ([^Zz]*)专栏",txt).group(1)
                        else:
                            column2 = re.search("ZzZ([^Zz]*)[ ]*Special",txt).group(1).strip()
                    else:
                        column2 = '--'    
                    paperList.loc[len(paperList)] =[year, month, no, title.strip(), columnChs.replace(' ',''), columnEng,'--',column2,author,txt1]
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