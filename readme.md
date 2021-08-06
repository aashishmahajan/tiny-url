#TINY URL
**Implementation Documented By : Aashish Mahajan**
#
* the implementation intends to store a big url make a short redirectable url available so that it can use the byte/character space in an optimized way. 

* ex: use can share a website or content or article: any sort of media by sharing the tinyurl for a big url. a url such as:
https://www.youtube.com/watch?v=xPfpUcnKico will become **shortenUrl/fjrpntuy**. the 43 byte url gets converted to an easily accessble and retrieveable url of 20 byte hence saving **20 Bytes**


_**The an effective implementation Ensure:**_
* the implementation offers a consistent and efficient way to create tiny url. 
* url submitted to the service should be responded back with a shorten url. 
* the shorten url when submitted back should be able to find the matching url if exist.<br> 1. ensure that the same URL if submitted to be shorten, it either returns a unique key already stored or generates a new tiny url depending on how cdn or load balancer or data has been sharded or partitioned.

* the service should be highly scalable and available. This can be achieved by using following <br> 1. use an **N server configuration**, where in all the servers have their own processing logic <br> 2. All the servers can be interfaced with a **zookeeper instance** which also interfaces with cache + serves as a master of configuration. It knows at any given time which servers are available and which servers are out of commission. It routes the request from LB appropriately.
<br> 3. All the incoming requests are routed through LB i.e. Load Balancer which routes the traffic depending on instance, or hosting or server location. This is to ensure that all the service is highly available, and are available through local CDN 



Please refer to the **../flow_diagram.png** for an example efficient system.
* Assumption: System to return a https://tinyurl.com/{encoded 7 letter URL}:
* the character base that I intend to use AlphaNumeric i.e all character Map encoded in base64 i.e.<br> base 64 offers 64 pow 7 = 68,719,476,736 possible combination that can be used.   
       
other approach includes using: **pip install short_url** where one can use a decode and encode url and refer it in a local schema. 


ex: **Code**
******
import short_url <br>
url = short_url.encode_url(12) <br>
print url  # this URL can dumped in the DB for future access.<br>
output : LhKA


**on return**
 
key = short_url.decode_url(url) <br> # can be retrieved from db or fast decrypt and returned <br>
print key <br>
12 <br>

********
# **How To Run The Project:**
1. download the code from github.com 
2. Pre-Requisite: Python 3.8, Pip <br> a. **install** flask : pip install Flask <br> b. **install** in app db SQLAlchemy: pip install Flask-SQLAlchemy <br>c. select the venv in which python interpretor is selected.
   
3. the code is configured on port:8082 and once main the function in app.py is executed <br> **the app is live on url: http://127.0.0.1:8082**
4. Function Implemented: <br>
a. **Convert Url to Tinyurl:** 
    this method is designed to generate a new tinyUrl every occurence to avoid any colusion. it picks 7 byte base64 encoded value from all lower case string, upper case string and digit (for more we can always add special characters)<br>
b. **Identify/Lookup Tiny Url to Long :** retrieves and redirects if the matching tinyUrlKey is identified in the db.if not identified, error message would be shown. <br/>
c. **Show All Keys :** retrieves all the key that exist in the db in tabular format <br>
d. **{url}/clean** : <br> i. url :_http://127.0.0.1:8082_   , If data exist in the schema, it would allow the user to delete all entries. retrieves the count deleted. 
 
 
