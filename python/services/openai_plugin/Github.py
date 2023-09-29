import requests
import base64

class Github():
    def get_repository_files(self, owner, repo):
        api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/"
        response = requests.get(api_url)

        files = []

        if response.status_code == 200:
            files_data = response.json()

            for file in files_data:
                if 'type' in file and file['type'] == 'file':
                    files.append(file["name"])
        
        return files
    
    def get_file_content(self, owner, repo, file):
        api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file}"
        response = requests.get(api_url)

        if response.status_code == 200:
            file_data = response.json()

            if 'content' in file_data:
                content = file_data['content']
                decoded_content = base64.b64decode(content)
                path = file_data['path']
                return path, decoded_content.decode('utf-8')
        
        return None
    

    
