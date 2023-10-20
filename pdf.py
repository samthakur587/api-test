from fastapi import FastAPI, UploadFile, File
import os

app = FastAPI()

# Define the upload directory
upload_folder = "pdfs"

if not os.path.exists(upload_folder):
    os.mkdir(upload_folder)

@app.post("/uploadpdfs/")
async def upload_pdfs(files: list[UploadFile] = File(...)):
    # Iterate through the uploaded files
    for uploaded_file in files:
        # Construct the file path for saving
        file_path = os.path.join(upload_folder, uploaded_file.filename)
        
        # Save the file to the upload directory
        with open(file_path, "wb") as file_object:
            file_object.write(uploaded_file.file.read())
    
    return {"message": "PDFs uploaded and saved successfully!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
