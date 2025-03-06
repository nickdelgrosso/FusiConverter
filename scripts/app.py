import cortical


filepath = cortical.open_file_dialog()
print(filepath)
data = cortical.load_openfus_mat(filename=filepath)
print(data)

