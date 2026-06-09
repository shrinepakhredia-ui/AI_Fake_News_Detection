from urllib.parse import urlparse


TRUSTED_SOURCES = {

    "indianexpress.com": "The Indian Express",

    "thehindu.com": "The Hindu",

    "hindustantimes.com": "Hindustan Times",

    "timesofindia.indiatimes.com": "Times of India",

    "reuters.com": "Reuters",

    "apnews.com": "Associated Press",

    "bbc.com": "BBC News",

    "ndtv.com": "NDTV",

    "theprint.in": "The Print",

    "livemint.com": "Mint",

    "business-standard.com": "Business Standard",

    "economictimes.indiatimes.com": "Economic Times",

    "moneycontrol.com": "Moneycontrol",

    "deccanherald.com": "Deccan Herald",

    "scroll.in": "Scroll",

    "thewire.in": "The Wire",

    "outlookindia.com": "Outlook India",

    "ddnews.gov.in": "DD News",

    "prasarbharati.gov.in": "Prasar Bharati",

    "indiatoday.in": "India Today",

    "firstpost.com": "Firstpost",

    "newslaundry.com": "Newslaundry",

    "financialexpress.com": "Financial Express",

    "prsindia.org": "PRS India",

    "manoramaonline.com": "Malayala Manorama",

    "anandabazar.com": "Anandabazar Patrika"

}


def check_source(url: str):

    try:

        domain = urlparse(url).netloc.lower()

        domain = domain.replace("www.", "")

        for trusted_domain, publisher in TRUSTED_SOURCES.items():

            if domain.endswith(trusted_domain):

                return {

                    "trusted": True,

                    "publisher": publisher,

                    "domain": domain

                }

        return {

            "trusted": False,

            "publisher": "Unknown",

            "domain": domain

        }

    except Exception:

        return {

            "trusted": False,

            "publisher": "Unknown",

            "domain": ""

        }