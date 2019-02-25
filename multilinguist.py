import requests
import json
import random

class Multilinguist:
  """This class represents a world traveller who knows
  what languages are spoken in each country around the world
  and can cobble together a sentence in most of them
  (but not very well)
  """

  translatr_base_url = "http://bitmakertranslate.herokuapp.com"
  countries_base_url = "https://restcountries.eu/rest/v2/name"
  #{name}?fullText=true
  #?text=The%20total%20is%2020485&to=ja&from=en

  def __init__(self):
    """Initializes the multilinguist's current_lang to 'en'

    Returns
    -------
    Multilinguist
        A new instance of Multilinguist
    """
    self.current_lang = 'en'

  def language_in(self, country_name):
    """Uses the RestCountries API to look up one of the languages
    spoken in a given country

    Parameters
    ----------
    country_name : str
         The full name of a country.

    Returns
    -------
    bool
        2 letter iso639_1 language code.
    """
    params = {'fullText': 'true'}
    response = requests.get(f"{self.countries_base_url}/{country_name}", params=params)
    json_response = json.loads(response.text)
    return json_response[0]['languages'][0]['iso639_1']

  def travel_to(self, country_name):
    """Sets current_lang to one of the languages spoken
    in a given country

    Parameters
    ----------
    country_name : str
        The full name of a country.

    Returns
    -------
    str
        The new value of current_lang as a 2 letter iso639_1 code.
    """
    local_lang = self.language_in(country_name)
    self.current_lang = local_lang
    return self.current_lang

  def say_in_local_language(self, msg):
    """(Roughly) translates msg into current_lang using the Transltr API

    Parameters
    ----------
    msg : str
        A message to be translated.

    Returns
    -------
    str
        A rough translation of msg.
    """
    params = {'text': msg, 'to': self.current_lang, 'from': 'en'}
    response = requests.get(self.translatr_base_url, params=params)
    json_response = json.loads(response.text)
    return json_response['translationText']


class MathGenius(Multilinguist):
    """ Adds up lists of numbers and reports the totals in local language """

    def __init__(self):
        super().__init__()

    def report_total(self, num_list):
        total = 0
        for num in num_list:
            total += num
        return self.say_in_local_language('The total is {}'.format(total))


class QuoteCollector(Multilinguist):
    """ Keeps a collection of quotes and translates in local language"""

    def __init__(self):
        super().__init__()
        self.quotes = []

    def add_quote(self, new_quote):
        self.quotes.append(new_quote)

    def share_random_quote(self):
        random_quote = random.choice(self.quotes)
        return self.say_in_local_language('{}'.format(random_quote))

#--------------------------------------------------------------------------
#Testing MathGenius
# me = MathGenius()
# print(me.report_total([23,45,676,34,5778,4,23,5465]))
# me.travel_to("India")
# print(me.report_total([23,45,676,34,5778,4,23,5465]))
# me.travel_to("Italy")
# print(me.report_total([23,45,676,34,5778,4,23,5465]))

#--------------------------------------------------------------------------
#Testing QuoteCollector
# fav_quotes = QuoteCollector()
# fav_quotes.add_quote("One man’s crappy software is another man’s full time job")
# fav_quotes.add_quote("There are two ways to write error-free programs; only the third one works")
# fav_quotes.add_quote("Programming is like sex. One mistake and you have to support it for the rest of your life")
# print(fav_quotes.share_random_quote())
# fav_quotes.travel_to("Italy")
# print(fav_quotes.share_random_quote())
