#!/usr/bin/python3
# Author: Gunnar Holwerda
# Creation: 8/11/2015
# Last Edit: 8/12/2015
# GUI to control a PiWall
from tkinter import *
from piwallcontroller import PiWallController, Playlist
from threading import Thread


class SelectorWindow(Frame):
    TIMEOUTS = {
        '1 hour ': 3600,
        '2 hours': 7200,
        '3 hours': 10800,
    }

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.__playlist = Playlist()
        self.__controller = PiWallController()
        self.__dropdown_selection = StringVar()
        self.__timeout_selection = StringVar()
        self.grid()
        self.create_video_file_dropdown()
        self.create_timeout_dropdown()
        self.create_display_box()
        self.create_add_button()
        self.create_delete_button()
        self.create_submit_button()
        self.create_reboot_button()
        self.create_status_label()
        self.create_stop_button()

    def create_video_file_dropdown(self):
        videos = self.__controller.get_video_file_list()
        videos.sort()
        self.__dropdown_selection.set(videos[0])
        self.video_dropdown = OptionMenu(None, self.__dropdown_selection, *videos)
        self.video_dropdown.config(width=15)
        self.video_dropdown.grid(row=0, column=0)

    def create_timeout_dropdown(self):
        timeouts = list(self.TIMEOUTS.keys())
        timeouts.sort()
        self.__timeout_selection.set(timeouts[0])
        self.timeout_dropdown = OptionMenu(None, self.__timeout_selection, *timeouts)
        self.timeout_dropdown.config(width=5)
        self.timeout_dropdown.grid(row=0, column=1)

    def create_display_box(self):
        self.display_box = Listbox(width=30, height=10)
        self.display_box.grid(row=0, column=2, columnspan=2)

    def create_submit_button(self):
        self.submit_button = Button(text="Submit")
        self.submit_button['command'] = self.submit_form
        self.submit_button.config(width=10)
        self.submit_button.grid(row=1, column=2, pady=5)

    def create_add_button(self):
        self.add_button = Button(text='Add', fg='green')
        self.add_button['command'] = self.update_display_box
        self.add_button.config(width=10)
        self.add_button.grid(row=1, column=0, pady=5)

    def create_delete_button(self):
        self.delete_button = Button(text='Delete', fg='red')
        self.delete_button['command'] = self.delete_selected_item
        self.delete_button.config(width=10)
        self.delete_button.grid(row=1, column=1, pady=5)

    def create_reboot_button(self):
        self.reboot_button = Button(text='Reboot Tiles', fg='red')
        self.reboot_button['command'] = self.reboot_pressed
        self.reboot_button.config(width=10)
        self.reboot_button.grid(row=1, column=3, pady=5)

    def create_status_label(self):
        self.status_label = Label()
        self.set_status_label(0)
        self.status_label.grid(row=2, column=2, columnspan=2, pady=5)

    def create_stop_button(self):
        self.stop_button = Button(text='Stop Playing')
        self.set_status_label(0)
        self.stop_button['command'] = self.stop_pressed
        self.stop_button.grid(row=2, column=0, columnspan=2, pady=5)

    def delete_selected_item(self):
        self.__playlist.remove_playlist_item(self.display_box.curselection())
        self.display_box.delete(self.display_box.curselection())

    def submit_form(self):
        # TODO: Maybe show what playlist is currently playing in a new Listbox
        if self.__playlist.is_empty():
            return
        self.set_status_label(1)
        self.display_box.delete(0, END)
        command_thread = Thread(target=self.__controller.run_commands, args=(self.__playlist,))
        command_thread.start()

    def update_display_box(self):
        video_file = self.__dropdown_selection.get()
        timeout = self.__timeout_selection.get()
        self.__playlist.add_playlist_item(video_file, self.TIMEOUTS[timeout])
        self.display_box.insert(END, "{0}   {1}".format(timeout, video_file))

    def stop_pressed(self):
        self.__controller.stop_wall()
        self.set_status_label(0)

    def reboot_pressed(self):
        self.set_status_label(0)
        self.__controller.reboot_pis()
        return True

    def set_status_label(self, state):
        if state == 1:
            self.status_label.config(text='Playing', bg='green')
            return True
        elif state == 0:
            self.status_label.config(text='Not Playing', bg='red')
            return True
        else:
            Exception('Status label state {0} not supported. Try 1 or 2'.format(state))

# Run the GUI
root = Tk(className="PiWall")
SelectorWindow(master=root)
root.mainloop()
