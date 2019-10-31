from tkinter import *
from tkinter.messagebox import *
from datetime import *
import os
import matplotlib.pyplot as plt
import numpy as np


class livraison:
    def __init__(self, date, livre, repris, init, reel):
        self.date = date
        self.livre = livre
        self.repris = repris
        self.reel = reel
        self.initial = init

    def total_l(self):
        result = 0
        for index in self.livre:
            result += index.quantity
        return result

    def total_r(self):
        result = 0
        for index in self.repris:
            result += index.quantity
        return result
 
            
class bouteille:
    def __init__(self, pro, t, qu, status, date):
        self.product = pro
        self.typ = t
        self.quantity = qu
        self.status = status
        self.date = date

    def set_date(self, date):
        self.date = date

class client:
    def __init__(self, name, adresse, tel, stock, historique):
        self.name = name
        self.adresse = adresse
        self.tel = tel
        self.stock = stock
        self.historique = historique

    def ch_a(self, adresse):
        self.adresse = adresse

    def ch_t(self, tel):
        self.tel = tel

    def add_b(self, b):
        new_b = bouteille(b.product, b.typ, b.quantity, b.status, b.date)
        self.stock.append(new_b)
    
    def add_l(self, l):
        self.historique.append(l)
    
    def r_total(self):
        result = 0
        for index in self.stock:
            result += index.quantity
        return result
    def p_p(self, mode):
        p_p = 0
        p_d = 0
        
        for index in self.stock:
            if index.status == 3:
                p_p+= index.quantity
            if index.status == 4:
                p_d+= index.quantity

            if mode == 0:
                return p_p
            else:
                return p_d

            
    def get_init(self, liv):
        result = self.historique[0].total_l()
        for ind, index in enumerate(self.historique):
            if self.historique[ind -1] == liv:
                return result
            if ind != 0:
                result = result + index.total_l() - index.total_r()
        return -1
                
            
            
        
class App:    
    def __init__(self, master):
        master.title("Gestion des bouteilles")
        self.screen_w, self.screen_h = master.winfo_screenwidth(), master.winfo_screenheight()
        self.screen_w2, self.screen_h2 = int(self.screen_w * 12.5/100), int(self.screen_h * 6.25/100)
        master.geometry("%dx%d+0+0"%(self.screen_w, self.screen_h))
        master.resizable(width=False, height=False)
        self.master = master
        self.frame_master = Frame(master)
        self.frame_master.grid(row = 0, column = 0)
        self.display()
        
    def info_text_d(self):
        p_p = 0
        p_d = 0
        for index in clients[self.c_choice].stock:
            if index.status == 3:
                p_p += index.quantity
            if index.status == 4:
                p_d+= index.quantity
                
        self.c_stock_list_info.delete(0, 'end')
        self.c_stock_list_info.insert('end', 'TOTAL : ' + str(clients[self.c_choice].r_total()))
        self.c_stock_list_info.itemconfig('end',{'fg' : 'white'})
        self.c_stock_list_info.itemconfig('end',{'bg' : 'Gray53'})

        self.c_stock_list_info.insert('end', 'Prêts provisoires : ' + str(p_p))
        self.c_stock_list_info.itemconfig('end',{'fg' : 'white'})
        self.c_stock_list_info.itemconfig('end',{'bg' : 'Gray53'})

        self.c_stock_list_info.insert('end', 'Prêts permanents : ' + str(p_d))
        self.c_stock_list_info.itemconfig('end',{'fg' : 'white'})
        self.c_stock_list_info.itemconfig('end',{'bg' : 'Gray53'})

        self.c_stock_list_info.insert('end', ' ')
        self.c_stock_list_info.itemconfig('end',{'fg' : 'white'})
        self.c_stock_list_info.itemconfig('end',{'bg' : 'azure2'})
        
        self.c_stock_list_info.insert('end', 'Livré : ')
        self.c_stock_list_info.itemconfig('end',{'fg' : 'white'})
        self.c_stock_list_info.itemconfig('end',{'bg' : 'Gray53'})

        for index in clients[self.c_choice].historique[self.client_l.curselection()[0]].livre:
                self.c_stock_list_info.insert('end', "Produit : " + index.product +  '     ' "Type : " + index.typ + '     ' + "Quantité : " + str(index.quantity))
                if index.status == 2:
                    self.c_stock_list_info.itemconfig('end',{'bg' : 'green'})
                if index.status == 3:
                    self.c_stock_list_info.itemconfig('end',{'bg' : 'red'})
                if index.status == 4:
                    self.c_stock_list_info.itemconfig('end',{'bg' : 'orange'})
        base = clients[self.c_choice].historique[0].livre


        for ind in clients[self.c_choice].historique:
            for index in ind.livre:
                ok = 0
                for data in base:
                    if data.product == index.product and data.typ == index.typ and data.status == index.status:
                        data.quantity += index.quantity
                        ok += 1
                if ok == 0:
                    new_c = bouteille(index.product, index.typ, index.quantity, index.status, index.date)
                    base.append(new_c)
                        
        for ind in clients[self.c_choice].historique:
            for index in ind.repris:
                for data in base:
                    ok2 = 0
                    if data.product == index.product and data.typ == index.typ and data.status == index.status:
                        if data.quatity - index.quantity > 0:
                            data.quantity -= index.quantity
                            ok2 += 1
                if ok2 == 1:
                    base.remove(data)
       
        self.c_stock_list_info.insert('end', ' ')
        self.c_stock_list_info.insert('end', 'Repris : ')
        self.c_stock_list_info.itemconfig('end',{'fg' : 'white'})
        self.c_stock_list_info.itemconfig('end',{'bg' : 'Gray53'})
        for index in clients[self.c_choice].historique[self.client_l.curselection()[0]].repris:
            self.c_stock_list_info.insert('end', "Produit : " + index.product +  '     ' "Type : " + index.typ + '     ' + "Quantité : " + str(index.quantity))
            if index.status == 2:
                self.c_stock_list_info.itemconfig('end',{'bg' : 'green'})
                if index.status == 3:
                    self.c_stock_list_info.itemconfig('end',{'bg' : 'red'})
                if index.status == 4:
                    self.c_stock_list_info.itemconfig('end',{'bg' : 'orange'})

    def retour(self):
        for index in self.frame_master.winfo_children():
            index.destroy()
        self.display()
        
    def analyse(self):
        
        name = []
        data = []

        for cl in clients:
            for b in cl.stock:
                ok = 0
                for i, nam in enumerate(name):
                    if b.product + b.typ == nam:
                        data[i] += b.quantity
                        ok = 1
                        break
                if ok ==  0:
                    name.append(b.product + b.typ)
                    data.append(b.quantity)

        for i, index in enumerate(name):
            index += ' : ' + str(data[i])

        figu1, ax1 = plt.subplots()
        ax1.pie(data, labels=name, autopct='%1.1f%%', startangle=90)
        ax1.axis('equal')
        mng = plt.get_current_fig_manager()
        mng.full_screen_toggle()
        plt.show()
        
        
    def display(self):

        self.clients_list_frame = LabelFrame(self.frame_master, text = "Clients", font = ("Helvetica", 15, 'bold'), relief=SUNKEN, borderwidth=5)
        self.clients_list_frame.grid(row = 0, column = 0, padx=10)

        self.clients_list = Listbox(self.clients_list_frame, bg='Gray90',  font = ("Helvetica", 12, "bold"), width=int(15*self.screen_w2/100), height= int(70*self.screen_h2/100))
        self.clients_list.grid(row = 0, column = 0, sticky = W)

        self.add_client = Button(self.clients_list_frame, text="Nouveau client", font=("Arial", 12, 'bold'), command = lambda:self.new_client(), width = int(5 * self.screen_w2/100), height = int(1 * self.screen_h2/100))
        self.add_client.grid(row = 1, column = 0, sticky=W)

        self.rm_clien = Button(self.clients_list_frame, text="Supprimer", font=("Arial", 12, "bold"), command = lambda:self.rm_client(), width = int(4 * self.screen_w2/100), height = int(1 * self.screen_h2/100))
        self.rm_clien.grid(row = 1, column = 0, sticky = E)

        self.stock_list_frame = LabelFrame(self.frame_master, text="Stock", font = ("Helvetica", 15, 'bold'))
        self.stock_list_frame.grid(row = 0, column = 2, padx=10)

        self.stock_list = Listbox(self.stock_list_frame, bg='Gray90', relief=SUNKEN, borderwidth=5,  font = ("Helvetica", 12, "bold"), width=int(20*self.screen_w2/100), height= int(65*self.screen_h2/100))
        self.stock_list.grid(row = 0, column = 0)

        self.client_frame = LabelFrame(self.frame_master,font = ("Helvetica", 15, "bold"), width = int(40*self.screen_w2/100), height = int(70 * self.screen_h2/100))

        Button(self.stock_list_frame, text = "Analyse des données", command = lambda:self.analyse()).grid(row = 1, column = 0)

        Button(self.stock_list_frame, text = "Ajouter", command = lambda:self.Ajouter_b()).grid(row = 2, column = 0, sticky=W)

        Button(self.stock_list_frame, text = 'Retirer', command = lambda:self.Retirer_b()).grid(row = 2, column = 0, sticky=E)
        
        i = 0
        for i, index in enumerate(clients):
            self.clients_list.insert(i, "Nom : " + index.name)
            for liv in index.historique:
                for bout in liv.livre:
                    if bout.status == 3:
                        self.clients_list.itemconfig(i, {'bg' : 'red','fg':'white'})
            
        self.clients_list.bind('<ButtonRelease-1>', lambda event: self.display_client())
        for i, typ in enumerate(stock_gd):
            self.stock_list.insert(i, "Produit : " + typ.product + "  /  Type : " + typ.typ + ' / Quantité ' + str(typ.quantity))

        logo = PhotoImage(file = 'data/src/logo.png')
        canv_logo = Canvas(self.client_frame, bg = 'white', width = int(450*self.screen_w2/100), height = int(1200 * self.screen_h2/100))

        canv_logo.photo = logo
        canv_logo.create_image(210,  250, anchor=NW, image=logo)
        canv_logo.grid(row = 0, column = 0) 
        self.client_frame.grid(row = 0, column = 1)
        
        if alert != '':
            showinfo('Alerte', alert)

    def rm_client(self):
        os.remove("data/clients/" + clients[self.name_choice].name)
        clients.remove(clients[self.name_choice])
        self.clients_list.delete(self.name_choice)
        for obj in self.client_frame.winfo_children():
            obj.destroy()
        self.client_frame.config(text = "")
        logo = PhotoImage(file = 'data/src/logo.png')
        canv_logo = Canvas(self.client_frame, bg = 'white', width = int(455*self.screen_w2/100), height = int(1200 * self.screen_h2/100))

        canv_logo.photo = logo
        canv_logo.create_image(210,  250, anchor=NW, image=logo)
        canv_logo.grid(row = 0, column = 0) 
        
    def display_client(self):
        self.name_choice = self.clients_list.curselection()[0]
        place = 0
        choice = int(self.clients_list.curselection()[0])

        self.c_choice = choice
        for obj in self.client_frame.winfo_children():
            obj.destroy()
        
        self.client_frame.config(text = clients[choice].name)
        self.client_frame.grid(row = 0, column = 1, padx=10)

        
        if clients[choice].adresse != None:
            Label(self.client_frame, text = "Adresse : " + clients[choice].adresse, font = ("Helvetica", 10, 'bold')).grid(row = place, column = 0, sticky = W)
            place +=1
        if clients[choice].tel != None:
            Label(self.client_frame, text = "Telephone : " + clients[choice].tel , font = ("Helvetica", 10, 'bold')).grid(row =  place, column = 0, sticky = W)
            place += 1

##################Historique###################        
        self.client_l = Listbox(self.client_frame, bg='Gray91', font = ("Helvetica", 12, 'bold'), width = int(50 * self.screen_w2/100), height = int(35 * self.screen_h2/100))

        obj_i = 0
        initial = clients[choice].historique[0].total_l()

        for ind, obj in enumerate(clients[choice].historique):
            string = str_date(obj.date) + 10*' ' + 'initial : ' + str(obj.initial)
            space = 12 - len(str(obj.initial))
            string = string + space * ' '  +   "Reel : " +  str(obj.reel)
            space = 12 - len(str(obj.reel))
            string = string + space * ' ' + 'Livraison : ' + str(obj.total_l())
            space = 12 - len(str(obj.total_r()))
            string = string + space * ' '   +'Reprise : ' + str(obj.total_r())
            space = len(str(obj.total_r()))
            string = string + space * ' '

            self.client_l.insert(obj_i, string)
            obj_i+=1

            for index in obj.livre:
                if index.status == 2:
                    self.client_l.itemconfig(obj_i - 1 , {'bg' : 'green'})
                    self.client_l.itemconfig(obj_i - 1, {'fg' : 'white'})
                    break
                if index.status == 3:
                    self.client_l.itemconfig(obj_i - 1 , {'bg' : 'red'})
                    self.client_l.itemconfig(obj_i - 1, {'fg' : 'white'})
                    break
                if index.status == 4:
                    self.client_l.itemconfig(obj_i - 1 , {'bg' : 'orange'})
                    self.client_l.itemconfig(obj_i - 1, {'fg' : 'white'})
                    break
        self.client_l.grid(row = place, column = 0, pady = 50)
        self.client_l.bind('<ButtonRelease-1>', lambda event: self.info_text_d())
        place += 1

############################################

        self.c_info_frame = Frame(self.client_frame, width = int(50 * self.screen_w2/100), height = int(20 * self.screen_h2/100), relief = SUNKEN )
        self.c_info_frame.grid(row = place, column = 0, sticky=W+N)
            
        self.c_stock_list = Listbox(self.client_frame, bg='Gray91', font = ('Helvetica', 12, 'bold'), width = int(20 * self.screen_w2/100), height = int(20 * self.screen_h2/100))

        self.c_stock_list_info = Listbox(self.c_info_frame, bg='Gray91', font = ('Helvetica', 12, 'bold'), width = int(20 * self.screen_w2/100), height = int(20 * self.screen_h2/100))

        for i in range(0, 10):
            self.c_stock_list_info.insert(i, str(i))

        self.c_stock_list_info.grid(row = 0, column = 1)
        p_p = 0
        p_d = 0
        for j, index in enumerate(clients[choice].stock):
            self.c_stock_list.insert(j, "Produit : " + index.product + ' ' + "     Type : " + index.typ + ' ' + "     Quantite :" + str(index.quantity))
            if index.status == 2:
                self.c_stock_list.itemconfig(j , {'bg':'green'})
                self.c_stock_list.itemconfig(j, {'fg':'white'})
            if index.status == 3:
                p_p+= index.quantity
                self.c_stock_list.itemconfig(j , {'bg':'red'})
                self.c_stock_list.itemconfig(j, {'fg':'white'})
            if index.status == 4:
                p_d+=index.quantity
                self.c_stock_list.itemconfig(j , {'bg':'orange'})
                self.c_stock_list.itemconfig(j, {'fg':'white'})
                
        self.c_stock_list.grid(row = place, column = 0, sticky=E)
        place += 1
        
        self.c_stock_list_info.delete(0, 'end')
        self.c_stock_list_info.insert('end', 'TOTAL : ' + str(clients[self.c_choice].r_total()))
        self.c_stock_list_info.itemconfig('end',{'fg' : 'white'})
        self.c_stock_list_info.itemconfig('end',{'bg' : 'Gray53'})

        self.c_stock_list_info.insert('end', 'Prêts provisoires : ' + str(p_p))
        self.c_stock_list_info.itemconfig('end',{'fg' : 'white'})
        self.c_stock_list_info.itemconfig('end',{'bg' : 'Gray53'})

        self.c_stock_list_info.insert('end', 'Prêts permanents : ' + str(p_d))
        self.c_stock_list_info.itemconfig('end',{'fg' : 'white'})
        self.c_stock_list_info.itemconfig('end',{'bg' : 'Gray53'})

        Button(self.client_frame, text = 'Livraison', command = lambda:self.ajouter()).grid(row = place, column = 0, pady = 20)

    def Ajouter_b(self):
        self.A_b = Toplevel(self.master)
        self.A_b.title("Ajouter")
        self.A_b.resizable(width=False, height=False)
        self.A_app = Ajouter_b(self.A_b)
        self.A_b.mainloop()

    def Retirer_b(self):
        self.R_b = Toplevel(self.master)
        self.R_b.title("Retirer")
        self.R_b.resizable(width=False, height=False)
        self.R_app = Retirer_b(self.R_b)
        self.R_b.mainloop()
    
    def ajouter(self):
        self.A_r = Toplevel(self.master)
        self.A_r.title("Livraison")
        #A_r.geometry(str(int(35 * self.screen_w/100)) + 'x' + str(int(40 * self.screen_h/100)))
        self.A_r.resizable(width=False, height=False)
        self.A_app = Ajouter(self.A_r, self.name_choice)
        self.A_r.mainloop()
        
    def new_client(self):
        self.Add = Toplevel(self.master)
        self.Add.title("Nouveau client")
        self.Add.resizable(width = False, height = False)
        Add_app = New_c(self.Add)
        self.Add.mainloop()
        
        
#########################################################
class New_c:
    def __init__(self, master):
        self.master = master
        self.frame_master = Frame(master)
        self.frame_master.grid(row = 0, column = 0)
        self.b_list = []
        self.display()
        
    def display(self):
        self.name = StringVar()
        self.phone = StringVar()
        self.addr = StringVar()
        self.date = StringVar()
        
        #name_e = Entry(self.fra
        self.value_frame = Frame(self.frame_master)
        self.value_frame.grid(row =  0, column = 0, padx = 10, pady = 5)
        self.liv_frame = Frame(self.frame_master)
        self.liv_frame.grid(row = 0, column = 1, padx = 10, pady = 5)

        Label(self.value_frame, text = "Nom").grid(row = 0, column = 0) 
        self.name_e = Entry(self.value_frame, textvariable = self.name).grid(row = 1, column = 0)
        Label(self.value_frame, text = "Numéro de téléphone").grid(row = 2, column = 0)
        self.phone_e = Entry(self.value_frame, textvariable = self.phone).grid(row = 3, column = 0)
        Label(self.value_frame, text = 'Adresse').grid(row  = 4, column = 0)
        self.addr_e = Entry(self.value_frame, textvariable = self.addr).grid(row = 5, column = 0)
        Label(self.value_frame, text = 'Date').grid(row = 6, column = 0)
        self.date_e = Entry(self.value_frame, textvariable = self.date).grid(row = 7, column = 0)

        
        self.list_b_l=Listbox(self.liv_frame, font=("Helvetica", 12, 'bol\
d'), width = int(10 * app.screen_w2/100), height=(int(15*app.screen_h2/100)))             
                                                                                
        for ind, index in enumerate (b_type):                                   
            self.list_b_l.insert(ind, index.product + ' ' + index.typ)          
        self.list_b_l.grid(row = 0, column = 1)                                 
        self.list_b_l.bind('<ButtonRelease>', lambda event:self.a_confirmer())  

        self.list_choice = Listbox(self.liv_frame, bg = 'Gray92', font=('Helvetica', 12, 'bold'), width = int(10 * app.screen_w2/100), height=(int(15*app.screen_h2/100)))

        self.number = Spinbox(self.liv_frame, from_=0, to=10)
        self.conf_button = Button(self.liv_frame, text='confirmer', command = lambda:self.a_confirmer2())      

    def a_confirmer(self):
        self.number.grid(row = 6, column = 1, pady = 5)
        self.list_choice.grid(row = 8, column = 1, sticky=E, pady = 5)
        self.conf_button.grid(row = 7, column = 1)
        Button(self.liv_frame, text = "Creer", command = lambda: self.create_client()).grid(row = 10, column = 1)
        
        #new_b = bouteille(b_type[value].product, b_type[value].typ, b_type[value], 

    def a_confirmer2(self):
        if int(self.number.get()) <= 0:
            showinfo("Erreur", "Vous ne pouvez pas ajouter 0 bouteille")
            return 0
        
        ok = 0
        value = self.list_b_l.curselection()[0]
        for index in stock_gd:
            if index.product == b_type[value].product and index.typ == b_type[value].typ and index.quantity < int (self.number.get()):
                showinfo("Erreur", "Il ne reste plus que " + str(index.quantity) + " bouteilles de ce type")
                return 0
            if index.product == b_type[value].product and index.typ == b_type[value].typ and index.quantity >= int (self.number.get()):
                ok = 1
        if ok == 0:
            showinfo("Erreur", "Ce produit n'est pas disponible")
            return 0
        
        new_b = bouteille(b_type[value].product, b_type[value].typ, int(self.number.get()), 1, 0)
        self.b_list.append(new_b)
        for i, index in enumerate(self.b_list):                                             
            self.list_choice.insert(i, index.product + ' ' + index.typ + ' : '+ str (index.quantity))                                                                                         
             
    def create_client(self):
        name = self.name.get()
        adresse = self.addr.get()
        phone = self.phone.get()
        date = self.date.get()

        init = 0
        new_l_l = []
        stock = []
        rep = []
        
        if len(name) == 0:
            showinfo("Alerte", "Un nom est nécessaire")
            return 0

        for data in clients:
            if name == data.name:
                showinfo("Alerte", "Ce nom est déjà dans la liste")
                return 0
        
        try:
            day, month, year = date.split('/')
            date = datetime(int(year), int(month), int(day))
            
        except:
            showinfo('Alerte', 'Une date valide est necessaire jour/mois/année')
            return 0
        
        for index in self.b_list:
            init += index.quantity
            index.set_date(date)
            
            
        new_l = livraison(date, self.b_list, rep, init, init)
        new_l_l.append(new_l)
        
        new_c = client(name, adresse, phone, self.b_list, new_l_l)
        clients.append(new_c)

        for index in self.b_list:
            for st in stock_gd:
                if index.product == st.product and index.typ == st.typ:
                    st.quantity -= index.quantity
                    if st.quantity < 1:
                        stock_gd.remove(st)

        app.display()
        rewrite_s()
        rewrite()
        app.Add.destroy()    
        

class Ajouter_b:
    def __init__(self, master):
        self.master = master
        self.frame_master = Frame(master)
        self.frame_master.grid(row = 0, column = 0)
        self.display()

    def display(self):

        self.list_a = Listbox(self.frame_master, font = ("Helvetica", 12, 'bold'), width = int(10 * app.screen_w2/100), height=(int(15*app.screen_h2/100)))

        for i, index in enumerate(b_type):
            self.list_a.insert(i, index.product + ' / ' + index.typ)
        self.list_a.grid(row = 0, column = 0)
        self.list_a.bind('<ButtonRelease>', lambda event:self.ajouter_f())
        
    def ajouter_f(self):
        choice = int(self.list_a.curselection()[0])
        number = StringVar()
                
        self.spin = Spinbox(self.frame_master, textvariable = number,  from_=0, to = 100)
        self.spin.grid(row = 0, column = 1)
        Button(self.frame_master, text="Ajouter", command = lambda:self.confirm(choice, int(number.get()))).grid(row=0, column = 1, sticky=S)

    def confirm(self, choice, number):
        ok = 0
        for index in stock_gd:
            if index.product == b_type[choice].product and index.typ == b_type[choice].typ:
                index.quantity += number
                ok = 1
        if ok == 0:
            new_b = bouteille(b_type[choice].product, b_type[choice].typ, number, 0, 0)
            stock_gd.append(new_b)
            app.stock_list.delete(0, 'end')
            for i, typ in enumerate(stock_gd):
                app.stock_list.insert(i, "Produit : " + typ.product + "  /  Type : " + typ.typ)
            rewrite_s()

            
class Retirer_b:
    def __init__(self, master):
        self.master = master
        self.frame_master = Frame(master)
        self.frame_master.grid(row = 0, column = 0)
        self.display()

    def display(self):

        self.list_a = Listbox(self.frame_master, font = ("Helvetica", 12, 'bold'), width = int(10 * app.screen_w2/100), height=(int(15*app.screen_h2/100)))

        for i, index in enumerate(stock_gd):
            self.list_a.insert(i, index.product + ' / ' + index.typ)
        self.list_a.grid(row = 0, column = 0)
        self.list_a.bind('<ButtonRelease>', lambda event:self.ajouter_f())
        
    def ajouter_f(self):
        number = StringVar()
        choice = int(self.list_a.curselection()[0])
        self.spin = Spinbox(self.frame_master, textvariable = number,  from_=0, to = 100)
        self.spin.grid(row = 0, column = 1)
        Button(self.frame_master, text="Ajouter", command = lambda:self.confirm(choice, int(number.get()))).grid(row=0, column = 1, sticky=S)

    def confirm(self, choice, number):
        for index in stock_gd:
            if index.product == b_type[choice].product and index.typ == b_type[choice].typ:
                index.quantity -= number

        for index in stock_gd:
            if index.quantity <= 0:
                stock_gd.remove(index)

        app.stock_list.delete(0, 'end')
        for i, typ in enumerate(stock_gd):
            app.stock_list.insert(i, "Produit : " + typ.product + "  /  Type : " + typ.typ)
            
        rewrite_s()

        
def rewrite_s():
    data_file = open('data/stock.txt', 'w')
    for index in stock_gd:
        data_file.write(index.product + '/' + index.typ + '/' + str(index.quantity) + '\n')
    app.stock_list.delete(0, 'end')

    for i,index in enumerate(stock_gd):
        app.stock_list.insert(i, "Produit : " + index.product + "  /  Type : " + index.typ + ' / Quantité ' + str(index.quantity))

class Ajouter:
    def __init__(self, master, choice):
        self.master = master
        self.frame_master = Frame(master)
        self.frame_master.grid(row = 0, column = 0)
        self.choice = choice
        self.s_w = app.screen_w2
        self.s_h = app.screen_h2
        self.b_list = []
        self.real_l  = []
        self.display()
        
    def confirm(self, mode):
        li = 0
        re = 0
        ok = 0
        date = StringVar()

        if mode == 1:
            for i in self.b_list:
                ok = 0
                for j in self.real_l:
                    if i.product == j.product and i.typ == j.typ and j.status == i.status:
                        j.quantity += i.quantity
                        ok = 1
                if ok == 0:
                    new_b = bouteille(i.product, i.typ, i.quantity, i.status, i.date)
                    self.real_l.append(new_b)
                
            for index in self.real_l:
                if index.status == 1:
                    li += 1
                else:
                    re += 1
                
        for obj in self.frame_master.winfo_children():
            obj.destroy()

        self.a_frame = LabelFrame(self.frame_master, text = "Livré")
        self.r_frame = LabelFrame(self.frame_master, text = "Repris")
        self.a_frame.grid(row = 0, column = 0)
        self.r_frame.grid(row = 0, column = 1)

        self.list_resume_a = Listbox(self.a_frame, font = ("Helvetica", 12, 'bold'), width = int(10 * self.s_w/100), height=(int(15*self.s_h/100)))
        self.list_resume_r = Listbox(self.r_frame, font = ("Helvetica", 12, 'bold'), width = int(10 * self.s_w/100), height=(int(15*self.s_h/100)))

        for i, index in enumerate(self.real_l):
            if index.status == 1:
                self.list_resume_a.insert(i,str(index.quantity) + ' : ' + index.product + ' ' + index.typ)
            if index.status == -1:
                self.list_resume_r.insert(i,str(index.quantity) + ' : ' + index.product + ' ' + index.typ)
        self.list_resume_a.grid(row = 0, column = 0)
        self.list_resume_r.grid(row = 0, column = 0)

        Label(self.frame_master, text = "Date :").grid(row = 1, column = 0, sticky=W)
        date_e = Entry(self.frame_master, textvariable = date)
        date_e.grid(row = 2, column = 0, pady = 2, sticky=W)

        Button(self.frame_master, text = "Prêt provisoire", command = lambda:self.pret(date.get(),1)).grid(row = 1, column = 1, pady = 5)
        Button(self.frame_master, text = "Prêt définitif", command = lambda:self.pret(date.get(),2)).grid(row = 2, column = 1, pady = 5)
        Button(self.frame_master, text = "Avenant", command = lambda:self.avenant(date.get())).grid(row = 3, column = 1, pady = 5)
        Button(self.frame_master, text = "Confirmer", command = lambda:self.new_liv(date.get())).grid(row = 4, column = 1, pady = 5)


    def pret(self,date, mode):
        try:
            day, month, year = date.split('/')
            date = datetime(int(year), int(month), int(day))
        except:
            showerror("Erreur", "Une date valide est nécessaire")
            return 0
        
        for obj in self.frame_master.winfo_children():
            obj.destroy()
        Button(self.frame_master, text='annuler', command = lambda:self.confirm(0)).grid(row = 0, column = 0)

        self.pret_list = []
        self.list_pret = Listbox(self.frame_master,  font = ("Helvetica", 12, 'bold'), width = int(10 * self.s_w/100), height=(int(15*self.s_h/100)))
        for i, index in enumerate(self.real_l):
            if index.status == 1:
                self.list_pret.insert(i,str(index.quantity) + ' : ' + index.product + ' ' + index.typ)
        self.list_pret.grid(row = 1, column = 0)
        self.list_pret_c = Listbox(self.frame_master, font = ("Helvetica", 12, 'bold'), width = int(10 * self.s_w/100), height=(int(15*self.s_h/100)))

        self.list_pret.bind('<ButtonRelease>', lambda event: self.pret_confirm(date, mode))


    def avenant(self, date):
        try:
            day, month, year = date.split('/')
            date = datetime(int(year), int(month), int(day))
        except:
            showerror("Erreur", "Une date valide est nécessaire")
            return 0
        
        for obj in self.frame_master.winfo_children():
            obj.destroy()
        Button(self.frame_master, text='annuler', command = lambda:self.confirm(0)).grid(row = 0, column = 0)

        self.av_list = []
        self.list_av = Listbox(self.frame_master,  font = ("Helvetica", 12, 'bold'), width = int(10 * self.s_w/100), height=(int(15*self.s_h/100)))
        for i, index in enumerate(self.real_l):
            if index.status == 1:
                self.list_av.insert(i,str(index.quantity) + ' : ' + index.product + ' ' + index.typ)
        self.list_av.grid(row = 1, column = 0)
        self.list_av_c = Listbox(self.frame_master, font = ("Helvetica", 12, 'bold'), width = int(10 * self.s_w/100), height=(int(15*self.s_h/100)))

        self.list_av.bind('<ButtonRelease>', lambda event: self.avenant_confirm(date))

    def pret_confirm(self, date, mode):
        number = StringVar()
        self.number_choice = int(self.list_pret.curselection()[0])
        self.list_pret_c.grid(row = 2, column = 0, sticky=N )
        self.pret_sb = Spinbox(self.frame_master, textvariable = number, from_=1, to=self.real_l[self.number_choice].quantity)
        Button(self.frame_master, text='Ajouter',command= lambda: self.pret_confi(number.get())).grid(row =  2, column = 1, sticky=S)
        self.pret_sb.grid(row = 2, column = 1)
        Button(self.frame_master, text = 'Confirmer', command = lambda: self.pret_final(date, mode)).grid(row = 4, column = 1)

    def avenant_confirm(self, date):
        number = StringVar()
        self.number_choice = int(self.list_av.curselection()[0])
        self.list_av_c.grid(row = 2, column = 0, sticky=N )
        self.avenant_sb = Spinbox(self.frame_master, textvariable = number, from_=1, to=self.real_l[self.number_choice].quantity)
        Button(self.frame_master, text='Ajouter',command= lambda: self.avenant_confi(number.get())).grid(row =  2, column = 1, sticky=S)
        self.avenant_sb.grid(row = 2, column = 1)
        Button(self.frame_master, text = 'Confirmer', command = lambda: self.avenant_final(date)).grid(row = 4, column = 1)

    def pret_final(self, date, mode):
         for index in self.pret_list:
            for real in self.real_l:
                if index.product == real.product and index.typ == real.typ:
                    if index.quantity < real.quantity:
                        real.quantity -= index.quantity
                        if mode == 1:
                            new_b = bouteille(real.product, real.typ, index.quantity, 3, real.date)
                        else:
                            new_b = bouteille(real.product, real.typ, index.quantity, 4, real.date)
                            
                        self.real_l.append(new_b)
                    else:
                        self.real_l.remove(real)
                        if mode == 1:
                            new_b = bouteille(real.product, real.typ, index.quantity, 3, real.date)
                        else:
                            new_b = bouteille(real.product, real.typ, index.quantity, 4, real.date)
                        self.real_l.append(new_b)
            self.new_liv(str_date(date))
   
    def avenant_final(self, date):
        for index in self.av_list:
            for real in self.real_l:
                if index.product == real.product and index.typ == real.typ:
                    if index.quantity < real.quantity:
                        real.quantity -= index.quantity
                        new_b = bouteille(real.product, real.typ, index.quantity, 2, real.date)
                        self.real_l.append(new_b)
                    else:
                        self.real_l.remove(real)
                        new_b = bouteille(real.product, real.typ, index.quantity, 2, real.date)
                        self.real_l.append(new_b)
        self.new_liv(str_date(date))

    def pret_confi(self, number):
        new_b = bouteille(self.real_l[self.number_choice].product, self.real_l[self.number_choice].typ, int(number), self.real_l[self.number_choice].status, self.real_l[self.number_choice].date)
        self.pret_list.append(new_b)
        self.list_pret_c.insert(len(self.pret_list), self.real_l[self.number_choice].product + ' ' + self.real_l[self.number_choice].typ + ' ' + str(number))        

    def avenant_confi(self, number):
        new_b = bouteille(self.real_l[self.number_choice].product, self.real_l[self.number_choice].typ, int(number), self.real_l[self.number_choice].status, self.real_l[self.number_choice].date)
        self.av_list.append(new_b)
        self.list_av_c.insert(len(self.av_list), self.real_l[self.number_choice].product + ' ' + self.real_l[self.number_choice].typ + ' ' + str(number))        

    def new_liv(self, date):
        try:
            day, month, year = date.split('/')
            date = datetime(int(year), int(month), int(day))
        except:
            showerror("Erreur", "Date invalide")
            return 0

        for i in self.real_l:
            i.set_date(date)
            
        liv = []
        rep = []
        init = clients[self.choice].historique[-1].initial
        reel = clients[self.choice].historique[-1].reel
        av_i = 0
        
        for index in self.real_l:
            if index.status != -1:
                new_b = bouteille(index.product, index.typ, index.quantity, index.status, index.date)
                liv.append(new_b)
                reel += index.quantity
                ve = 0
                for data in clients[self.choice].stock:
                    if data.product == index.product and data.typ == index.typ and data.status == index.status:
                        ve = 1
                        data.quantity += index.quantity
                if ve == 0:
                    new_b = bouteille(index.product, index.typ, index.quantity, index.status, index.date)
                    clients[self.choice].stock.append(new_b)
                        
            else:
                rep.append(index)
                reel -= index.quantity
                for data in clients[self.choice].stock:
                    if data.product == index.product and data.typ == index.typ:
                        if data.quantity - index.quantity > 0:
                            data.quantity -= index.quantity
                        else:
                            clients[self.choice].stock.remove(data)

            if index.status == 2:
                av_i += index.quantity
                
        new_l = livraison(date, liv, rep, init + av_i, reel)
        clients[self.choice].historique.append(new_l)

        app.client_l.delete(0, 'end') 
        for ind, obj in enumerate(clients[self.choice].historique):
            string = str_date(obj.date) + 10*' ' + 'initial : ' + str(obj.initial)
            space = 12 - len(str(obj.initial))
            string = string + space * ' '  +   "Reel : " +  str(obj.reel)
            space = 12 - len(str(obj.reel))
            string = string + space * ' ' + 'Livraison : ' + str(obj.total_l())
            space = 12 - len(str(obj.total_r()))
            string = string + space * ' '   +'Reprise : ' + str(obj.total_r())
            space = len(str(obj.total_r()))
            string = string + space * ' '

            app.client_l.insert(ind, string)

            
            for index in obj.livre:
                if index.status == 2:
                    app.client_l.itemconfig(ind , {'bg' : 'green'})
                    app.client_l.itemconfig(ind, {'fg' : 'white'})
                    break
                
                if index.status == 3:
                    app.client_l.itemconfig(ind , {'bg' : 'red'})
                    app.client_l.itemconfig(ind, {'fg' : 'white'})
                    break
                
                if index.status == 4:
                    app.client_l.itemconfig(ind , {'bg' : 'orange'})
                    app.client_l.itemconfig(ind, {'fg' : 'white'})
                    break
                
            app.c_stock_list.delete(0, 'end')
            for j, index in enumerate(clients[self.choice].stock):
                app.c_stock_list.insert(j, "Produit : " + index.product + ' ' + "     Type : " + index.typ + ' ' + "     Quantite :" + str(index.quantity))
                
                if index.status == 2:
                    app.c_stock_list.itemconfig(j, {'bg':'green'})
                    app.c_stock_list.itemconfig(j, {'fg':'white'})
                if index.status == 3:
                    app.c_stock_list.itemconfig(j, {'bg':'red'})
                    app.c_stock_list.itemconfig(j, {'fg':'white'})
                if index.status == 4:
                    app.c_stock_list.itemconfig(j, {'bg':'orange'})
                    app.c_stock_list.itemconfig(j, {'fg':'white'})
            total = 0
            for index in clients[self.choice].stock:
                total += index.quantity


        for index in self.real_l:
            for st in stock_gd:
                if index.product == st.product and index.typ == st.typ:
                    if index == 1:
                        st.quantity -= index.quantity
                        if st.quantity < 1:
                            stock_gd.remove(st)

        
        for index in self.real_l:
            ok = 0
            for st in stock_gd:
                if index.product == st.product and index.typ == st.typ:
                    ok = 1
                    st.quantity += index.quantity
            if ok == 0:
                new_b = bouteille(index.product, index.typ, index.quantity, 0, 0)
                stock_gd.append(new_b)

        
                        
        rewrite_s()
        rewrite()
        app.A_r.destroy()
        
    def display(self):
        Button(self.frame_master, text = "Confirmer", command = lambda:self.confirm(1)).grid(row = 0, column = 1, sticky=E)
        Label(self.frame_master,text = clients[(self.choice)].name).grid(row = 0, column = 0, sticky=W)

        self.frame_livraison = LabelFrame(self.frame_master, text = "Livré".encode('latin1'))
        self.frame_livraison.grid(row = 1, column = 0, padx = 5, pady = 0)

        self.list_b_l=Listbox(self.frame_livraison, font=("Helvetica", 12, 'bold'), width = int(10 * self.s_w/100), height=(int(15*self.s_h/100)))

        for ind, index in enumerate (b_type):
            self.list_b_l.insert(ind, index.product + ' ' + index.typ)
        self.list_b_l.grid(row = 0, column = 0)
        self.list_b_l.bind('<ButtonRelease>', lambda event:self.a_confirmer())
        
        self.a_result=Listbox(self.frame_livraison, font=("Helvetica", 11, "bold"), width = int(15 * self.s_w/100), height=(int(10*self.s_h/100)), bg = "Gray90")
        self.a_result.grid(row = 1, column = 0, pady = 15)
        #####


        self.frame_repris = LabelFrame(self.frame_master, text = "Repris")
        self.frame_repris.grid(row = 1, column = 1, padx = 5, pady = 0)
               
        self.list_b_r=Listbox(self.frame_repris, font=("Helvetica", 12, 'bold'), width = int(10 * self.s_w/100), height=(int(15*self.s_h/100)))

        for ind, index in enumerate(clients[self.choice].stock):
            self.list_b_r.insert(ind, index.product + ' ' + index.typ)
        self.list_b_r.grid(row = 0, column = 0 , pady = 15)
        self.list_b_r.bind('<ButtonRelease>', lambda event:self.r_confirmer())
        

        self.r_result=Listbox(self.frame_repris, font=("Helvetica", 12, 'bold'), width = int(15 * self.s_w/100), height=(int(10*self.s_h/100)), bg="Grey90")
        self.r_result.grid(row = 1, column = 0, pady = 15)

    def r_confirmer(self):
        b = self.list_b_r.curselection()[0]
        b_p = clients[self.choice].stock[b].product
        b_t = clients[self.choice].stock[b].typ
        b_q = clients[self.choice].stock[b].quantity
        a_numb = StringVar()
        
        conframe = Frame(self.frame_repris)
        conframe.grid(row = 0, column = 1)

        self.r_spin = Spinbox(conframe, textvariable = a_numb, from_=0, to=b_q).grid(row = 0, column = 0)
        Button(conframe, text='Confirmer', command = lambda:self.new_r(b_p,b_t, a_numb.get())).grid(row = 1, column = 0, sticky=S)

    def new_r(self, b_p, b_t, numb):
        if int(numb) < 0:
            showinfo("Erreur", "Vous ne pouvez pas ajouter 0 bouteille")
            return 0
        new_b = bouteille(b_p, b_t, int(numb), -1, datetime.now())
        self.b_list.append(new_b)
        self.display_result(-1)
        
    def a_confirmer(self):
        b =  self.list_b_l.curselection()[0]
        b_p = b_type[b].product
        b_t = b_type[b].typ
        a_numb = StringVar()

        conframe = Frame(self.frame_livraison)
        conframe.grid(row = 0, column = 1)
        
        self.a_spin = Spinbox(conframe, textvariable = a_numb, from_=1, to=999).grid(row = 0, column = 0)
        Button(conframe, text='Confirmer', command = lambda:self.new_a(b_p,b_t, a_numb.get())).grid(row = 1, column = 0, sticky=S)
        
    def new_a(self, b_p, b_t, numb):
        if int(numb) < 1 :
            showinfo("Erreur", "Vous ne pouvez pas ajouter 0 bouteille") 
            return 0
        ok = 0
        for index in stock_gd:
            if index.product == b_p and index.typ == b_t and int(numb) > index.quantity:
                showinfo("Erreur", "Il ne reste plus que " + str(index.quantity) + " bouteilles de ce type")
                return 0
            if index.product == b_p and index.typ == b_t and int(numb) <= index.quantity:
                ok = 1
                
        if ok == 0:
            showinfo("Erreur", "Ce produit n'est pas disponible")
            return 0
               

        new_b = bouteille(b_p, b_t, int(numb), 1, 0)
        self.b_list.append(new_b)
        self.display_result(1)
        
    def display_result(self, mode):
        if mode == 1:
            self.a_result.delete(0, 'end')
            for ind, index in enumerate(self.b_list):
                if index.status == 1:
                    j = 10 - len(str(index.quantity))
                    self.a_result.insert(ind,'Quantité : ' + str(index.quantity) + j *' ' + index.product + ' ' + index.typ)
            self.a_result.grid(row = 1, column = 0)
        else:
            self.r_result.delete(0, 'end')
            for ind, index in enumerate(self.b_list):
                if index.status == -1:
                    j = 10 - len(str(index.quantity))
                    self.r_result.insert(ind,'Quantité : ' + str(index.quantity) + j *' ' + index.product + ' ' + index.typ)
            self.r_result.grid(row = 1, column = 0)
#########################################################

def rewrite():
    all_f = sorted(os.listdir('data/clients'))

    ##open.. 
    for index in clients:
        data_file = open('data/clients/' + index.name, 'w')

        ##name ...
        data_file.write('@T|' + index.tel + '\n@A|' + index.adresse + '\n{\n')

        ##stock..
        for bout in index.stock:
            data_file.write(bout.product + '|' + bout.typ + '|' + str(bout.quantity) + '|' + str(bout.status) + '|' + str_date(bout.date) + '\n')
        data_file.write('}\n[\n')
        
        ##historique
        for liv in index.historique:
                data_file.write(str_date(liv.date) + '|')

                if liv.livre != []:
                    for i, livre in enumerate(liv.livre):
                        data_file.write(livre.product + '/' + livre.typ + ':' + str(livre.quantity) + ':' + str(livre.status))
                        if i + 1 == len(liv.livre):
                            data_file.write('|')
                        else:
                            data_file.write(',')
                else:
                    data_file.write('0|')
                            
                if liv.repris != []:
                    for j, repris in enumerate(liv.repris):
                        data_file.write(repris.product + '/' + repris.typ + ':' + str(repris.quantity))
                        if j + 1 == len(liv.repris):
                            data_file.write('|')
                        else:
                            data_file.write(',')
                else:
                    data_file.write('0|')
                        
                data_file.write(str(liv.initial) + '|' + str(liv.reel) + '\n')
        data_file.write(']')
    
                
def parser():
    all_f = sorted(os.listdir('data/clients'))

    with open("data/stock.txt", 'r') as file:
        stock_b = file.readlines()
    for index in stock_b:
        product, typ, quant = index.split('/')
        new_b = bouteille(product, typ, int(quant), 0, 0)
        stock_gd.append(new_b)

    with open("data/type.txt", 'r') as file:
        type_file = file.readlines()
        type_file = sorted(type_file)
    for ind, obj in enumerate(type_file):
        obj = obj.split('\n')[0]
        pro, typ = obj.split('/')
        new_b = bouteille(pro, typ, 0, 0, datetime.now())
        b_type.append(new_b)

    for index in all_f:

        mode = 0
        with open("data/clients/"+index, 'r') as data:
            new_s = []
            new_l = []
            new_c = client(index, None, None, new_s, new_l) 
            for line in data:
                line = line.split('\n')[0]
                if line[0] == '{':
                    mode = 1
                    continue
                if line[0] == '}' and mode == 1:
                    mode = 0
                    continue
                if line[0] == '[' and mode == 0:
                    mode = 2
                    continue
                if line[0] == ']' and mode == 2:
                    mode = 0
                    continue
                    
                if line[0] == '@' and line[1] == 'A' and mode == 0:
                    null, adresse = line.split('|')
                    new_c.ch_a(adresse)
                if line[0] == '@' and line[1] == 'T' and mode == 0:
                    null, tel = line.split('|')
                    new_c.ch_t(tel)
                if mode == 1:
                    pro, ty, quan, sta, date = line.split('|')
                    date = datetime(int(date.split('/')[2]),int(date.split('/')[1]),int(date.split('/')[0]))
                    new_b = bouteille(pro, ty, int(quan), int(sta), date)
                    new_c.add_b(new_b)


                if mode == 2:
                    b_l = []
                    b_r = []
                    date, l_b, r_b, init, reel = line.split('|')
                    date = datetime(int(date.split('/')[2]), int(date.split('/')[1]), int(date.split('/')[0]))
                    if l_b != '0':
                        l_b = l_b.split(',')
                        for index in l_b:
                            bout, nombre, status = index.split(':')
                            new_b = bouteille(bout.split('/')[0], bout.split('/')[1], int(nombre), int(status), 0)
                            b_l.append(new_b)
        
                    if r_b != '0':
                        r_b = r_b.split(',')
                        for index in r_b:
                            bout, nombre = index.split(':')
                            new_b = bouteille(bout.split('/')[0], bout.split('/')[1], int(nombre), -1, 0)
                            b_r.append(new_b)
                        
                    new_li = livraison(date, b_l, b_r, int(init), int(reel))
                    new_c.add_l(new_li)
            clients.append(new_c)



def str_date(date):
    result = str(date).split(' ')[0].split('-')
    y,m,d = result
    result = d + '/' + m + '/' + y
    return result

stock_gd = []
stock = []
clients = []
b_type = []
alert = ''
parser()
for client in clients:
    for st in client.stock:
        if st.status == 3 and datetime.now() - st.date > timedelta(14):
            alert += client.name + ' possède ' +  str(st.quantity) + ' ' + st.product + '/' +  st.typ  + ' en tant que prêt depuis le ' +  str_date(st.date) + '\n\n'

root = Tk()
app = App(root)
root.mainloop()
