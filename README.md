# Video-Lecture-To-PDF
A simple python script to generate a pdf from a video lecture. Basically the program captures the unique frames from the video and marge them into a pdf. 

### **Setting up virtual environment [Windows]**

1.  At first you need to install virtualenv

	`
	python -m pip install --user virtualenv
	`
2. Creating virtual env

	`
	python -m venv venv
	`
3. Activate virtual env

	`
	venv\Scripts\Activate
	`

### **Install Depencies**
1. Simply run this command

	`
	pip install -r requirements.txt
	`

## **Running the script**
1.  At first place all the videos into the folder called 'videos'

2. Open command prompt and navigate to the main script's folder

3. In your command prompt type - 

	`
	python main.py
	`
	
> [Note: It will take some time to generate the pdf. Meanwhile it will print the similarity score while getting an unique frame and move the processed videos to ProcessedVideos folder.]

After successful execution, you will find your desired PDFs in the folder called pdf.  
