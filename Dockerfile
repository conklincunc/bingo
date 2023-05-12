FROM python:3

#Set the working directory
WORKDIR /opt/app-root

#copy all the files
COPY . .

RUN pip --disable-pip-version-check install -r requirements.txt
#Expose the required port
EXPOSE 8080

#Run the command
CMD ["python3", "./app/app.py"]
