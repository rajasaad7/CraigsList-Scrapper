import re
import time
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, redirect, url_for
from craigslist import CraigslistHousing

app = Flask(__name__)
app.config['SECRET_KEY'] = 'our very hard to guess secretfir'


def start_scrapper(cit, cat):
    print("Starting to scrape data...")
    def housing(citi_code, category_code):

        cl_h = CraigslistHousing(site=citi_code, category=category_code, filters={'posted_today': True})

        for result in cl_h.get_results(sort_by='newest', geotagged=True):
            id = str(result["id"]).replace(",", "")
            name = str(result["name"]).replace(",", "")
            url = str(result["url"]).replace(",", "")
            date_time = str(result["datetime"]).replace(",", "")
            last_update = str(result["last_updated"]).replace(",", "")
            price = str(result["price"]).replace(",", "")
            location = str(result["where"]).replace(",", "")
            geolocation = str(result["geotag"]).replace(",", " and ")

            asd = requests.get(result["url"])
            time.sleep(2)
            soup = BeautifulSoup(asd.text, "html.parser")
            bsd = soup.find('section', {'id': 'postingbody'})
            discription = bsd.text.replace("\n", " ").replace(",", "").strip("  ").strip(
                "QR Code Link to This Post      ")
            phone_number = re.findall("(\d{3}[-\.\s]\d{3}[-\.\s]\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]\d{4}|\d{3}[-\.\s]\d{4})", discription)
            PhoneNumber = ''
            for phone in phone_number:
                PhoneNumber += phone + "/"
            emails = re.findall("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", discription)
            Emails = ''
            for email in emails:
                Emails += email + "/"


            to_write = id + "," + name + "," +PhoneNumber.replace(",","")+ "," +Emails.replace(",","")+ "," + discription + "," + url + "," + date_time + "," + last_update + "," + price + "," + location + "," + geolocation + "\n"
            write_to_file.write(to_write)
            print(to_write)
        write_to_file.close()

    write_to_file = open("output.csv", "w", encoding='utf-8')
    header = "ID,Title,Phone_Number,Email,Discription,URL,TimePosted,LastUpdate,Price,Location,GeoCodes\n"
    write_to_file.write(header)
    housing(cit, cat)


@app.route('/thank-you')
def thank_you():
    return render_template('thank-you.html')


# Simple form handling using raw HTML forms

@app.route('/', methods=['GET', 'POST'])
def scrapping():
    error = ""
    if request.method == 'POST':
        # Form being submitted; grab data from form.
        city = request.form['city']
        category = request.form['category']
        start_scrapper(city, category)
        return redirect(url_for('thank_you'))

    # Render the sign-up page
    return render_template('index.html', message=error)


# Run the application
app.run(debug=True)
