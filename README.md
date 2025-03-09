# PDF Merger App

A simple GUI application to merge multiple PDF files into one. This app allows users to select PDF files, reorder them via drag-and-drop, and merge them into a single PDF file.

<img src="images/app_screenshot.png" width="500" height="auto">

## Features

- **Add PDF Files**: Select multiple PDF files to add to the list.
- **Drag-and-Drop Reordering**: Easily reorder the selected PDF files by dragging them around in the list.
- **Remove PDF Files**: Remove any selected PDF file from the list.
- **Merge PDFs**: Merge the selected PDF files into a single PDF file and save it to the desired location.
- **Customizable Window**: The window can be resized, and it will center on the screen.

## Requirements

- Python 3.x
- Tkinter (for the GUI)
- PyPDF2 (for PDF manipulation)
- Pillow (for handling image icons)

## Installation

1. Install the required Python libraries:

```bash
pip install -r requirements.txt
```

2. Download or clone the repository.

## Usage

1. Run the Python script:
```bash
python PDFMergerApp.py
```
2. The application window will open, displaying the following options:

- **Add PDFs:** Opens a file dialog to select PDF files.
- **Remove Selected:** Removes the currently selected file from the list.
- **Merge PDFs:** Merges the selected files into a single PDF.
3. Drag and drop PDF files within the list to adjust their order.
4. After merging, the app will prompt you to choose a location to save the merged PDF.

## Application Icon

The application displays an icon in the window and on the taskbar. Ensure the icon file is placed correctly in the project folder, or update the file path as needed.

## License

This project is open-source and available under the MIT License.

## Required Python Libraries

- **Tkinter:** The GUI toolkit used for building the application.
- **PyPDF2:** Used for merging PDF files.
- **Pillow:** Used for loading and displaying the application icon.




