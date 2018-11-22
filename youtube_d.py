import tkinter

root = tkinter.Tk()

root.title("YOUTUBE downloader!")

root.resizable(width="false", height="false")

root.minsize(width=600, height=300)
root.maxsize(width=600, height=300)

simple_label = tkinter.Label(root, text="Download video")


closing_button = tkinter.Button(root, text="Exit", command=root.destroy)

simple_label.pack()
closing_button.pack()

root.mainloop()
