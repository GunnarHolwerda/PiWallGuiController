"""
    GUI Application to control the PiWall from
"""
#!/usr/bin/python3
# Author: Gunnar Holwerda
# GUI to control a PiWall

from tkinter import Frame, StringVar, OptionMenu, Listbox, Button, Label, Tk, END
from piwallcontroller.piwallcontroller import PiWallController
from piwallcontroller.playlist import Playlist
from threading import Thread


class SelectorWindow(Frame):
    """
        GUI Class extending the tkinter.Frame class
    """
    TIMEOUTS = {
        '1 hour ': 3600,
        '2 hours': 7200,
        '3 hours': 10800,
        'Infinite': -1,
    }

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.__playlist = Playlist()
        self.__controller = PiWallController()
        self.__dropdown_selection = StringVar()
        self.__timeout_selection = StringVar()
        self.__command_thread = Thread(
            target=self.__controller.run_commands, args=(self.__playlist,))
        self.grid()
        self.create_video_file_dropdown()
        self.create_timeout_dropdown()
        self.create_display_box()
        self.create_add_button()
        self.create_delete_button()
        self.create_play_button()
        self.create_reboot_button()
        self.create_status_label()
        self.create_stop_button()

    def create_video_file_dropdown(self):
        """
            Creates the dropdown to display the video files from
        """
        videos = self.__controller.get_video_file_list()

        if videos:
            self.__dropdown_selection.set(videos[0])
        else:
            videos.append(None)

        self.video_dropdown = OptionMenu(
            None, self.__dropdown_selection, *videos)
        self.video_dropdown.config(width=10)
        self.video_dropdown.grid(row=0, column=0)

    def create_timeout_dropdown(self):
        """
            Creates the dropdown that displays the timeouts
        """
        timeouts = list(self.TIMEOUTS.keys())
        timeouts.sort()
        self.__timeout_selection.set(timeouts[0])
        self.timeout_dropdown = OptionMenu(
            None, self.__timeout_selection, *timeouts)
        self.timeout_dropdown.config(width=5)
        self.timeout_dropdown.grid(row=0, column=1)

    def create_display_box(self):
        """
            Creates display box that displays all current items in the playlist
        """
        self.display_box = Listbox(width=30, height=10)
        self.display_box.grid(row=0, column=2, columnspan=2)

    def create_play_button(self):
        """
            Creates the play button
        """
        self.submit_button = Button(text="Play", width=10)
        self.submit_button['command'] = self.play_wall
        self.submit_button.grid(row=1, column=2, pady=5)

    def create_add_button(self):
        """
            Creates the button to add the current values in the video and timeout dropdown
            into the playlist
        """
        self.add_button = Button(text='Add', fg='green', width=10)
        self.add_button['command'] = self.update_display_box
        self.add_button.grid(row=1, column=0, pady=5)

    def create_delete_button(self):
        """
            Creates delete button to delete items from display blox
        """
        self.delete_button = Button(text='Delete', fg='red', width=10)
        self.delete_button['command'] = self.delete_selected_item
        self.delete_button.grid(row=1, column=1, pady=5)

    def create_reboot_button(self):
        """
            Creates button that reboots the pi's
        """
        self.reboot_button = Button(text='Reboot Tiles', fg='red', width=10)
        self.reboot_button['command'] = self.reboot_pressed
        self.reboot_button.grid(row=1, column=3, pady=5)

    def create_status_label(self):
        """
            Creates label to display current status of the wall
        """
        self.status_label = Label(relief="ridge", width=11)
        self.set_status_label(0)
        self.status_label.grid(row=2, column=3, pady=5)

    def create_stop_button(self):
        """
            Creates stop button to stop PiWall
        """
        self.stop_button = Button(text='Stop Playing')
        self.set_status_label(0)
        self.stop_button['command'] = self.stop_pressed
        self.stop_button.grid(row=2, column=2, pady=5)

    def delete_selected_item(self):
        """
            Deletes the currently selected item from the displaybox
        """
        self.__playlist.remove_playlist_item(self.display_box.curselection())
        self.display_box.delete(self.display_box.curselection())

    def play_wall(self):
        """
            Submits ths form to be played on the pi's
        """
        if self.__playlist.is_empty():
            return
        self.set_status_label(1)
        self.display_box.delete(0, END)
        # If there is a thread running, we need to stop the wall, which will
        # end the thread
        if self.__command_thread.isAlive():
            print("Stopping Wall")
            self.__controller.stop_wall()
            self.__command_thread.join()
        self.__command_thread = Thread(
            target=self.__controller.run_commands, args=(self.__playlist,))
        self.__command_thread.start()

    def update_display_box(self):
        """
            Button listener for the Add Button (create_add_button)
        """
        video_file = self.__dropdown_selection.get()
        timeout = self.__timeout_selection.get()
        self.__playlist.add_playlist_item(video_file, self.TIMEOUTS[timeout])
        self.display_box.insert(END, "{0}   {1}".format(timeout, video_file))

    def stop_pressed(self):
        """
            Button listener for the Stop Button (create_stop_button)
        """
        self.__controller.stop_wall()
        self.set_status_label(0)

    def reboot_pressed(self):
        """
            Button listener for the Reboot Button (create_reboot_button)
        """
        self.set_status_label(0)
        self.__controller.reboot_pis()
        return True

    def set_status_label(self, state):
        """
            Updates the status label to the current status of the PiWall
        """
        if state == 1:
            self.status_label.config(text='Playing', fg='green')
            return True
        elif state == 0:
            self.status_label.config(text='Not Playing', fg='red')
            return True
        else:
            Exception(
                'Status label state {0} not supported. Try 1 or 2'.format(state))

    def get_controller(self):
        """
            Returns the piwallcontrollers
        """
        return self.__controller


# Run the GUI
if __name__ == "__main__":
    tk_window = Tk(className="PiWall")
    frame = SelectorWindow(master=tk_window)
    tk_window.mainloop()
    frame.get_controller().stop_wall()
