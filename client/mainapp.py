import tkinter as tk
from library import request_lib
# from library.request_lib import token_require


class Applicaiton(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry('500x300')
        self.title('Login window')
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        tk.Label(text='User Name').grid(padx=50,pady=20,row=0,column=0)
        tk.Entry(textvariable=self.username).grid(row=0,column=1)
        tk.Label(text='Password').grid(padx=50,pady=20,row=1,column=0)
        tk.Entry(textvariable=self.password,show='*').grid(row=1,column=1)
        tk.Button(text='login',command=self.login).grid(row=2)
        tk.Button(text='register',command=self.register).grid(row=2,column=3)
    
    def login(self):
        if len(self.username.get().strip()) > 0 and len(self.password.get()) > 0:
            status_code = request_lib.authenticate(self.username.get(),self.password.get())
            if status_code == 200:
                self.resetall()
                self.Dashboard()
            elif status_code == 401:
                tk.Message(text="username or password wrong").grid(row=4,column=1)
            else:
                tk.Message(text="No user found .Please register ").grid(row=4,column=1)           
        else:
            tk.Message(text="please enter the values").grid(row=4,column=1)

    def register(self):
        if len(self.username.get().strip()) > 0 and len(self.password.get()) > 0:
            status_code = request_lib.register(self.username.get(),self.password.get())
            if status_code == 200:
                tk.Message(text="Registration successful please login").grid(row=4,column=1)
            elif status_code == 409:
                tk.Message(text="User already registered").grid(row=4,column=1)
            else:
                tk.Message(text="Something went wrong").grid(row=4,column=1)

        else:
            tk.Message(text="enter a valid input").grid(row=4,column=1)


        pass

    def resetall(self):
        self.destroy()
        return
        
    def Dashboard(self):
        tk.Tk.__init__(self)
        self.geometry('500x400')
        self.title('Ebill-dashboard')
        res = request_lib.get_resource(uri="http://127.0.0.1:5000/api/resource")
        print(res , type(res))
        for i in res.get("dates"):
            print(i)
            btn = tk.Button(self,text=i,command=self.login)
            btn.pack()


        




if __name__=='__main__':
    try:
        app = Applicaiton()
        app.mainloop()
    except:
        pass    



        



