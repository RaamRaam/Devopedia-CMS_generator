from libraries import sys, requests,os


if __name__=="__main__":

    folder_path='Prediction_outputs'
    try:    
        os.mkdir(folder_path)
    except:
        pass
    url=str(sys.argv[1])

    source=requests.get(url).text
 
    try:
        with open(os.path.join(folder_path,'file.htm'),'w',encoding='utf8') as f:
            f.write(source)
    except:
        with open(os.path.join(folder_path,'file.htm'),'w',encoding='iso-8859-1') as f:
            f.write(source)


    print("URL content saved as file.htm!")


