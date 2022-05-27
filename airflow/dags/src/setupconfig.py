import yaml
from airflow.models import Variable

class Configservice():
    ##----------------------- Config Setup -----------------------##
    ## Load data config file
       
    dataconfigyml = open("dags/src/dataconfig.yml")
    dataconfig = yaml.load(dataconfigyml, Loader=yaml.FullLoader)

    ## Get polygon.io token
    @staticmethod
    def getPolygonToken():
        return Variable.get("POLYGON_API_KEY", default_var = "")
    
    ## Get Finnhub.io token
    @staticmethod
    def getFinnhubToken():
        return Variable.get("FINNHUB_API_KEY", default_var = "")

    ## Get ticker list of raw market data
    @staticmethod
    def getTickerList():
        cs = Configservice()
        return cs.dataconfig["tickersubscribelist"]
