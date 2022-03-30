from src.setupconfig import Configservice
from sqlalchemy import create_engine

class Dataservice():
    
    confg = Configservice()        

## create connection to MySQL
    @staticmethod
    def getMySQLConn(db):

        if db == "aggrdb" or db == "preddb":
            mysqlconfig = "mysqlsettings"
        elif db == "histdb":
            mysqlconfig = "mysqlhistsettings"
        elif db == "rptdb":
            mysqlconfig = "mysqlrptsettings"
           
        cs = Configservice()
        return create_engine("mysql+pymysql://{user}:{pw}@{host}:{port}/{db}"\
            .format(host=cs.getStorageLayerConfig(mysqlconfig,"host"),\
                port=cs.getStorageLayerConfig(mysqlconfig,"port"),\
                    user=cs.getStorageLayerConfig(mysqlconfig,"user"),\
                        pw=cs.getStorageLayerConfig(mysqlconfig,"passwd"),\
                            db=cs.getStorageLayerConfig(mysqlconfig,db)))


    @staticmethod
    def callgraviteeapi(service, post_param="", method = ""):
        import requests
        try:
            servicelist = { 
            "predict_news_sentiment": lambda : "newssentiment-service.news-sentiment:6022/predict_news_sentiment",
            
            "": lambda : ""
            }   
            url = 'http://' + servicelist[service]()
            result = ""    
            print("*** Calling API ***: " + service)
            print(method)
            if method == "get":
                response = requests.get(url=url, params=post_param)
                result = response
            else:
                response = requests.post(url=url, json=post_param)
                result = response.text            
            
            return result
        except Exception as e:    
            print("Error occured calling the API function:")
            print("Error description: ", str(e))
            return e
