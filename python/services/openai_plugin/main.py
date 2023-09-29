import os
from pathlib import Path
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from services.openai_plugin.Github import Github

router = APIRouter()

github = Github()

@router.get('/.well-known/ai-plugin.json')
def plugin_manifest(): 
    try:
        pwd = os.getcwd()
        manifest_path = Path(f"{pwd}/services/openai_plugin/ai-plugin.json")
        if manifest_path.exists() and manifest_path.is_file():
            with manifest_path.open("r") as manifest_file:
                manifest_content = manifest_file.read()
                return JSONResponse(content=manifest_content, media_type="application/json")
        else:
            return JSONResponse(content={"error": "Manifest file not found"}, status_code=404)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    
@router.get('/.well-known/openapi.json')
def openapi_plugin():
    try:
        pwd = os.getcwd()
        manifest_path = Path(f"{pwd}/services/openai_plugin/openapi.json")
        if manifest_path.exists() and manifest_path.is_file():
            with manifest_path.open("r") as manifest_file:
                manifest_content = manifest_file.read()
                return JSONResponse(content=manifest_content, media_type="application/json")
        else:
            return JSONResponse(content={"error": "OpenAPI file not found"}, status_code=404)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@router.get("/github/repository/{owner}/{repo}")
def get_github_repository(owner: str, repo: str):
    files = github.get_repository_files(owner, repo)
    
    result = []
    for file in files:
        path, file_content = github.get_file_content(owner, repo, file)
        result.append({
            "path": path,
            "content": file_content
        })

    return result

    
    