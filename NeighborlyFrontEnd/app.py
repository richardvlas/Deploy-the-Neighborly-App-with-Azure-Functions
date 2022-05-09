import logging.config
import os
from flask import Flask, Blueprint, request, jsonify, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
import settings
import requests
import json


app = Flask(__name__)
Bootstrap(app)


@app.route('/')
def home():
    response = requests.get(settings.API_URL + '/getAdvertisements')
    response2 = requests.get(settings.API_URL + '/getPosts')

    ads = response.json()
    posts = response2.json()
    
    return render_template("index.html", ads=ads, posts=posts)


@app.route('/ad/add', methods=['GET'])
def add_ad_view():
    return render_template("new_ad.html")


@app.route('/ad/edit/<id>', methods=['GET'])
def edit_ad_view(id):
    response = requests.get(settings.API_URL + '/getAdvertisement?id=' + id)
    ad = response.json()
    return render_template("edit_ad.html", ad=ad)


# ADD '/ad/delete/<id>'


@app.route('/ad/new', methods=['POST'])
def add_ad_request():
    # Get item from the POST body
    req_data = {
        'title': request.form['title'],
        'city': request.form['city'],
        'description': request.form['description'],
        'email': request.form['email'],
        'imgUrl': request.form['imgUrl'],
        'price': request.form['price']
    }
    response = requests.post(
        settings.API_URL + '/createAdvertisement', json=json.dumps(req_data)
    )
    return redirect(url_for('home'))


@app.route('/ad/update/<id>', methods=['POST'])
def update_ad_request(id):
    # Get item from the POST body
    req_data = {
        'title': request.form['title'],
        'city': request.form['city'],
        'description': request.form['description'],
        'email': request.form['email'],
        'imgUrl': request.form['imgUrl'],
        'price': request.form['price']
    }

    response = requests.put(settings.API_URL + '/updateAdvertisement?id=' + id, json=json.dumps(req_data))
    return redirect(url_for('home'))



# running app
def main():
    print(' ----->>>> Flask Python Application running in development server')
    app.run(
        host=settings.SERVER_HOST, 
        port=settings.SERVER_PORT, 
        debug=settings.FLASK_DEBUG
    )


if __name__ == "__main__":
    main()