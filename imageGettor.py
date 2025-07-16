from duckduckgo_search import DDGS
from PIL import Image
import os
import requests
from io import BytesIO
from dotenv import load_dotenv

ddgs = DDGS()

if __name__ == "__main__":
    load_dotenv()
    #Get search results for classication
    header = {"Authorization": os.environ.get("pexels_apikey")}
    bearResults = requests.get("https://api.pexels.com/v1/search?query=bear&per_page=80", headers=header).json()
    brownieResults = requests.get("https://api.pexels.com/v1/search?query=brownie&per_page=80", headers=header).json()
    duckResults = requests.get("https://api.pexels.com/v1/search?query=duck&per_page=80", headers=header).json()
    
    #Add the images to the bears, brownies, and ducks dir
    for i, result in enumerate(bearResults["photos"]):
        response = requests.get(result['src']['original'])
        image = BytesIO(response.content)
        with Image.open(image) as img:
            resized = img.resize((256,256))
            if i <= 59:
                resized.save(os.path.join("./bears", f"bear_{i}" + ".jpg"))   
            elif i <= 69:
                resized.save(os.path.join("./bears_test", f"bear_{i}" + ".jpg"))   
            else:
                resized.save(os.path.join("./bears_validation", f"bear_{i}" + ".jpg"))   

    for i, result in enumerate(brownieResults["photos"]):
        response = requests.get(result['src']['original'])
        image = BytesIO(response.content)
        with Image.open(image) as img:
            resized = img.resize((256,256))
            if i <= 59:
                resized.save(os.path.join("./brownies", f"brownie_{i}" + ".jpg"))   
            elif i <= 69:
                resized.save(os.path.join("./brownies_test", f"brownie_{i}" + ".jpg"))   
            else:
                resized.save(os.path.join("./brownies_validation", f"brownie_{i}" + ".jpg"))   
    for i, result in enumerate(duckResults["photos"]):
        response = requests.get(result['src']['original'])
        image = BytesIO(response.content)
        with Image.open(image) as img:
            resized = img.resize((256,256))
            if i <= 59:
                resized.save(os.path.join("./ducks", f"duck_{i}" + ".jpg"))   
            elif i <= 69:
                resized.save(os.path.join("./ducks_test", f"duck_{i}" + ".jpg"))   
            else:
                resized.save(os.path.join("./ducks_validation", f"duck_{i}" + ".jpg"))  


    