import streamlit as st
import os
import subprocess

# Define the Streamlit app
def main():
    st.title("Log to Columnar Converter")

    # File upload section
    st.header("Upload Input Log File")
    uploaded_file = st.file_uploader("Choose a JSON log file", type=["json", "log"])

    if uploaded_file:
        # Save the uploaded file to a temporary location
        temp_dir = "temp_input"
        os.makedirs(temp_dir, exist_ok=True)
        temp_file_path = os.path.join(temp_dir, uploaded_file.name)
        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(uploaded_file.read())

        # Output directory selection
        output_directory = st.text_input("Output Directory", "output_columns")

        # Convert button
        if st.button("Convert"):
            # Execute the log conversion script using subprocess
            command = f"python log_to_columns.py {temp_file_path} {output_directory}"
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()

            # Display the conversion result
            if process.returncode == 0:
                st.success("Conversion successful. Columnar files are generated.")
            else:
                st.error(f"Conversion failed with the following error:\n{stderr.decode()}")

    st.text("")  # Add some spacing

# Run the Streamlit app
if __name__ == "__main__":
    main()
