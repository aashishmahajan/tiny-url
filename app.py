# Author : Aashish
# Implementation Tiny URL
# https://pypi.org/project/Flask-SQLAlchemy/

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from util.db_impl import getFirst, insertRecordsInDb
from util.long_to_short_url_impl import short_url_generator

global app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///longToShortMap.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# leverage in app dynamic db table creation, it can be used for leveraging and ensuring db can be stored and referred.
@app.before_first_request
def create_tables():
	db.create_all()


class shortToLongLookup(db.Model):
	id_ = db.Column("id_", db.INTEGER, primary_key = True)
	# effective last 7 to be stripped-out of the URL
	# handle edge case on the URL's
	shortenUrl = db.Column("shortenUrl", db.String(7))
	originalUrl = db.Column("originalUrl", db.String())

	def __init__(self, shortenUrl, originalUrl):
		self.shortenUrl = shortenUrl
		self.originalUrl = originalUrl


# method takes the url and return the valid output for tiny url if exist else basic notification
def retrieveTinyUrl(urlToConvert):
	print('Request received to retrieve Tiny URL')
	# urlToConvert = request.form["retrieveTinyUrl"]
	lastIndex = int(urlToConvert.rindex("/")) + 1
	# print(lastIndex, len(str1))
	shortUrl = urlToConvert[lastIndex: 27]
	print(shortUrl)
	originalUrl = None
	if None != shortUrl:
		original = getFirst(shortToLongLookup, shortUrl)
		if (None != original):
			print('a valid original Url found!')
			originalUrl = original.originalUrl
		else:
			print('a original Url not found for tiny url!')
	return originalUrl


# method takes the short url and retrieve the original url
def generateTinyUrl(urlToConvert):
	print('Request received to generate Tiny URL')
	# urlToConvert = request.form["generateTiny"]
	shortenedUrl = short_url_generator(shortToLongLookup, urlToConvert)
	print('tiny url generated for original url:', urlToConvert, 'tiny url generated:', shortenedUrl)
	new_url = shortToLongLookup(shortenedUrl, urlToConvert)
	insertRecordsInDb(db, new_url)

	return shortenedUrl


@app.route('/', methods = ['POST', 'GET'])
def home():
	if request.method == "POST":
		if "generateTiny" in request.form:
			shortenedUrl = generateTinyUrl(request.form["generateTiny"])
			return redirect(url_for("redirectToShortUrl", url = shortenedUrl))
		elif "retrieveTiny" in request.form:
			tinyValue = request.form["retrieveTiny"]
			originalUrl = retrieveTinyUrl(tinyValue)
			if None != originalUrl:
				return redirect(originalUrl)
			else:
				return f'<div class="container"><h1>No Url Found for '+ tinyValue+'</h1><br/><a href="http://127.0.0.1:8082/">BACK TO HOME</a></div>'

		elif 'retrieveAll' in request.form:
			return redirect(url_for("allTinyUrls"))
	else:
		return render_template('homePage.html')


@app.route('/tinyUrl/<url>')
def redirectToShortUrl(url):
	return render_template('generatedUrl.html', longToShortUrlVal = ("https://tinyUrl.com/" + url))


@app.route('/originalUrl')
def redirectToNotFoundUrl():
	print('original url:', )
	return render_template('nonFound.html', url = "#")


@app.route('/allTinyUrls')
def allTinyUrls():
	return render_template('allTinyUrls.html', vals = shortToLongLookup.query.all())


@app.route('/cleanup')
def cleanupUrls():
	print('request received for the db cleanup')
	count = db.session.query(shortToLongLookup).count()
	if count == 0:
		return render_template('successDelete.html', vals = '0')
	countDeleted = db.session.query(shortToLongLookup).delete()
	db.session.commit()
	return render_template('successDelete.html', countDeleted = countDeleted)


if __name__ == '__main__':
	app.run(port = 8082, debug = True)
