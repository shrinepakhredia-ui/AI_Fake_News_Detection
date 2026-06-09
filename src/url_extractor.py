from newspaper import Article
from src.source_checker import check_source

# Extract Article


def extract_article(url):
    """
    Extract article information from a news URL.

    Returns
    -------
    dict
        success
        title
        text
        authors
        publish_date
        top_image
        error
    """

    try:

        article = Article(url)

        article.download()

        article.parse()

        source_info = check_source(url)

        return {

            "success": True,

            "title": article.title,

            "text": article.text,

            "authors": article.authors,

            "publish_date": article.publish_date,

            "top_image": article.top_image,

            "trusted":source_info["trusted"],

            "publisher":source_info["publisher"],

            "domain":source_info["domain"],

            "error": None

        }

    except Exception as e:

        return {

            "success": False,

            "title": "",

            "text": "",

            "authors": [],

            "publish_date": None,

            "top_image": "",

            "error": str(e)

        }


# Testing


if __name__ == "__main__":

    url = input("Enter News URL:\n\n")

    result = extract_article(url)

    print("\n" + "=" * 60)

    if result["success"]:

        print("Title :", result["title"])

        print("\nAuthors :", result["authors"])

        print("\nPublish Date :", result["publish_date"])

        print("\nImage :", result["top_image"])

        print("\nArticle Preview:\n")

        print(result["text"][:1000])

    else:

        print("Extraction Failed")

        print(result["error"])

    print("=" * 60)