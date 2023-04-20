from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
import tkinter.ttk as exTk
import googletrans
from googletrans import Translator
import cv2
from tkinter.filedialog import asksaveasfile
from tkinter import filedialog
from tkinter import scrolledtext
import os
from tkinter import messagebox
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import sys
from spellchecker import SpellChecker
import pytesseract

'''
	input: là đường dẫn tới ảnh
	Kiểu dữ liệu đầu vào là string (đường dẫn mà ^_^)

	output: là đoạn văn bản thu được sau xử lý
	Kiểu dữ liệu đầu ra là string
'''

# Bạn hãy đặt code hàm xử lý chính trên dòng này
def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation = inter)

    # return the resized image
    return resized

def adjust_contrast_brightness(img, contrast:float=1.0, brightness:int=0):
    """
    Adjusts contrast and brightness of an uint8 image.
    contrast:   (0.0,  inf) with 1.0 leaving the contrast as is
    brightness: [-255, 255] with 0 leaving the brightness as is
    """
    brightness += int(round(255*(1-contrast)/2))
    return cv2.addWeighted(img, contrast, img, 0, brightness)

# get grayscale image - anh xám
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def importing(image):
    image = cv2.imread(image)
    image = image_resize(image, height = 600)
    contrast1 = adjust_contrast_brightness(image, contrast=1.0, brightness=0)
    gray = get_grayscale(contrast1)  # tao anh gray
# do adaptive threshold on gray image
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 21, 15)
# make background of input white where thresh is white
    result = image.copy()
    result[thresh == 255] = (255, 255, 255)
    return result

# adaptiveThreshold

def exporting(image):
	# Ghi tạm ảnh xuống ổ cứng để sau đó apply OCR
	filename = "{}.png".format(os.getpid())
	cv2.imwrite(filename, image)

	# Load ảnh và apply nhận dạng bằng Tesseract OCR
	text = pytesseract.image_to_string(Image.open(filename), lang='vie')

	# Xóa ảnh tạm sau khi nhận dạng
	os.remove(filename)
	return text

def clean_text(text):
    ret = text.replace("\n\n","\n")
    ret = ret.replace("\n\n", "\n")
    return ret

def OCR(link):
	image2 = importing(link)
	text2 = exporting(image2)
	text2=clean_text(text2)
	return text2

def on_closing():
	rs = messagebox.askokcancel("Quit", "Bạn muốn thoát chứ?\nĐừng quên lưu các thông tin bạn cần nhé!")
	if(rs == True):
		sys.exit(0)
	else:
		pass

class monitor(Frame):
	check_new_window = pip install tkinter
pip install Pillow
pip install googletrans
pip install opencv-python
pip install matplotlib
pip install pyspellchecker
pip install pytesseract

	lang = googletrans.LANGUAGES
	lang = list(lang.values())
	lang = [i.title() for i in lang]
	inp_lang = "Vietnamese"
	out_lang = "English"
	program_lang = "Vietnamese"

	def loadImage(obj):

		objW = obj.winfo_width()
		objH = obj.winfo_height()
		obj.clearText()
		print(objW, objH)

		#obj.folder_name = filedialog.askdirectory()
		obj.filename = filedialog.askopenfilename()
		#print(obj.folder_name)

		try:
			obj.image_bgr = cv2.imread(obj.filename)
			obj.height, obj.width = obj.image_bgr.shape[:2]
			scale = obj.height/obj.width
			obj.canvas1.delete("all")
			if scale<615/758:
				obj.new_size = (int(758), int(758*scale))
			else:
				obj.new_size = (int(615/scale), int(615))
			obj.image_bgr_resize = cv2.resize(obj.image_bgr, obj.new_size, interpolation=cv2.INTER_AREA)
			obj.image_rgb = cv2.cvtColor(obj.image_bgr_resize, cv2.COLOR_BGR2RGB)  #Since imread is BGR, it is converted to RGB

		   # obj.image_rgb = cv2.cvtColor(obj.image_bgr, cv2.COLOR_BGR2RGB) #Since imread is BGR, it is converted to RGB
			obj.image_PIL = Image.fromarray(obj.image_rgb) #Convert from RGB to PIL format
			obj.image_tk = ImageTk.PhotoImage(obj.image_PIL) #Convert to ImageTk format
			obj.canvas1.create_image(int(758/2), int(615/2), image=obj.image_tk)

			obj.link_text.config(state=NORMAL)
			obj.link_text.delete(0, END)
			obj.link_text.insert(END, obj.filename)
			obj.link_text.config(state=DISABLED)
		except:
			pass

	def processText(obj, a):
		if (a.find("  ") == -1):
			return(a)
		else:
			a = a.replace("  ", " ")
			a = obj.processText(a)
			return(a)

	def processText1(obj, a):
		if (a.find("\n\n") == -1):
			return(a)
		else:
			a = a.replace("\n\n", "\n")
			a = obj.processText1(a)
			return(a)

	def processText2(obj):
		essay = obj.inp_text.get(1.0, END)
		spell = SpellChecker()
		paragraph = essay.split("\n")
		text = str()
		for i in range(len(paragraph)):
			paragraph2word = paragraph[i].split()
			for word in paragraph2word:
				text += str(spell.correction(word)) + " "
			text += "\n"
		obj.inp_text.config(state=NORMAL)
		obj.inp_text.delete(1.0, END)	
		obj.inp_text.insert(END, text)
		obj.inp_text.config(state=DISABLED)
		messagebox.showinfo("", "Done!")

	def show_inp_to_text(obj):
		link = str(obj.link_text.get())
		link = link.strip()

		# Gọi OCR
		try:
			background = Image.open(link)
			text = OCR(link)
			text = obj.processText(text)
			text = obj.processText1(text)

			obj.inp_text.config(state=NORMAL)
			obj.inp_text.delete(1.0, END)
			obj.inp_text.insert(END, text)
			obj.inp_text.config(state=DISABLED)
		except AttributeError:
			messagebox.showerror("Error", "Xin hãy chọn ảnh\nPlease choose a photo")
		except FileNotFoundError:
			messagebox.showerror("Error", "Xin hãy chọn ảnh\nPlease choose a photo")

	def Translate(obj):
		t = Translator()
		inp = obj.inp_text.get(1.0, END)

		obj.inp_lang = obj.inp_combobox.get()
		obj.out_lang = obj.out_combobox.get()

		try:
			out = t.translate(inp, src=obj.inp_lang, dest=obj.out_lang)
			out = out.text
			obj.out_text.config(state=NORMAL)
			obj.out_text.delete(1.0, END)
			obj.out_text.insert(END, out)
			obj.out_text.config(state=DISABLED)
		
		except ValueError:
			messagebox.showerror("Error", "Kiểm tra lại ngôn ngữ bạn nhé!!!\nPlease check your language!!!\n-_-")
		except TypeError:
			pass

	def clearText(obj):
		obj.inp_text.config(state=NORMAL)
		obj.inp_text.delete(1.0, END)
		obj.inp_text.config(state=DISABLED)
		obj.out_text.config(state=NORMAL)
		obj.out_text.delete(1.0, END)
		obj.out_text.config(state=DISABLED)

	def  openImgNewWindow(obj):
		Files = [('All Files', '*.*'),
				('Portable Network Graphics', '*.png'),
				('Joint Photographic Experts Group', '*.jpeg'),
				('Joint Photographic Experts Group', '*.jpg'),
				('???', '*.jfif')]
		link = filedialog.askopenfilename(initialdir="./",
				title="Please select one or more files:",
				filetypes=Files)
		link = link.strip()
		obj.link_text.config(state=NORMAL)
		obj.link_text.delete(0, END)
		obj.link_text.insert(END, link)
		obj.link_text.config(state=DISABLED)
		try:
			background = Image.open(link)
			plt.clf()
			img = mpimg.imread(link)
			imgplot = plt.imshow(img)
			plt.title("Image")
			plt.show()
		except:
			pass

	def saveP(obj):
		Files = [('All Files', '*.*'),
				('Python Files', '*.py'),
				('Text Document', '*.txt'),
				('Microsoft Word', '*.docx')]
		file = asksaveasfile(filetypes = Files, initialdir="./", defaultextension = Files)
		try:
			f = open(file.name, "w", encoding="utf-8")
			t = obj.out_text.get(1.0, END)
			f.write(t)
			f.close()
		except AttributeError:
			pass

	def saveT(obj):
		Files = [('All Files', '*.*'),
				('Python Files', '*.py'),
				('Text Document', '*.txt'),
				('Microsoft Word', '*.docx')]
		file = asksaveasfile(filetypes = Files, initialdir="./", defaultextension = Files)
		try:
			f = open(file.name, "w", encoding="utf-8")
			t = obj.inp_text.get(1.0, END)
			f.write(t)
			f.close()
		except AttributeError:
			pass

	def quitProgram(obj):
		rs = messagebox.askquestion("Quit","Bạn muốn thoát chứ?\nĐừng quên lưu các thông tin bạn cần nhé!")
		if(rs == "yes"):
			sys.exit(0)
		else:
			pass

	def tutorial(obj):
		try:
			f = open("imageicon/tutorial.txt", "r", encoding="utf-8")
			text = f.read()
			f.close()
			messagebox.showinfo("Tutorial", text)
		except FileNotFoundError:
			messagebox.showwarning("Warning", "Ai đó đó xóa file rồi @_@")

	def contactToUs(obj):
		try:
			f = open("imageicon/contactToUs.txt", "r", encoding="utf-8")
			text = f.read()
			f.close()
			messagebox.showinfo("Contact to us", text)
		except FileNotFoundError:
			messagebox.showwarning("Warning", "Ai đó đó xóa file rồi @_@")


	def chooseLanguage(obj):
		T = Translator()
		obj.program_lang = obj.language_combobox.get()
		# T.translate(inp, src=obj.inp_lang, dest=obj.out_lang)
		obj.load_image.configure(text=T.translate("Upload", src="English", dest=obj.program_lang).text)
		obj.handling_button.configure(text=T.translate("Processing", src="English", dest=obj.program_lang).text)
		obj.trans_button.configure(text=T.translate("Translate", src="English", dest=obj.program_lang).text)
		obj.clear_button.configure(text=T.translate("Erase", src="English", dest=obj.program_lang).text)
		obj.inp_combobox_label.configure(text=T.translate("Văn bản đã xử lý", src="Vietnamese", dest=obj.program_lang).text, justify=LEFT)
		obj.out_combobox_label.configure(text=T.translate("Văn bản đã dịch", src="Vietnamese", dest=obj.program_lang).text, justify=LEFT)

	def new_window_closing(obj):
		obj.check_new_window = 0
		obj.new_win.destroy()

	def newWindow(obj):
		if(obj.check_new_window == 0):
			obj.new_win = Toplevel(obj)

			obj.new_win.geometry("400x200")
			obj.new_win.resizable(width=False, height=False)
			obj.new_win.protocol("WM_DELETE_WINDOW", obj.new_window_closing)
			apply_button = Button(obj.new_win, text="Apply", bd=4, command=obj.chooseLanguage)
			apply_button.place(x=295, y=165, width=100, height=30)

			language_combobox_text = tk.StringVar()
			language_combobox_label = Label(obj.new_win, text="Language", font=("Time", 15))
			language_combobox_label.place(x=5, y=10, width=100, height=30)
			obj.language_combobox = exTk.Combobox(obj.new_win, textvariable = language_combobox_text, font=10)
			obj.language_combobox["values"] = obj.lang
			# obj.language_combobox.set("Vietnamese")
			obj.language_combobox.place(x=110, y=10, width=250, height=30)
			obj.check_new_window = 1
		else:
			pass

	def placeGUI(obj, e):
		# obj.update()
		objW = obj.winfo_width()
		objH = obj.winfo_height()

		obj.link_text.place(x=20, y=70, width=objW-40, height=30)

		obj.load_image.place(x=20, y=10, width=int(objW/4-30), height=40)
		obj.handling_button.place(x=40+int(objW/4-30), y=10, width=int(objW/4-30), height=40)
		obj.trans_button.place(x=60+int(objW/4-30)*2, y=10, width=int(objW/4-30), height=40)
		obj.clear_button.place(x=80+int(objW/4-30)*3, y=10, width=int(objW/4-30), height=40)

		obj.inp_text.place(x=objW/2+30, y=150, width=objW/2-50, height=int((objH-150-50)*0.46))
		obj.out_text.place(x=objW/2+30, y=150+int((objH-150-50)*0.46)+50, width=objW/2-50, height=int((objH-150-50)*0.46))
		obj.inp_combobox_label.place(x=objW/2+150, y=110, width=400, height=30)
		obj.inp_combobox.place(x=objW/2+20, y=110, width=130, height=30)
		obj.out_combobox_label.place(x=objW/2+150, y=150+int((objH-150-50)*0.46)+10, width=400, height=30)
		obj.out_combobox.place(x=objW/2+20, y=150+int((objH-150-50)*0.46)+10, width=130, height=30)
		obj.canvas1.place(x=10, y=125, width=objW/2-10, height=objH*0.8-10)
		
	def __init__(obj, master):
		super().__init__(master)
		obj.menu = Menu(obj)
		obj.master.config(menu=obj.menu)
		
		fileMenu = Menu(obj.menu)
		obj.menu.add_cascade(label="File", menu=fileMenu)

		fileMenu.add_command(label="Open image file in new window", command=obj.openImgNewWindow)
		fileMenu.add_command(label="Save the processed text", command=obj.saveP)
		fileMenu.add_command(label="Save translated text", command=obj.saveT)
		fileMenu.add_command(label="Quit", command=obj.quitProgram)

		toolsMenu = Menu(obj.menu)
		obj.menu.add_cascade(label="Tools", menu=toolsMenu)
		toolsMenu.add_command(label="Chose language", command=obj.newWindow)
		toolsMenu.add_command(label="Process text", command=obj.processText2)

		helpMenu = Menu(obj.menu)
		obj.menu.add_cascade(label="Help", menu=helpMenu)
		helpMenu.add_command(label="Tutorial", command=obj.tutorial)
		helpMenu.add_command(label="Contact with us", command=obj.contactToUs)
		obj.link_text = Entry(obj, state=DISABLED, bd=4)

		obj.inp_text = scrolledtext.ScrolledText(obj, font=("Time", 15),
			wrap=tk.WORD,
			bd=10,
			state=DISABLED)
		obj.out_text = scrolledtext.ScrolledText(obj, font=("Time", 15),
			wrap=tk.WORD,
			bd=10,
			state=DISABLED)
		obj.load_image = Button(obj, text="Tải", bd=4, 
			font=("Time", 15), compound="left", command=obj.loadImage)
		obj.handling_button = Button(obj, text="Xử lý", bd=4,
			font=("Time", 15), command=obj.show_inp_to_text)
		obj.trans_button = Button(obj, text="Dịch", bd=4,
			font=("Time", 15), command=obj.Translate)
		obj.clear_button = Button(obj, text="Xóa", bd=4,
			font=("Time", 15), command=obj.clearText)

		obj.inp_combobox_label = Label(obj, text="Văn bản đã xử lý", font=("Time", 12), justify=LEFT)
		obj.inp_combobox_text = tk.StringVar()
		obj.inp_combobox = exTk.Combobox(root, textvariable = obj.inp_combobox_text, font=10)
		obj.inp_combobox["values"] = obj.lang
		obj.inp_combobox.set("Vietnamese")

		obj.out_combobox_label = Label(obj, text="Văn bản đã dịch", font=("Time", 12), justify=LEFT)
		obj.out_combobox_text = tk.StringVar()
		obj.out_combobox = exTk.Combobox(root, textvariable = obj.out_combobox_text, font=10)
		obj.out_combobox["values"] = obj.lang
		obj.out_combobox.set("English")
		
		obj.canvas1 = Canvas(obj, bd=5, bg="#C7CBD1")

		master.bind("<Configure>", obj.placeGUI)

root = Tk()

root.title("TRaT 2.0")				 # Text Recognition and Translation
root.iconbitmap("imageicon/ava1.ico")
scrW = int(root.winfo_screenwidth()*0.9)
scrH = int(root.winfo_screenheight()*0.9)

root.geometry(f"{scrW}x{scrH}+0+0")
root.minsize(550, 500)
root.protocol("WM_DELETE_WINDOW", on_closing)
hi = monitor(root)
hi.place(relwidth=1, relheight=1)

root.mainloop()