from tkinter import *
from pil import ImageTk
from customtkinter import *
from tkinter import messagebox
import pickle as pkl    
import datetime


class lms:
    def __init__(self, library_name):
        self.list_of_books='books.pkl'
        self.library_name=library_name
        self.books_dict={}
        self.logs=[]
        try:
             with open('logs.pkl', 'rb') as f:
                 self.logs = pkl.load(f)
                 if self.logs==[]:
                     print("currently no book is issued")
                 else:
                   print("currently book issued details")
                   print(self.logs)
        except:
             pass

        self.issued = [i["book_id"] for i in self.logs]
        if self.logs==[]:
            pass
        else:
           print("currently issued book id")
           print(self.issued)
        Id=101
        try:
            with open('bk.pkl','rb') as f:
                self.books=pkl.load(f)
                for value in self.books.values():
                    if str(Id) not in self.issued:
                      self.books_dict.update({str(Id):{"books_title":value.get("books_title"),
                 "lender_name":"","issue_date":"","status":"available"}})
                    else:
                       self.books_dict.update({str(Id):{"books_title":value.get("books_title"),
                 "lender_name":"","issue_date":"","status":"issued"}})
                    Id=Id+1
        except:
         with open(self.list_of_books) as bk:
               content=bk.readlines()
         for line in content:
                 if str(Id) not in self.issued:
                   self.books_dict.update({str(Id):{"books_title":line.replace("\n",""),
                 "lender_name":"","issue_date":"","status":"available"}})
                 else:
                   self.books_dict.update({str(Id):{"books_title":line.replace("\n",""),
                 "lender_name":"","issue_date":"","status":"issued"}})
                 Id=Id+1
        f.close()
       # with open(self.list_of_books,'rb') as bk:
           # self.books_dict = pkl.load(bk)

    def display_books(self):
        if self.logs==[]:
            print("currently no book is issued")
        else:
            print(" currently book issued details")
            print(self.logs)
        win = Tk()
        win.title("Library")
        win.geometry("500x400")

        # create canvas
        canvas = Canvas(win, bg="white")
        canvas.pack(side=LEFT, fill=BOTH, expand=1)

        # add scrollbar
        scrollbar = Scrollbar(win, orient=VERTICAL, command=canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        # configure canvas
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # create table frame
        table_frame = Frame(canvas)
        canvas.create_window((0,0), window=table_frame, anchor="nw")

        # create labels
        Label(table_frame, text="LIST OF BOOKS", font=("Arial", 14)).grid(row=0, column=1, padx=20, pady=10)
        Label(table_frame, text='BOOK ID', font=("Arial", 12, "bold"), borderwidth=1, relief="solid").grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        Label(table_frame, text='AUTHOR NAME', font=("Arial", 12, "bold"), borderwidth=1, relief="solid").grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        Label(table_frame, text='STATUS', font=("Arial", 12, "bold"), borderwidth=1, relief="solid").grid(row=1, column=2, padx=10, pady=10, sticky="ew")

        # iterate over books_dict and create labels for each book
        for i, (key, value) in enumerate(self.books_dict.items(), start=2):
            book_title = value.get("books_title")
            status = value.get("status")
            Label(table_frame, text=key, font=("Arial", 10), borderwidth=1, relief="solid").grid(row=i, column=0, padx=10, pady=5, sticky="ew")
            Label(table_frame, text=book_title, font=("Arial", 10), borderwidth=1, relief="solid").grid(row=i, column=1, padx=10, pady=5, sticky="ew")
            Label(table_frame, text=status, font=("Arial", 10), borderwidth=1, relief="solid").grid(row=i, column=2, padx=10, pady=5, sticky="ew")

        win.mainloop()

    def add_books_gui(self):
        # create window
        win = Toplevel()
        win.title("Add Book")
        win.geometry("400x200")

        # create labels
        Label(win, text="Enter Book Title:", font=("Arial", 12)).grid(row=0, column=0, padx=20, pady=20)

        # create entry widget
        title_entry = Entry(win, font=("Arial", 12))
        title_entry.grid(row=0, column=1)

        # add button to add book
        def add_book():
            # get book title
            new_book = title_entry.get().strip()

            # check if book title is valid
            if not new_book:
                messagebox.showwarning("Warning", "Please enter a book title.")
                return
            elif len(new_book) > 25:
                messagebox.showwarning("Warning", "Book title is too long. Title length should be 25 characters or less.")
                return
            for  value in self.books_dict.values():
                if new_book==value.get("books_title"):
                     messagebox.showwarning("Warning", "This book already exists in library")
                     return
            with open(self.list_of_books, "a") as bk:
                bk.write(f"{new_book}\n")    
            

            book_id = str(int(max(self.books_dict)) + 1)
            self.books_dict[book_id] = {"books_title": new_book, "lender name": "", "issue_date": "", "status": "available"}
            messagebox.showinfo("Success", f"Book '{new_book}' has been added successfully.")
            self.save_data()
            win.destroy()

        # create button to add book
        add_btn = Button(win, text="Add Book", font=("Arial", 12), command=add_book)
        add_btn.grid(row=1, column=1, pady=20)

        win.mainloop()

    def delete_books_gui(self):
        win = Tk()
        win.title("Delete Book")
        win.minsize(width=300, height=150)
        win.geometry("400x200")
        lab.pack(side='top')
        lab.place(x=0, y=0)

        def delete_book():
            book_id = entry.get()
            if book_id in self.books_dict.keys():
                if self.books_dict[book_id]["status"] == "available":
                    # self.books_dict.pop(book_id)
                    del self.books_dict[book_id]
                    self.save_data()
                    result.config(text="The book ID " + book_id + " has been successfully deleted.")
                else:
                    result.config(text="Cannot delete the book as it is currently issued to someone.")
                    entry.delete(0,END)
            else:
                result.config(text="Book ID not found.")
                entry.delete(0,END)

        label = Label(win, text="Enter the book ID that you want to delete:", font=("Arial", 12))
        label.pack(pady=10)
        label.place(x=30, y=20)

        entry = Entry(win, font=("Arial", 12))
        entry.pack(pady=10)
        entry.place(x=60, y=50)

        button = Button(win, text="Delete Book", font=("Arial", 12), command=delete_book)
        button.pack(pady=10)
        button.place(x=150, y=90)

        result = Label(win, text="", font=("Arial", 12))
        result.pack(pady=10)
        result.place(x=30, y=140)

        win.mainloop()

    def issue_books_gui(self):
        win = Tk()
        win.title("Issue Books")
        win.geometry("400x300")

        books_id_lbl = Label(win, text="Enter the book ID:")
        books_id_lbl.pack(pady=(20,10))

        books_id_entry = Entry(win, width=25)
        books_id_entry.pack()

        your_name_lbl = Label(win, text="Enter your name:")
        your_name_lbl.pack(pady=(20,10))

        your_name_entry = Entry(win, width=25)
        your_name_entry.pack()

        def issue():
            your_name = your_name_entry.get()
            books_id = books_id_entry.get()
            if your_name=='':
                messagebox.showinfo("failed to issue",f"please enter your name")
                
            #print(books_id,self.books_dict.keys())
            if books_id in self.books_dict.keys():
                issue_date = datetime.datetime.now().strftime("%Y-%M-%D %H:%M:%S")
                if self.books_dict[books_id]["status"] == "available":
                    self.books_dict[books_id]["lender_name"] = your_name
                    self.books_dict[books_id]["issue date"] = issue_date
                    self.books_dict[books_id]["status"] = "issued"
                    self.logs.append({"book_id": books_id, "lender_name": your_name, "issue_date": issue_date, "action": "issued"})
                    self.save_data()
                    win.destroy()
                    messagebox.showinfo("success",f"The book with ID {books_id} has been successfully issued to {your_name} on {issue_date}")
                else:
                    messagebox.showinfo("failed to issue",f"The book with ID {books_id} is currently issued to someone else.")
                    books_id_entry.delete(0,END)

                    
            else:
                result.config(text="Book ID not found in library.")
                books_id_entry.delete(0,END)
        
            

        issue_btn = Button(win, text="Issue", command=issue)
        issue_btn.pack(pady=20)

        result = Label(win, text="", font=("Arial", 12))
        result.pack(pady=10)
        result.place(x=60, y=200)


        win.mainloop()
   
    def save_data(self):
         # function to save updated data to files
        with open('bk.pkl', 'wb') as file:
            file.seek(0)
            file.truncate(0)
            pkl.dump(self.books_dict,file)
            

        with open('logs.pkl', 'wb') as file:
             file.seek(0)
             file.truncate(0)
             pkl.dump(self.logs, file)
    
    def return_books(self):
        win = Toplevel()
        win.title("Return Book")
        win.geometry("400x300")
        win.resizable(False, False)

        # Label and Entry for Book ID
        lbl_book_id = Label(win, text="Book ID:")
        lbl_book_id.pack(pady=10)
        ent_book_id = Entry(win)
        ent_book_id.pack()

        # Function to handle returning of book
        def return_book():
            book_id = ent_book_id.get()
            if book_id in self.books_dict.keys():
                if self.books_dict[book_id]["status"] == "available":
                    lbl_result.config(text="This book is already available in the library. Please check your Book ID.")
                else:
                    self.books_dict[book_id]["lender_name"] = ""
                    self.books_dict[book_id]["issue_date"] = ""
                    self.books_dict[book_id]["status"] = "available"
                    for i in self.logs:
                        if i['book_id'] == book_id:
                            print("returned bookid")
                            print(i['book_id'])
                            self.logs.remove(i)
                    self.save_data()
                    lbl_result.config(text="Book returned successfully!")
            else:
                lbl_result.config(text="Book ID not found.")
                ent_book_id.delete(0,END)
        
        # Button to return book
        btn_return = Button(win, text="Return Book", command=return_book)
        btn_return.pack(pady=10)

        # Label to display result
        lbl_result = Label(win, text="")
        lbl_result.pack()

        win.mainloop()




#___________________________________________________________________________________________

root = Tk()
root.title("Library")
root.minsize(width=400,height=400)
root.geometry("605x405")
bg = ImageTk.PhotoImage(file='assets/libBg.jpg')
lab = Label(root, image=bg)
lab.pack(side='top')
lab.place(x=0, y=0)

frame1 = CTkFrame(root)
frame1.pack(expand=True)
a =lms("python library")
label = Label(frame1, text='Welcome to Library', font=('Impact', 22, 'bold') )
label.pack(padx=40, pady=25)
bt1 = Button(frame1, text='Display Books', height = 2, width = 16, command=a.display_books)
bt1.pack(pady=2, padx=60)
bt2 = Button(frame1, text='add books', height = 2, width = 16,command=a.add_books_gui)
bt2.pack(pady=2, padx=20)
bt3 = Button(frame1, text='issue books', height = 2, width = 16,command=a.issue_books_gui)
bt3.pack(pady=2, padx=20)
bt4 = Button(frame1, text='return books', height = 2, width = 16,command=a.return_books)
bt4.pack(pady=2, padx=20)
bt4 = Button(frame1, text='delete books', height = 2, width = 16,command=a.delete_books_gui)
bt4.pack(pady=2, padx=20)
label = Label(frame1, text='')
label.pack(padx=40, pady=25)
root.mainloop()