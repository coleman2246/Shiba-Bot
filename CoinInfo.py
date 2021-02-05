import requests 



def get_json(PARAMS):
    
  # api-endpoint 
  URL = "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2"
  

  # sending get request and saving the response as response object 
  r = requests.Session()
  p = r.post(URL, json=PARAMS )
    
  return p.json()
  

def get_shib_price_eth():
  # defining a params dict for the parameters to be sent to the API 

  SHIB_PARAM = {
    "query": "{	pair(id: \"0x811beed0119b4afce20d2583eb608c6f7af1954f\"){    \n token1Price  }}"
    

  }
  shib_price_eth = float(get_json(SHIB_PARAM)["data"]["pair"]["token1Price"])
  return shib_price_eth


def get_shib_hour_volume_usd():
  # defining a params dict for the parameters to be sent to the API 

  SHIB_PARAM = {
    "query": "{ pairHourDatas(orderDirection: desc,  where: {    pair: \"0x811beed0119b4afce20d2583eb608c6f7af1954f\"  },  orderBy: hourStartUnix ,  first: 1	){	hourlyVolumeUSD }}"
    

  }
  volume = int(float(get_json(SHIB_PARAM)["data"]["pairHourDatas"][0]["hourlyVolumeUSD"]))
  return volume


def get_shib_price_usd():
    
  # defining a params dict for the parameters to be sent to the API 
  ETH_PARAM = {
      
    "query": "{	pair(id: \"0xb4e16d0168e52d35cacd2c6185b44281ec28c9dc\"){    token0Price  }}"
      
    } 

  eth_price = float(get_json(ETH_PARAM)["data"]["pair"]["token0Price"])
  shib_price_eth = float(get_shib_price_eth())
  return shib_price_eth*eth_price


def get_eth_gas():
  URL = "https://ethgasstation.info/api/ethgasAPI.json?"

  r = requests.Session()
  p = r.get(URL)
    
  return p.json()
  