import yaml

class Configservice():
    ##----------------------- Config Setup -----------------------##
    ## Load data config file
       
    dataconfigyml = open("dags/src/dataconfig.yml")
    dataconfig = yaml.load(dataconfigyml, Loader=yaml.FullLoader)

    ## Get config for market data source token
    @staticmethod
    def getMarketSourceToken():
        cs = Configservice()
        marketdatasrctkn = cs.dataconfig["auth"]["token"]
        return marketdatasrctkn

    ## Get ticker list of raw market data
    @staticmethod
    def getTickerList():
        cs = Configservice()
        return cs.dataconfig["tickersubscribelist"]
