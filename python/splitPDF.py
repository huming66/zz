from PyPDF2 import PdfFileWriter, PdfFileReader
file =r"L:\download\民国续遵义府志（二）-01\民国续遵义府志（二）-01.pdf"
pdfOutName = '选举.pdf'
input_pdf = PdfFileReader(file)
output = PdfFileWriter()
for j in ( [0]+ list(range(26,46)) ):
    output.addPage(input_pdf.getPage(j))
with open(pdfOutName, "wb") as output_stream:
    output.write(output_stream)