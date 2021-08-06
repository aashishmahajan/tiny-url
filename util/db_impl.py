# implementation for the randomized Key get from DB
# db function to retrieve the fist match found for the key.
def getFirst(shortToLongLookup, stringfyShortRandomizedKey):
	print('find first occurrence of key:', stringfyShortRandomizedKey)
	return shortToLongLookup.query.filter_by(shortenUrl = stringfyShortRandomizedKey).first()


# db function to insert the record
def insertRecordsInDb(db, new_url):
	print('request received to insert record in db:', new_url.shortenUrl, new_url.originalUrl)
	db.session.add(new_url)
	db.session.commit()
	# print('record saved in db:', info, insert)
	return
