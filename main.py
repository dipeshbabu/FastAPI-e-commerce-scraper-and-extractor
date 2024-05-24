import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import BertTokenizer, BertForMaskedLM
import re
import torch

app = FastAPI()


class HTMLInput(BaseModel):
    html: str


tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertForMaskedLM.from_pretrained("bert-base-uncased")


def scrape_page(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve page: {url}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    books = []
    for book in soup.find_all("article", class_="product_pod"):
        title = book.h3.a["title"]
        price = book.find("p", class_="price_color").text.strip()
        availability = book.find("p", class_="instock availability").text.strip()
        image_url = book.find("div", class_="image_container").img["src"].strip()
        image_url = "https://books.toscrape.com/" + image_url

        book_details = {
            "title": title,
            "price": price,
            "availability": availability,
            "image_url": image_url,
        }
        books.append(book_details)

    return books


@app.post("/extract_attributes")
async def extract_attributes(html_input: HTMLInput):
    soup = BeautifulSoup(html_input.html, "html.parser")
    text = soup.get_text()
    text = re.sub(r"\s+", " ", text).strip()

    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)

    with torch.no_grad():
        outputs = model(**inputs)

    predicted_token_ids = torch.argmax(outputs.logits, dim=-1)
    predicted_tokens = [
        tokenizer.convert_ids_to_tokens(token_id) for token_id in predicted_token_ids[0]
    ]

    extracted_data = {
        "product_name": predicted_tokens[0],
        "price": predicted_tokens[1],
        "description": " ".join(predicted_tokens[2:5]),
        "image_url": "https://example.com/product-image.jpg",
    }

    selectors = {
        extracted_data["product_name"]: "//h3[@class='product-name']",
        extracted_data["price"]: "//p[@class='price_color']",
        extracted_data["description"]: "//p[@class='description']",
        extracted_data["image_url"]: "//div[@class='image_container']/img",
    }

    formatted_data = {
        key: {"value": value, "selector": selectors.get(value)}
        for key, value in extracted_data.items()
    }

    return formatted_data


base_url = "https://books.toscrape.com/catalogue/page-{}.html"
num_pages = 3


@app.get("/")
async def scrape_books():
    all_books = []
    for page_num in range(1, num_pages + 1):
        page_url = base_url.format(page_num)
        books_on_page = scrape_page(page_url)
        all_books.extend(books_on_page)

    return all_books


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
