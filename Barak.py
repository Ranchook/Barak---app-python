import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
import os
import tkinter.messagebox as messagebox

"""
 Folder are located where client wants it to be, *.jpg are in ...\Barak\dist\Plots
 *.csv files are in ...\Barak\dist\Graphs_Data
"""

graph_path = os.getcwd() + "\\Plots"
data_path = os.getcwd() + "\\Graphs_Data"


def new_window_func(w, h):
    # Create new window
    new_window = tk.Tk()
    new_window.title("Barak & Ra'am")
    # Get the screen width and height
    screen_width = new_window.winfo_screenwidth()
    screen_height = new_window.winfo_screenheight()

    # Determine the position of the window
    window_width = w
    window_height = h

    # Position the window in the middle of the screen
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    # Set the window size and position
    new_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
    new_window.resizable(False, False)
    return new_window


def clean_df(df):
    # The *.csv file has specific data that looks like this [date,x,y,z,total,size]
    # Columns x,y,z are redundant according to the client
    # The file has no titles so titles are added for easy work
    col_names = ["date", "emp", "emp2", "emp3", "value", "size"]
    # Rename the columns
    for i in range(len(col_names)):
        df.rename(columns={i: col_names[i]}, inplace=True)
    # Drop the redundant columns
    for i in range(1, 4):
        df.drop(columns=col_names[i], inplace=True)
    return df


def plot_graph(df, file_name, xtick_indices, angle):
    # get the data required from the gui and plot the graph accordingly
    x_graph = df['date']
    y_graph = df['value']
    fig, ax = plt.subplots()
    fig.subplots_adjust(top=0.95, bottom=0.2)
    ax.plot(x_graph, y_graph)
    plt.grid(visible=True)
    fig.set_figwidth(15)
    fig.set_figheight(6)

    # set y-axis label and set its coordinates
    plt.ylabel('[mG]', rotation=0)
    ax.yaxis.set_label_coords(-.02, 1)

    # tick the x-axis at appropriate times and at desired angle
    xtick_tmp = np.arange(0, (len(df)), (int(len(df)-1)/xtick_indices))
    xtick_tmp[len(xtick_tmp)-1] = len(df) - 1
    plt.xticks(xtick_tmp, rotation=angle)

    # Save the plot to the Plots folder
    # print(os.path.join(graph_path, file_name + '.jpg'))
    plt.savefig(os.path.join(graph_path, file_name + '.jpg'))
    # Open the folder containing the new plot *.jpg
    os.startfile(graph_path)


def clean_file_name(name_with_csv):
    # Remove the ".csv" part and everything that follows it
    return name_with_csv.split(".csv")[0]


def data_window_func(df, name):
    # Create new window after reading the *.csv file
    data_window = new_window_func(600, 500)
    # Info label
    info_str = "You have " + str(len(df)) + " data points in " + name
    data_window_label = tk.Label(data_window, text=info_str, font=9)
    data_window_label.place(relx=0.5, rely=0.1, anchor="center")

    # X-tick selection label
    select_label = "How many x-axis ticks do you want?"
    data_window_select_label = tk.Label(data_window, text=select_label, font=9)
    data_window_select_label.place(relx=0.5, rely=0.2, anchor="center")

    # X-tick slider
    x_tick_slider = tk.Scale(data_window, from_=5, to=10, orient="horizontal", resolution=1, width=30, font=9)
    x_tick_slider.place(relx=0.5, rely=0.3, anchor="center")
    x_tick_slider.set(7)

    # X-tick rotation label
    rotation_label = "Please select the rotation angle of the ticks:"
    data_window_rotation_label = tk.Label(data_window, text=rotation_label, font=9)
    data_window_rotation_label.place(relx=0.5, rely=0.5, anchor="center")

    # Rotation slider
    Rotation_slider = tk.Scale(data_window, from_=0, to=90, orient="horizontal", resolution=15, width=30, font=9)
    Rotation_slider.place(relx=0.5, rely=0.62, anchor="center")
    Rotation_slider.set(45)

    # Create a button
    plot_button = tk.Button(data_window, text="Generate \nGraph", font=9,
                            command=lambda: plot_graph(df, name, x_tick_slider.get(), Rotation_slider.get()))
    plot_button.place(relx=0.5, rely=0.8, anchor="center")


# "Read data" button function
def on_button_click(event=None):
    # Get the text from the text box
    text = text_box.get()
    # Check if input is legal
    if text == "":  # if no input
        messagebox.showerror('Error', 'Please enter text')

    else:  # legal input
        name = clean_file_name(text)  # save file name to be the *.jpg file name
        # *.csv file should be located under ...\Barak\dist\Graphs_data folder
        file_path = data_path + "\\" + name + ".csv"
        # print(file_path)
        if os.path.exists(file_path):  # check if file exists
            df = pd.read_csv(file_path, header=None)  # read file without header
            df = clean_df(df)  # remove redundant columns
            data_window_func(df, name)  # move to data window
        else:  # file doesn't exists
            messagebox.showerror('Error', "File doesn't exists\n Maybe you misspelled it...")


# Create the main window
main_window = new_window_func(600, 300)

label = tk.Label(main_window, text="Enter file name:", font=9)
label.place(relx=0.17, rely=0.3, anchor="center")

# Create a text box
text_box = tk.Entry(main_window, font=9)
text_box.place(relx=0.52, rely=0.3, anchor="center")

# Create a button
read_data_button = tk.Button(main_window, text="Read Data", font=9, command=on_button_click)
read_data_button.place(relx=0.857, rely=0.3, anchor="center")

# Folder buttons
data_folder_button = tk.Button(main_window, text="Open\nData Folder", font=9, command=lambda: os.startfile(data_path))
data_folder_button.place(relx=0.3, rely=0.7, anchor="center")

plots_folder_button = tk.Button(main_window, text="Open\nGraphs Folder", font=9, command=lambda: os.startfile(graph_path))
plots_folder_button.place(relx=0.7, rely=0.7, anchor="center")

# Run the main loop
main_window.mainloop()
