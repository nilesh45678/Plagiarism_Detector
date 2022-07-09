from tkinter import *   # for gui
from tkinter import filedialog # for file selection menu
from tkinter import messagebox # for showing warnings
import PyPDF2 # for reading PDF files
import docx2txt #for reading file
from sklearn.metrics.pairwise import cosine_similarity 
from sklearn.feature_extraction.text import TfidfVectorizer



class Plagiarism_Detector():
    def __init__(self,file1 = '',file2 = ''):
        self.file1 = file1
        self.file2 = file2
        self.root = Tk()
        self.root.title("Palagarism Detector")
        self.root.geometry('900x600')
        self.file_label1 = Label(self.root,text="No file choosen" if self.file1 == '' else self.file1,background="lightgrey",font=('TimesNewRoman',12))
        self.file_label1.place(x=25,y=50,height=50,width=600)
        self.file_button1 = Button(self.root,text="Click to select file",background="yellow",font=('TimesNewRoman',12),command=lambda : self.select_file(1))
        self.file_button1.place(x=650,y=50,height=50,width=200)
        self.file_label2 = Label(self.root,text="No file choosen" if self.file2 == '' else self.file2,background="lightgrey",font=('TimesNewRoman',12))
        self.file_label2.place(x=25,y=150,height=50,width=600)
        self.file_button2 = Button(self.root,text="Click to select file",background="yellow",font=('TimesNewRoman',12),command=lambda : self.select_file(2))
        self.file_button2.place(x=650,y=150,height=50,width=200)
        self.result_button = Button(self.root,text="Click to Check Plagiarism",background="Orange",font=('TimesNewRoman',12),command=self.check_plagiarism)
        self.result_button.place(x=350,y=300,height=50,width=200)
        self.result_label = Label(self.root,text="RESULT  = ",background = 'red',font=('TimesNewRoman',12))
        self.result_label.place(x=250,y=450,height=50,width=400)
        self.root.mainloop()
    
    def select_file(self,file):
        if file == 1:
            self.file1 = filedialog.askopenfilename()
            self.file_label1.configure(text=self.file1)
        elif file == 2:
            self.file2 = filedialog.askopenfilename()
            self.file_label2.configure(text=self.file2)
    
    def check_plagiarism(self):
        if(self.file1 == '' or self.file2 == ''):
            messagebox.showwarning('WARNING','Select both file first.')
            return
        text1 = self.get_text(self.file1)
        text2 = self.get_text(self.file2)
        if(text1 == None):
            messagebox.showwarning("Unsupported file format","{} is a unsupported file format.".format(self.file1))
        if(text2 == None):
            messagebox.showwarning("Unsupported file format","{} is a unsupported file format.".format(self.file2))
        vector1,vector2 = TfidfVectorizer().fit_transform([text1,text2]).toarray()
        score = cosine_similarity([vector1, vector2])[0][1]
        self.result_label.configure(text="RESULT  = {:3.2f}%".format(score*100))
        # print('#{:2X}{:2x}00'.format(round(255 * score),round(255*(1-score))))
        self.result_label.configure(background='#{:02X}{:02x}00'.format(round(255 * score),round(255*(1-score))))
        


    def get_text(self,path):
        text = ''
        try:
            if(path.endswith('.pdf')):
                file = open(path,'rb')
                pdf = PyPDF2.PdfFileReader(file)
                for i in range(0,pdf.getNumPages()):
                    text += pdf.getPage(i).extractText()
            elif(path.endswith('.docx')):
                text = docx2txt.process(path)
            else:
                file = open(path,'r')
                text = file.read()
            return text
        except :
            return None
    
if __name__ == '__main__':
    Plagiarism_Detector()

