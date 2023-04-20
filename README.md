# OCR_excercise
Một bài tập lớn cho môn Xử Lý Ảnh khi học tại trường HUST *.py linguist-language=python


# Vietnamese Recognition and Translation window app use Tkinter



## Description

The project aims to develop an application that can recognize Vietnamese and translate it into the desired language. The application will use machine learning algorithms to recognize text and then translate it using googletrans.

## Getting Started

### 


### Dependencies

* Python 3
* OpenCV
* Tkinter
* googletrans
* pytesseract

### Installing

* Clone the repository
* Install dependencies using pip

or pip install -r requirements.txt

### Executing program

* Run the application using the command "python main.py"
* Write the text in Vietnamese on the screen
* The application will recognize the text and translate it into the desired language

### Preprocess the image:
1. Resize image
``` python
def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]
    ...
```
2. Adjust contrast brightness
```python
def adjust_contrast_brightness(img, contrast:float=1.0, brightness:int=0):
    """
    Adjusts contrast and brightness of an uint8 image.
    contrast:   (0.0,  inf) with 1.0 leaving the contrast as is
    brightness: [-255, 255] with 0 leaving the brightness as is
    """
    brightness += int(round(255*(1-contrast)/2))
    return cv2.addWeighted(img, contrast, img, 0, brightness)
```
3. Convert to grayscale
```python
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
```
4. Apply AdaptiveThreshold

--> Apply OCR on the preprocessed image using Pytesseract.

--> Extract the text output and save it to a text file.

--> Visualize the preprocessed image and the extracted text output.

--> Save the results to file.

--> Translate

### User interface
![image](https://user-images.githubusercontent.com/83382634/233055365-986c2e35-296b-44bf-8c9b-735826fb122a.png)

## Quá trình
1. Training: 
- Công cụ để train Tesseract – jTessBoxEditor. 
- File font chữ cần đào tạo có đuôi là ttf. Ví dụ: TimeNewRoman.ttf  
- File văn bản khoảng 600KB đến 1MB để học được nhiều kí tự khác nhau.
- Cài Java Runtime Environment (JRE) là một lớp phần mềm cung cấp các dịch vụ cần thiết để thực thi những ứng dụng Java.
![image](https://user-images.githubusercontent.com/83382634/233062282-f47a4ab2-9e1c-4e8e-bd12-784c29256514.png)
2. Sau training: Sau khi train ta thu được 1 bộ font để sử dụng
![image](https://user-images.githubusercontent.com/83382634/233062411-3602b54c-b663-4e29-9464-94b0fe389e3b.png)



## Authors

* Lê Thu Thủy
* Trần Long Quang Anh
* Nguyễn Trung Hiếu

## License



## Acknowledgments


