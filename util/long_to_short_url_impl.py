# Author : Aashish
# Implementation Tiny URL

import random
import string
import base64

from util.db_impl import getFirst

# method takes in the object and url to convert and recursively create and identify if the key exist in the db
# if exist: recreate
# if new: save and retrurn the key value as Tiny Url
def short_url_generator(shortToLongLookup, urlToConvert):
	allChars = string.ascii_lowercase + string.ascii_uppercase + string.digits

	while True:
		shortRandomizedKey = random.choices(allChars, k = 7)
		stringfyShortRandomizedKey = "".join(shortRandomizedKey)
		print('stringfyShortRandomizedKey :', stringfyShortRandomizedKey)
		url = stringfyShortRandomizedKey + urlToConvert
		print('concatenated URL: ', url)
		encodedUrlByte = base64.b64encode(url.encode("ascii"))
		encodedUrl = str(encodedUrlByte, "ascii")[0:7]

		print('encoded_url :', encodedUrl)
		short_url = getFirst(shortToLongLookup, encodedUrl)
		if not short_url:
			return (encodedUrl)
		else:
			return short_url_generator(shortToLongLookup, urlToConvert)
