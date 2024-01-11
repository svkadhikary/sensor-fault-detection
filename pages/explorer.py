import streamlit as st
import os


st.title("Sensor data explorer")

# Function to list files and folders recursively
def list_files_and_folders(directory):
    items = os.listdir(directory)
    try:
        selection = st.sidebar.selectbox(f"Choose an option", items)
        selection_path = os.path.join(directory, selection)
        if os.path.isdir(selection_path):
            list_files_and_folders(selection_path)
        else:
            st.header(f"{selection}")
            if selection_path.endswith((".log", ".csv", ".yaml")):
                file_contents = open(os.path.join(directory, selection_path), "r").readlines()
                st.download_button(f"Download {selection}", data=open(selection_path, "rb"), file_name=f"{selection}")
                st.write(file_contents)
            else:
                st.write(selection_path)
                st.download_button(f"Download {selection}", data=open(selection_path, "rb"), file_name=f"{selection}")
                
    
    except TypeError as te:
        st.error("No contents inside")
    except Exception as e:
        st.error("Exception: ", e)
    
        

# list of allowed folders
allowed_folders = ["logs", "data", "artifact", "saved_models"]

# sidebar for selecting directory
selected_folder = st.sidebar.selectbox("Select a folder:", allowed_folders)

# Get the full path of the selected folder
selected_folder_path = os.path.join(os.getcwd(), "datadir", selected_folder)

# Display files and folders starting from the root directory
list_files_and_folders(selected_folder_path)
