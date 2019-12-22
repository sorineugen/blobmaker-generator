import os
import time
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


def set_driver(src_address):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(src_address)
    driver.implicitly_wait(10)

    return driver


def set_blob_shape(driver, complexity, contrast):
    elements = driver.find_elements_by_class_name('rc-slider-handle')
    for element in elements:
        if element.get_attribute('aria-valuemax') == '1':
            contrast_element = element
        if element.get_attribute('aria-valuemax') == '11':
            complexity_element = element
    
    driver.execute_script(f'arguments[0].setAttribute("aria-valuenow","{complexity}");', complexity_element)
    driver.execute_script(f'arguments[0].setAttribute("aria-valuenow","{contrast}");', contrast_element)

    return driver

def refresh_blob_shape(driver):
    refresh = driver.find_element_by_name('Update blob')
    refresh.click()

    return driver

def download_blob_shape(driver):
    download = driver.find_element_by_name('Download blob')
    download.click()

    return driver

def get_blob_shapes(driver, complexity, contrast, quantity=1):
    destination_dir = 'blobmaker.app'
    os.makedirs(destination_dir, exist_ok=True)
    driver = set_blob_shape(driver, complexity, contrast)
    for i in range(1, quantity + 1):
        driver = refresh_blob_shape(driver)
        driver = download_blob_shape(driver)
        i_display = ('0' + str(i))[-2:]
        file_path = os.path.join(os.getcwd(), 'blob-shape.svg')
        file_path_new = os.path.join(os.getcwd(), destination_dir, f'blob-shape_{complexity}-{contrast}_{i_display}.svg')
        while not os.path.exists(file_path):
            time.sleep(1)
        if os.path.isfile(file_path):
            os.rename(file_path, file_path_new)
        
    return f'Complexity: {complexity}\nContrast: {contrast}\nQuantity: {quantity} blobs\nDestination: {os.path.realpath(destination_dir)}\n'



if __name__ == '__main__':
    if len(sys.argv) > 1:
        complexity = int(sys.argv[1])
        contrast = float(sys.argv[2])
        quantity = int(sys.argv[3])
    else:
        complexity = int(input('Complexity: '))
        contrast = float(input('Contrast: '))
        quantity = int(input('Quantity: '))

    if complexity not in range(3,12):
        sys.exit('ERROR: Complexity should be an integer between 3 and 11')

    if contrast < 0 or contrast > 1:
        sys.exit('ERROR: Contrast should be a decimal number between 0 and 1')
    
    if quantity < 1 or quantity > 99:
        sys.exit('ERROR: Quantity should be an integer between 1 and 99')

    try:
        driver = set_driver('https://www.blobmaker.app/')
        result = get_blob_shapes(driver, complexity, contrast, quantity)
        print('\nProcess summary:\n' + result)
    except Exception as e:
        print(e)
    finally:
        driver.close()
