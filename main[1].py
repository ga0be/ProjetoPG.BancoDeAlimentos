import tkinter as tk
from tkinter import ttk
import sqlite3

# Funktion zur Verbindung mit der Datenbank
def conectardb():
    return sqlite3.connect('bancodealimentos1.db')

# Funktion zur Einrichtung der Datenbank
def inicializardb():
    with conectardb() as conexao:

        cursor = conexao.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Colaborador(
          ID_colaborador INTEGER PRIMARY KEY AUTOINCREMENT,
          Nome_colaborador VARCHAR(50) NOT NULL,
          Sobrenome_colaborador VARCHAR(50) NOT NULL,
          CPF VARCHAR(20) NOT NULL,
          cidade VARCHAR(50) NOT NULL,
          Email VARCHAR(50) NOT NULL,
          Telefone VARCHAR(20) NOT NULL
        );""")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Beneficiario(
          ID_beneficiario INTEGER PRIMARY KEY AUTOINCREMENT,
          Nome_beneficiario VARCHAR(50) NOT NULL,
          Sobrenome_beneficiario VARCHAR(50) NOT NULL,
          CPFb VARCHAR(11) NOT NULL,
          logradourob VARCHAR(50) NOT NULL,
          Emailb VARCHAR(50) NOT NULL,
          Telefoneb VARCHAR(15)
           );""")

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Alimento (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            data_validade DATE,
            Nome_colaborador VARCHAR(50),
            Sobrenome_colaborador VARCHAR(50),
            colaborador_id INTEGER,
            FOREIGN KEY(colaborador_id) REFERENCES Colaborador(ID_colaborador),
            FOREIGN KEY(Nome_colaborador) REFERENCES Colaborador(Nome_colaborador)
            FOREIGN KEY(Sobrenome_colaborador) REFERENCES Colaborador(Sobrenome_colaborador)
        )
        ''')

        conexao.commit()

# Funktion zum Registrieren eines Mitarbeiters
def cadastro_colaborador():
    global conome, cosobrenome
    try:
        conome = Nome_colaborador.get()
        cosobrenome = Sobrenome_colaborador.get()
        cocpf = CPF.get()
        cocidade = cidade.get()
        coemail = Email.get()
        cotelefone = Telefone.get()

        with conectardb() as conexao:
            cursor = conexao.cursor()
            cursor.execute("""
            INSERT INTO Colaborador (Nome_colaborador, Sobrenome_colaborador, 
            CPF, cidade, Email, Telefone) VALUES (?,?,?,?,?,?)""",
            (conome, cosobrenome, cocpf, cocidade, coemail, cotelefone))

            res = cursor.execute("""SELECT * FROM Colaborador;""")
            print(res.fetchall())

            conexao.commit()

        sucesso = tk.Label(text='Cadastro realizado com sucesso!', font=('Arial', 10, 'bold'), fg='green')
        sucesso.grid(row=8, column=0, pady=7, padx=7)

    except Exception as erro:
        erro_label = tk.Label(janelacolab, text=f'Erro: {erro}', font=('Arial', 10, 'bold'), fg='red')
        erro_label.grid(row=8, column=0)

    alimentoaba = tk.Button(janelacolab, text='Doar alimento', command=janelaalimentos, 
                         font=('Arial', 10, 'bold'), fg='white', bg='green')

    alimentoaba.grid(row=9, column=0, pady=7, padx=7, ipadx=40)

def janelacolaborador():
    global Nome_colaborador, Sobrenome_colaborador, CPF, cidade, Email, Telefone, janelacolab

    janelainicial.destroy()
    janelacolab = tk.Tk()
    janelacolab.title('Cadastro de colaborador no Banco de Alimentos!')
    janelacolab.geometry("500x500")
    janelacolab.config(bg='lightyellow')

    Nome_colaborador = ttk.Entry(janelacolab, width=30)
    Nome_colaborador.grid(column=1, row=0, padx=20)
    Sobrenome_colaborador = ttk.Entry(janelacolab, width=30)
    Sobrenome_colaborador.grid(column=1, row=1)
    CPF = ttk.Entry(janelacolab, width=30)
    CPF.grid(column=1, row=2)
    cidade = ttk.Entry(janelacolab, width=30)
    cidade.grid(column=1, row=3)
    Email = ttk.Entry(janelacolab, width=30)
    Email.grid(column=1, row=4)
    Telefone = ttk.Entry(janelacolab, width=30)
    Telefone.grid(column=1, row=5)

    labels = ["Nome:", "Sobrenome:", "CPF:", "Cidade:", "Email:", "Telefone:"]
    for i, text in enumerate(labels):
        ttk.Label(janelacolab, text=text, foreground='blue').grid(column=0, row=i)

    botaocadastroco = tk.Button(janelacolab, 
                                text='-- Cadastrar-se como Colaborador --', 
                                command=cadastro_colaborador, fg ="red", bg='gold')
    botaocadastroco.grid(column=0, row=6, columnspan=2, padx=10, pady=10, ipadx=40)

    janelacolab.mainloop()

def cadastro_beneficiario():
    try:
        bennome = Nome_beneficiario.get()
        bensobrenome = Sobrenome_beneficiario.get()
        bencpf = CPFb.get()
        bencidade = logradourob.get()
        benemail = Emailb.get()
        bentelefone = Telefoneb.get()

        with conectardb() as conexao:
            cursor = conexao.cursor()
            cursor.execute("""
            INSERT INTO Beneficiario (Nome_beneficiario, Sobrenome_beneficiario, 
            CPFb, logradourob, Emailb, Telefoneb) VALUES (?,?,?,?,?,?)""",
            (bennome, bensobrenome, bencpf, bencidade, benemail, bentelefone))

            res = cursor.execute("""SELECT * FROM Beneficiario;""")
            print(res.fetchall())

            conexao.commit()

        sucesso = tk.Label(text='Cadastro realizado com sucesso!', 
                           font=('Arial', 10, 'bold'), fg='green')
        sucesso.grid(row=8, column=0, pady=7, padx=7)

    except Exception as erro:
        erro_label = tk.Label(text=f'Erro: {erro}', font=('Arial', 10, 'bold'), fg='red')
        erro_label.grid(row=8, column=1, pady=7, padx=7)

    alimentoconsulta = tk.Button(janelabenef, text='Ver alimentos disponíveis'
                                 , command=consultaalimentos, fg='white', bg='green', highlightcolor='white')
    alimentoconsulta.grid(row=9, column=0, pady=7, padx=7, ipadx=30)

def janelabeneficiario():
    global Nome_beneficiario, Sobrenome_beneficiario, CPFb, logradourob, Emailb, Telefoneb, janelabenef

    janelainicial.destroy()
    janelabenef = tk.Tk()
    janelabenef.title('Cadastro de beneficiário no Banco de Alimentos!')
    janelabenef.geometry("400x300")
    janelabenef.config(bg='lightyellow')

    Nome_beneficiario = ttk.Entry(janelabenef, width=30)
    Nome_beneficiario.grid(column=1, row=0, padx=20)
    Sobrenome_beneficiario = ttk.Entry(janelabenef, width=30)
    Sobrenome_beneficiario.grid(column=1, row=1)
    CPFb = ttk.Entry(janelabenef, width=30)
    CPFb.grid(column=1, row=2)
    logradourob = ttk.Entry(janelabenef, width=30)
    logradourob.grid(column=1, row=3)
    Emailb = ttk.Entry(janelabenef, width=30)
    Emailb.grid(column=1, row=4)
    Telefoneb = ttk.Entry(janelabenef, width=30)
    Telefoneb.grid(column=1, row=5)
    labels = ["Nome:", "Sobrenome:", "CPF:", "Logradouro:", "Email:", "Telefone:"]
    for i, text in enumerate(labels):
        ttk.Label(janelabenef, text=text, foreground='blue').grid(column=0, row=i)

    botaocadastroben = tk.Button(janelabenef, 
                                 text='-- Cadastrar-se como Beneficiário --', 
                                 command=cadastro_beneficiario, fg ="red", bg='gold')

    botaocadastroben.grid(column=0, row=6, columnspan=2, padx=10, pady=10, ipadx=40)

def cadastro_alimentos():
    try:
       alnome = nomealimento.get()
       alquantidade = qntalimento.get()
       aldata_validade=dataalimento.get()


       with conectardb() as conexao:
         cursor = conexao.cursor()
         cursor.execute('''
         INSERT INTO Alimento (nome, quantidade, data_validade, Nome_colaborador, Sobrenome_colaborador)
         VALUES (?, ?, ?, ?, ?)
         ''', (alnome, alquantidade, aldata_validade, conome, cosobrenome))

         res = cursor.execute("""SELECT * FROM Alimento;""")
         print(res.fetchall())
         conexao.commit()

       sucesso = tk.Label(text='Alimentos cadastrados' + '\n' 'Agradecemos por sua colaboração!',
                          font=('Arial', 10, 'bold'), fg='green')
       sucesso.grid(row=4, column=1, pady=7, padx=7)

    except Exception as erro:
     erro_label = tk.Label(text=f'Erro: {erro}', font=('Arial', 10, 'bold'), fg='red')
     erro_label.grid(row=4, column=1, pady=7, padx=7)

def janelaalimentos():
    global nomealimento, qntalimento, dataalimento, janelaalimento

    janelacolab.destroy()
    janelaalimento = tk.Tk()
    janelaalimento.title('Cadastro de alimentos')
    janelaalimento.geometry("400x300")
    janelaalimento.config(bg='lightgoldenrod2')

    nomealimento = ttk.Entry(janelaalimento, width=30)
    nomealimento.grid(column=1, row=0, padx=20)
    qntalimento = ttk.Entry(janelaalimento, width=30)
    qntalimento.grid(column=1, row=1)
    dataalimento = ttk.Entry(janelaalimento, width=30)
    dataalimento.grid(column=1, row=2)

    labels = ["Alimento:", "Quantidade:", "Data de validade:"]
    for i, text in enumerate(labels):
        ttk.Label(janelaalimento, text=text, foreground='blue').grid(column=0, row=i)

    botaocadastroal = tk.Button(janelaalimento, text='-- Cadastrar alimento --', 
                                command=cadastro_alimentos, fg='white', bg='green')
    botaocadastroal.grid(column=0, row=3, columnspan=2, padx=30)



def obteralimentos():


    return


def consultaalimentos():
    global janelaconsulta
    janelabenef.destroy()
    janelaconsulta = tk.Tk()
    janelaconsulta.title('Consulta de alimentos')
    janelaconsulta.geometry("500x300")
    janelaconsulta.config(bg='lightgoldenrod2')

    alimentos = tk.Label(janelaconsulta, text='Alimentos disponíveis:', font=('Arial', 10, 'bold'), fg='blue')
    alimentos.grid(row=0, column=0, pady=7, padx=7)
    with conectardb() as conexao:
        cursor = conexao.cursor()
        cursor.execute('SELECT * FROM Alimento')
        alimentos_disponiveis = cursor.fetchall()
        for i, alimento in enumerate(alimentos_disponiveis):
            alimento_label = tk.Label(janelaconsulta, text= f'{alimento[0]}    ' + f'{alimento[1]}       ' + 
                                      'Quantidade:  ' + f'{alimento[2]}   ' + 'Colaborador:  ' + f'{alimento[4]} ' + f'{alimento[5]}')
            alimento_label.grid(row=i+1, column=0, pady=7, padx=40)

    janelainicial.mainloop()


# Setup der Datenbank
inicializardb()

# Hauptfenster erstellen
janelainicial = tk.Tk()
janelainicial.title('Escolher seu cadastro:')
janelainicial.geometry("600x200")
janelainicial.config(bg='medium spring green')

bemvindo = tk.Label(text='Bem-vindo ao Banco de Alimentos!', font=('Comic Sans MS', 20, 
                                                                   'bold')
                    , fg='goldenrod1', bg='springgreen3')
bemvindo.grid(row=0, column=0, pady=10, padx=10, columnspan=2)


botaocolab = tk.Button(janelainicial, text='-- Cadastrar-se como Colaborador --', 
                            command=janelacolaborador, bg='bisque')
botaocolab.grid(column=0, row=1, columnspan=2, padx=8, pady=7, ipadx=40)

botaobenef = tk.Button(janelainicial, text='-- Cadastrar-se como Beneficiario --', 
                       command=janelabeneficiario, bg='bisque')
botaobenef.grid(column=0, row=2, columnspan=2, rowspan=8, padx=8, pady=7, ipadx=40)

janelainicial.mainloop()