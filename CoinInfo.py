import requests 


class CoinQuery:

  def get_json(self,enpoint,request_type = "get",params = None):
    r = requests.Session()
    if(request_type == "get"):
        p = r.get(enpoint,json=params)
    else:
        p = r.post(enpoint,json=params)

    return p.json()

  def get_gas(self):

    URL = "https://ethgasstation.info/api/ethgasAPI.json?"
    json = self.get_json(URL)
    message = str(json["fastest"]/10) + " "+ str(json["fast"]/10)+" " + str(json["average"]/10)

    return message


class TheGraph(CoinQuery):

  def __init__(self ):
    self.URL = "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2"
    self.SHIB_GRAPH_URL = "https://api.thegraph.com/subgraphs/name/shibaswaparmy/exchange"
  def get_eth_price(self):
    

    ETH_PARAM = {            
        "query": "{	pair(id: \"0xb4e16d0168e52d35cacd2c6185b44281ec28c9dc\"){    token0Price  }}"
    } 

    eth_price = float(self.get_json(self.URL,request_type="post",params=ETH_PARAM)["data"]["pair"]["token0Price"])

    return eth_price

  def get_shib_price(self):
    

    SHIB_PARAM = {
        "query": "{	pair(id: \"0x811beed0119b4afce20d2583eb608c6f7af1954f\"){    \n token1Price  }}"
    }

    shib_price_eth = float(self.get_json(self.URL,request_type="post",params=SHIB_PARAM)["data"]["pair"]["token1Price"])

    return shib_price_eth * self.get_eth_price()

  def get_shib_volume(self):

    SHIB_PARAM = {
        "query": "{ pairHourDatas(orderDirection: desc,  where: {    pair: \"0x811beed0119b4afce20d2583eb608c6f7af1954f\"  },  orderBy: hourStartUnix ,  first: 1	){	hourlyVolumeUSD }}"
    }

    volume = int(float(self.get_json(self.URL,params= SHIB_PARAM,request_type="POST")["data"]["pairHourDatas"][0]["hourlyVolumeUSD"]))

    return volume


  def get_shib_marketcap(self):        
    circ_supply = 1e15

    return circ_supply * self.get_shib_price()

  def get_bone_price(self):
    params = {
      "query" : "{tokens(where:{id:\"0x9813037ee2218799597d83d4a5b6f3b6778218d9\"},first:1000,orderBy:id){derivedETH,id}}"
    }
    bone_price_eth = float(self.get_json(self.SHIB_GRAPH_URL,request_type="post",params=params)["data"]["tokens"][0]['derivedETH'])
    eth_price = self.get_eth_price()

    return bone_price_eth * eth_price
    

  def get_leash_price(self):
    params = {
        "query" : "{ pair(id: \"0x874376be8231dad99aabf9ef0767b3cc054c60ee\"){   \n token1Price  }}"
    }         

    leash_price_eth = float(self.get_json(self.URL,request_type="post",params=params)["data"]["pair"]["token1Price"])
    eth_price = self.get_eth_price()

    return eth_price*leash_price_eth

  def get_swap_tvl(self):
    params = {"operationName":"dayDatasQuery","variables":{"first":1},"query":"query dayDatasQuery($first: Int! = 1, $date: Int! = 0) {\n  dayDatas(first: $first, orderBy: date, orderDirection: desc) {\n    id\n    date\n    volumeETH\n    volumeUSD\n    untrackedVolume\n    liquidityETH\n    liquidityUSD\n    txCount\n    __typename\n  }\n}\n"}
    
    tvl = int(float(self.get_json(self.SHIB_GRAPH_URL,request_type="post",params=params)["data"]["dayDatas"][0]["liquidityUSD"]))

    return tvl

