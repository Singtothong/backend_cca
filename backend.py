import schedule
import time
from datetime import date
import girder_client

def new_slide_update():
    # API Key
    APIURL = 'https://dsa.prod.evernetwork.io/api/v1/'
    gc = girder_client.GirderClient(apiUrl=APIURL)
    gc.authenticate(apiKey='VMelRVQSyYRLdPMpD8i8nrEUKEaWkK8b1zbIqPgj')
    # find all collections
    collection_info = gc.get('collection')
    collection_dict = {}
    collection_name = []
    for collection in collection_info:
        collection_dict[collection["name"]] = collection["_id"]
        collection_name.append(collection["name"])
    # find all folders
    folder_dict = {}
    folder_name = []
    for collection_ in collection_name:
        collectionId = collection_dict[collection_]
        folder_info = gc.get(
            'folder?parentType=collection&parentId=%s&limit=50&sort=lowerName&sortdir=1' % collectionId)
        for folder in folder_info:
            folder_dict[folder["name"]] = folder["_id"]
            folder_name.append(folder["name"])
    # find new slide
    new_slide_dict = {}
    new_slide = []
    today = date.today()
    d1 = today.strftime("%Y-%m-%d")
    for folder_ in folder_name:
        folderId = folder_dict[folder_]
        item_info = gc.get('item?folderId=%s&sort=lowerName' % folderId)
        for item in item_info:
            date_create = item['created'].split('T')[0]
            if date_create == d1:
                new_slide_dict['folder_Id'] = folderId
                new_slide_dict['slide_no'] = item["name"]
                new_slide.append(new_slide_dict.copy())
    return new_slide

def getNewSlideandCallAPI():
    # check new slides
    ls = new_slide_update()
    
    # suppose output of list as ....
    """
    ls = [{'folder_Id': '615f2eaa821f2ce94387a47a', 'slide_no': 'S62-04412-1-D'},
          {'folder_Id': '615f2eaa821f2ce94387a47a', 'slide_no': 'S62-00114-1-A'},
          {'folder_Id': '615f2eaa821f2ce94387a47a', 'slide_no': 'S62-00184-1-D'}]
    """
    # run model via API
    for item in ls:
        f = item['folder_Id']
        s = item['slide_no']

        url = 'https://cca-ai-nkicjqa6tq-as.a.run.app/cca?folder_Id={0}&slide_no={1}'.format(f, s)
        print(url)
        
        response = requests.get(url)
        print(response)

def job():
    getNewSlideandCallAPI()

schedule.every().day.at('11:00').do(job)
schedule.every().day.at('23:00').do(job)

while 1:
    schedule.run_pending()
    time.sleep(1)
