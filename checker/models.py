from django.db import models
from django.contrib.auth.models import User

# Create your models here.
import json
import time
import zipfile
import requests
import google.generativeai as genai


headers = {
    "app_key": "09ca526cba33c5506e1caf3a99f7d45575b1fc6e4c5518b1a1b3be16a4cfcab6",
    "app_id": "plagarismdetector_1c01cd_5322ce"
}
class Question(models.Model):
    textbook = models.TextField(max_length=200)
    chapter = models.IntegerField()
    question_number = models.IntegerField()
    question_text = models.CharField(max_length=200)
    ai_response = models.CharField(max_length=500)

    def get_gemini_response(self):
        genai.configure(api_key="AIzaSyCocAfdhyrwvn8kJzpfULH7vGcayiC2O80") 
        model = genai.GenerativeModel("gemini-1.5-flash")
        self.ai_response = model.generate_content(self.question_text)

class Student_Work_PDF(models.Model):
    pdf = models.FileField(upload_to="uploads/")
    name = models.CharField(default=f"{pdf.name}", max_length=25)
    upload_date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

class Student_Work(models.Model): 
    file = models.FileField()
    transcription = models.TextField()
    pdf_id = models.TextField()

    def transcribe_pdf(self):
        
        r = requests.post("https://api.mathpix.com/v3/pdf",
            headers=headers,
            files={
                "file": open("sample.pdf","rb")
            }
        )
        if r.status_code == 200:
            self.pdf_id = json.loads(json.dumps(r.json))['pdf_id']

    def get_transcription_results(self):
        conversion_response = None
        while (True):
            time.sleep(5)
            conversion_response = requests.get("https://api.mathpix.com/v3/converter/"+self.pdf_id,
            headers=headers)
            json_data = json.loads(json.dumps(conversion_response.json()))
            
            if(json_data['status'] == "completed"):
                break

        if conversion_response.status_code == 200:
            # get tex.zip file
            url = "https://api.mathpix.com/v3/pdf/" + self.pdf_id + ".tex"
            response = requests.get(url, headers=headers)
            with open(self.pdf_id + ".tex.zip", "wb") as f:
                f.write(response.content)

            # extract zip folder to current directory
            with zipfile.ZipFile(self.pdf_id+".tex.zip","r") as zip_ref:
                zip_ref.extractall()
            self.transcription = open(self.pdf_id+"/"+self.pdf_id+".tex", "r").read()