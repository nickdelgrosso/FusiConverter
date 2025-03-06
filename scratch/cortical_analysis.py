import h5py
import numpy as np
import napari
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QFileDialog, QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from magicgui import magicgui

def load_h5_file(filepath):
    """Load an H5 file and extract the image dataset."""
    with h5py.File(filepath, 'r') as f:
        fusi = f['image'][:]
    print('Image Loaded. Size:', fusi.shape)
    return fusi

def create_napari_viewer():
    """Create a Napari viewer with interactive widgets."""
    viewer = napari.Viewer()
    image_data = None  # Store the full image data

    @magicgui(call_button="Load H5 File")
    def open_file_dialog():
        nonlocal image_data
        filepath, _ = QFileDialog.getOpenFileName(None, "Select H5 File", "", "H5 Files (*.h5)")
        if filepath:
            image_data = load_h5_file(filepath)
            max_proj = np.max(image_data, axis=0)  # Default max projection
            viewer.add_image(max_proj, name="Max Projection")
            return image_data

    viewer.window.add_dock_widget(open_file_dialog)

    @magicgui(call_button="Update Projection", top_idx={"max": 50}, bottom_idx={"max": 50})
    def update_max_projection(top_idx: int = 7, bottom_idx: int = 12):
        if image_data is None:
            print("No image data loaded.")
            return
        cortex_data = image_data[top_idx:bottom_idx, :, :, :]
        max_proj = np.max(cortex_data, axis=0)
        viewer.layers["Max Projection"].data = max_proj  # Update the image layer instead of creating new ones
    
    viewer.window.add_dock_widget(update_max_projection)
    
    class ROISignalPlot(QWidget):
        def __init__(self):
            super().__init__()
            self.layout = QVBoxLayout()
            self.figure, self.ax = plt.subplots()
            self.canvas = FigureCanvas(self.figure)
            self.layout.addWidget(self.canvas)
            self.setLayout(self.layout)

        def update_plot(self, signals, method):
            self.ax.clear()
            for i, signal in enumerate(signals):
                self.ax.plot(signal, label=f"ROI {i+1}")
            self.ax.set_xlabel("Time")
            self.ax.set_ylabel("Signal Intensity")
            self.ax.set_title(f"ROI Signal ({method})")
            self.ax.legend()
            self.canvas.draw()
    
    roi_plot_widget = ROISignalPlot()
    viewer.window.add_dock_widget(roi_plot_widget, name="ROI Signal Plot")
    
    @magicgui(call_button="Plot ROI Signals", method={"choices": ["mean", "median", "mean_log"]})
    def plot_roi_signals(method: str = "mean"):
        if image_data is None:
            print("No image data available.")
            return

        time_points = image_data.shape[-1]
        roi_signals = []

        for layer in viewer.layers:
            if isinstance(layer, napari.layers.Shapes):
                for roi in layer.data:
                    min_x, min_y = np.min(roi, axis=0).astype(int)
                    max_x, max_y = np.max(roi, axis=0).astype(int)

                    roi_data = image_data[min_x:max_x, min_y:max_y, :, :]
                    signal_over_time = []

                    for t in range(time_points):
                        frame = roi_data[:, :, :, t].flatten()
                        if method == "mean":
                            signal_over_time.append(np.mean(frame))
                        elif method == "median":
                            signal_over_time.append(np.median(frame))
                        elif method == "mean_log":
                            signal_over_time.append(np.mean(np.log1p(frame)))
                    
                    roi_signals.append(signal_over_time)
        
        roi_plot_widget.update_plot(roi_signals, method)
    
    viewer.window.add_dock_widget(plot_roi_signals)
    
    napari.run()

if __name__ == "__main__":
    create_napari_viewer()
