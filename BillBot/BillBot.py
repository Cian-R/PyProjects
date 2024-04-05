from tkinter import *
import customtkinter


class App(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("500x400")
        self.wm_title("BillBot")
        self.content = customtkinter.CTkFrame(self, bg_color="Teal")
        self.content.grid(row=0, column=0)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        #
        # self.total_frame = customtkinter.CTkFrame(self, fg_color="Blue", corner_radius=1)
        # self.total_frame.grid(row=0, column=0, rowspan=1, sticky=(N, S, E, W))
        # self.list_frame = customtkinter.CTkFrame(self, fg_color="Red", corner_radius=1)
        # self.list_frame.grid(row=1, column=1, rowspan=3)
        #
        # self.padder = customtkinter.CTkFrame(content, fg_color="White", corner_radius=30)
        # self.padder2 = customtkinter.CTkFrame(content, fg_color="White", corner_radius=30)
        # self.padder3 = customtkinter.CTkFrame(content, fg_color="White", corner_radius=30)
        # self.padder.grid(row=0, column=1, sticky="NE")
        # self.padder2.grid(row=1, column=2, sticky="NE")
        # self.padder3.grid(row=0, column=3, sticky="NE")
        #
        # self.rowconfigure(0, weight=1)
        # self.rowconfigure(1, weight=1)
        # self.columnconfigure(0, weight=1)
        # self.columnconfigure(0, weight=3)
        # self.columnconfigure(1, weight=3)
        # self.columnconfigure(2, weight=3)
        # self.columnconfigure(3, weight=1)
        # self.columnconfigure(4, weight=1)



        # self.frame1 = customtkinter.CTkFrame(self, fg_color="Blue").pack()

    # def


if __name__ == "__main__":
    app = App()
    app.mainloop()
