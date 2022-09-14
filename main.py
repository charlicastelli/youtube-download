from logging import error
from pytube import YouTube
import youtube_dl
from tkinter import *
import tkinter.messagebox as tkMessageBox
import os
import tkinter.filedialog as fdlg
from tkinter import ttk


COLOR_BUTTON = "#7984EE"
COLOR_PROGRESS = "#FF6464"
COLOR_TEXT_BUTTON = "#FFFFFF"


def selecionado(event,textnome):
    textnome.delete(0,'end')
    textnome.config(fg='black')

def deselecionado(event,textnome):
    if textnome.get()=="":
        textnome.insert(0,'Obrigatório!')
        textnome.config(fg='red')
def saindo():
	result = tkMessageBox.askquestion("", "Confirma a saída?", icon='question')
	if result=='yes':
		os._exit(1)
	else:
		pass
def limpar():
	txtLink.delete(0,"end")
	progress1.stop()

def baixadormp3():
	progress1['value']+=10
	screen.update()
	video_url = txtLink.get()
	txtLink['state'] = DISABLED
	
	try:
		video_info = youtube_dl.YoutubeDL().extract_info(
		url = video_url,download=False
		)
		filename = f"{video_info['title']}.mp3"
		options={
			'format':'bestaudio/best',
			'keepvideo':False,
			'outtmpl':filename,
		}
		tkMessageBox.showinfo("Selecionar pasta", message= "Selecione a pasta onde deseja salvar!")

		#seleciona pasta para salvar arquivo
		opcoes = {}                
		opcoes['initialdir'] = ''    
		opcoes['parent'] = screen
		opcoes['title'] = 'Escolha uma pasta para salvar'
		caminhosalvar = fdlg.askdirectory(**opcoes)

		progress1['value']+=10
		screen.update()
		assert caminhosalvar != "", 'nenhum dado para notas'
		
		os.chdir(caminhosalvar)
		
		with youtube_dl.YoutubeDL(options) as ydl:
			ydl.download([video_url])

		txtLink['state'] = NORMAL
		tkMessageBox.showinfo("Download completo", message= "Salvo na pasta: " + str(caminhosalvar))
		limpar()
	except:
		progress1.stop()
		txtLink['state'] = NORMAL
		tkMessageBox.showinfo("Erro", message= "Não foi possível finalizar!!")
		
def baixadormp4():
	link = txtLink.get()
	progress1['value']+=10
	txtLink['state'] = DISABLED
	screen.update()
	try:
		
		progress1['value']+=10
		screen.update()

		tube = YouTube(link)
		progress1['value']+=10
		screen.update()

		
		tubes = tube.streams.get_highest_resolution()
		progress1['value']+=10
		screen.update()

		tkMessageBox.showinfo("Selecionar pasta", message= "Selecione a pasta onde deseja salvar!")

		#seleciona pasta para salvar arquivo
		opcoes = {}                
		opcoes['initialdir'] = ''    
		opcoes['parent'] = screen
		opcoes['title'] = 'Escolha uma pasta para salvar'
		caminhosalvar = fdlg.askdirectory(**opcoes)

		progress1['value']+=10
		screen.update()
		assert caminhosalvar != "", 'nenhum dado para notas'
		
		tubes.download(caminhosalvar)
		txtLink['state'] = NORMAL
		tkMessageBox.showinfo("Download completo", message= "Salvo na pasta: " + str(caminhosalvar))
		limpar()

	except:
		progress1.stop()
		txtLink['state'] = NORMAL
		tkMessageBox.showinfo("Erro", message= "Não foi possível finalizar!!")
		

def progresso(escolhido):
	url = txtLink.get()
	if url == "" or url == 'URL do vídeo obrigatório!' or url == 'URL do vídeo':
		tkMessageBox.showinfo("Erro", message= "Favor preencher uma URL válida!!")
	else:
		if escolhido =="mp4":
			progress1.start(10)
			baixadormp4()
		else:
			progress1.start(10)
			baixadormp3()


screen = Tk()
screen.title("Download De Vídeos MP4 e MP3")
screen.geometry("700x500")
screen.resizable(False, False) 
screen['bg'] = "#000000"
screen.iconphoto(True, PhotoImage(file='./images/icon.png'))

image=PhotoImage(file='./images/musica-yt.png')

campointervalo = Label(screen, width=700, height=500, image=image, bd=3, fg='black',bg = 'black', font=('arial',10,'bold'))
campointervalo.grid(rowspan=10,columnspan =5)

lblLink = Label(screen, height=1, width=15, foreground=COLOR_TEXT_BUTTON, bg=COLOR_BUTTON, text = "YouTube link: ",font=('arial',14, 'bold'))
lblLink.place(relx = 0.03, rely = 0.1)

txtLink = Entry(screen,width=40,justify='left',fg='black', font=('arial',14))
txtLink.place(relx=0.3, rely=0.1)
txtLink.insert(0,'Entre com o link')
txtLink.bind('<FocusIn>', lambda event=txtLink, btn=txtLink: selecionado(event,btn))
txtLink.bind('<FocusOut>', lambda event=txtLink, btn=txtLink: deselecionado(event,btn))




btinicio = Button(screen, width=15, text = " Baixar MP4  ", foreground=COLOR_TEXT_BUTTON, bg=COLOR_BUTTON, font=('arial',14,'bold'),command=lambda: progresso('mp4'))
btinicio.place(relx = 0.03, rely = 0.3)

btimusica = Button(screen, width=15, text = " Baixar MP3  ", foreground=COLOR_TEXT_BUTTON, bg=COLOR_BUTTON, font=('arial',14,'bold'),command=lambda: progresso('mp3'))
btimusica.place(relx = 0.03, rely = 0.4)

btilimpa = Button(screen, width=15, text = " Limpar  ", foreground=COLOR_TEXT_BUTTON, bg=COLOR_BUTTON, font=('arial',14,'bold'),command=limpar)
btilimpa.place(relx = 0.03, rely = 0.5)

btsair = Button(screen, width=15, text = "   Sair   ",foreground=COLOR_TEXT_BUTTON, bg=COLOR_BUTTON, font=('arial',14,'bold'),command=saindo)
btsair.place(relx = 0.03, rely = 0.8)

#Progressbar 
s = ttk.Style() 
s.theme_use('default') 
s.configure("#E23E57.Horizontal.TProgressbar", foreground=COLOR_PROGRESS, background=COLOR_PROGRESS)

progress1 =ttk.Progressbar(screen, orient=HORIZONTAL, length=750, style="#E23E57.Horizontal.TProgressbar",mode='determinate')
progress1.place(relx=0, rely = 0)

screen.mainloop()


