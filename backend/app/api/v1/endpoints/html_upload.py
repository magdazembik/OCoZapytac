"""
HTML Upload endpoint for rich content

"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import os
import uuid
from datetime import datetime

router = APIRouter()

# Define the directory where HTML content will be stored
# This should be accessible by your FastAPI application
HTML_CONTENT_DIR = Path("uploaded_html_content")
HTML_CONTENT_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/upload-html/")
async def upload_html_content(file: UploadFile = File(...)):
    """
    Uploads an HTML file and returns its path.
    The content of this file will be used for article content.
    
    Usage:
    1. Save your Google Docs content as HTML file
    2. Upload it using this endpoint
    3. Use the returned 'content_path' in your article creation
    """
    if not file.filename.endswith((".html", ".htm")):
        raise HTTPException(status_code=400, detail="Only HTML files are allowed")

    # Create a unique filename to prevent overwrites
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    safe_filename = f"{timestamp}_{unique_id}_{file.filename}"
    
    file_location = HTML_CONTENT_DIR / safe_filename

    try:
        # Read and save the file content
        content = await file.read()
        with open(file_location, "wb") as f:
            f.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not upload file: {str(e)}")

    # Return the relative path that can be stored in the database
    return {
        "message": "HTML file uploaded successfully",
        "original_filename": file.filename,
        "content_path": str(file_location),
        "usage_instructions": {
            "step_1": "Copy the 'content_path' value below",
            "step_2": "Use it in the 'content_file_path' field when creating an article via Swagger UI",
            "step_3": "Leave the 'content' field empty or put a brief description"
        }
    }

@router.get("/list-uploaded-files/")
async def list_uploaded_files():
    """
    List all uploaded HTML files
    """
    try:
        files = []
        for file_path in HTML_CONTENT_DIR.glob("*.html"):
            stat = file_path.stat()
            files.append({
                "filename": file_path.name,
                "path": str(file_path),
                "size_bytes": stat.st_size,
                "created": datetime.fromtimestamp(stat.st_ctime).isoformat()
            })
        
        return {
            "uploaded_files": files,
            "total_files": len(files)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not list files: {str(e)}")

@router.delete("/delete-html-file/")
async def delete_html_file(file_path: str):
    """
    Delete an uploaded HTML file
    """
    try:
        file_to_delete = Path(file_path)
        
        # Security check: ensure the file is in our upload directory
        if not str(file_to_delete).startswith(str(HTML_CONTENT_DIR)):
            raise HTTPException(status_code=400, detail="Invalid file path")
        
        if file_to_delete.exists():
            file_to_delete.unlink()
            return {"message": f"File {file_to_delete.name} deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="File not found")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not delete file: {str(e)}")

