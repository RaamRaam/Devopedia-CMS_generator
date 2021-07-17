from libraries import sys, requests


if __name__=="__main__":

    url=str(sys.argv[1])

    source=requests.get(url).text
 
    try:
        with open('file.htm','w',encoding='utf8') as f:
            f.write(source)
    except:
        with open('file.htm','w',encoding='iso-8859-1') as f:
            f.write(source)


    print("URL content saved as file.htm!")


