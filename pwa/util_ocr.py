import pyautogui
import pytesseract
import openpyxl
from pywinauto.application import Application

def capture_grid_as_image(wnd_ctrl):
    """
    Capture a screenshot of the specified grid control
    """
    # Get the bounding rectangle of the grid control
    rect = wnd_ctrl.rectangle()
    
    # Capture the screenshot of the grid area
    return pyautogui.screenshot(region=(rect.left, rect.top, rect.width(), rect.height()))

def extract_grid_text_using_ocr(image):
    """
    Use Tesseract OCR to extract text from the grid image
    """
    return pytesseract.image_to_string(image)

def save_grid_to_excel(grid_data, file_path):
    """
    Save the grid data to an Excel file
    """
    workbook = openpyxl.Workbook()
    worksheet = workbook.active

    for row, row_data in enumerate(grid_data, start=1):
        for col, cell_value in enumerate(row_data, start=1):
            worksheet.cell(row=row, column=col, value=cell_value)

    workbook.save(file_path)

def extract_grid_data_from_window(wnd_ctrl):
    """
    Extract grid data from the specified window and grid control ID
    """
    # Capture the grid area screenshot
    grid_image = capture_grid_as_image(wnd_ctrl)
    
    # Extract text from the grid image using OCR
    grid_text = extract_grid_text_using_ocr(grid_image)
    
    # Split the grid text into rows and columns
    grid_data = [row.split('\t') for row in grid_text.strip().split('\n')]
    
    return grid_data

# Example usage
