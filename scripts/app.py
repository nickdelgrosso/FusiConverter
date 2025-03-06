from magicgui import magicgui
import napari
import cortical




viewer = napari.Viewer()

@magicgui(call_button="Load Fusion File")
def load_fusion_file():
    filepath = cortical.open_file_dialog()
    print(filepath)
    data = cortical.load_openfus_mat(filename=filepath)
    viewer.add_image(data.image, name='Fusion')
viewer.window.add_dock_widget(load_fusion_file)

napari.run()