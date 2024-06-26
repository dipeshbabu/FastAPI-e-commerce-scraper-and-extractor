# FastAPI E-commerce Scraper and Extractor

A FastAPI application that scrapes e-commerce websites and extracts product details using a combination of BeautifulSoup and [BERT](https://huggingface.co/google-bert/bert-base-uncased).

## Choice of LLM and Rationale

For this project, BERT (Bidirectional Encoder Representations from Transformers) was chosen due to its strong performance in understanding context and relationships in text. BERT's pre-trained model on a large corpus of text data makes it a robust choice for processing and extracting meaningful information from HTML content, especially in an e-commerce context.

## API Design and Implementation

The API is implemented using FastAPI, known for its performance and ease of use. The design includes two primary endpoints:

1. GET `/`: Scrapes book data from "Books to Scrape" by iterating through multiple pages, extracting details such as titles, prices, availability, and image URLs.

2. POST `/extract_attributes`: Accepts an HTML block as input, processes it using BERT to extract attributes, and identifies their corresponding CSS selectors or XPaths.

## Setup

1. **Clone the repository**:

   ```sh
   git clone https://github.com/dipeshbabu/FastAPI-e-commerce-scraper-and-extractor.git
   cd FastAPI-e-commerce-scraper-and-extractor
   ```

2. **Create and activate a virtual environment**:

   - **Using `venv` (Python 3.3+)**:

     ```sh
     python -m venv grepenv
     source grepenv/bin/activate  # On Windows use `grepenv\Scripts\activate`
     ```

   - **Using `virtualenv`**:
     ```sh
     virtualenv grepenv
     source grepenv/bin/activate  # On Windows use `grepenv\Scripts\activate`
     ```

3. **Install dependencies**:

   ```sh
   pip install -r requirements.txt
   ```

4. **Run the FastAPI server**:

   ```sh
   uvicorn main:app --reload
   or
   fastapi dev main.py
   ```

5. **Access the API**:

- Navigate to `http://127.0.0.1:8000/` to test the scraping endpoint.
- Use an API client like Postman to test the `/extract_attributes` endpoint by sending a POST request with an HTML block.

## API Endpoints

### Scrape Books

- **URL**: `/`
- **Method**: `GET`
- **Description**: Scrapes book data from "Books to Scrape" website.
- **Response**: JSON array of books with details.

### Extract Attributes

- **URL**: `/extract_attributes`
- **Method**: `POST`
- **Description**: Extracts attributes from an HTML block.
- **Request Body**:
  ```json
  {
    "html": "<html_content>"
  }
  ```
- **Response**: JSON object with extracted data and CSS selectors.

## Examples

### Example Response for `/`

```json
[
{
"title": "A Light in the Attic",
"price": "£51.77",
"availability": "In stock",
"image_url": "https://books.toscrape.com/media/cache/fe/00/fe0012b0bce617e77a6d68b3e89f9254.jpg"
},
...
]
```

### Example Input for `/extract_attributes`

```json
{
  "html": "<div class='product'><h3 class='product-name'>Sample Book</h3><p class='price_color'>$20.00</p><p class='instock availability'>In stock</p><div class='image_container'><img src='sample-image.jpg'/></div></div>"
}
```

### Example Output for `/extract_attributes`

```json
{
  "product_name": {
    "value": "Sample Book",
    "selector": "//h3[@class='product-name']"
  },
  "price": {
    "value": "$20.00",
    "selector": "//p[@class='price_color']"
  },
  "description": {
    "value": "In stock",
    "selector": "//p[@class='description']"
  },
  "image_url": {
    "value": "https://example.com/product-image.jpg",
    "selector": "//div[@class='image_container']/img"
  }
}
```

## Enhanced HTML Processing with BERT and Heuristics

**Dynamic Rule-Based System**

Develop rules that adapt based on the structure detected by BERT and BeautifulSoup. For example:

- If a price is found next to a product name, but the exact HTML structure varies, create rules that handle these variations.
- Use BERT to understand context within product descriptions and map these descriptions back to their HTML tags using patterns detected during processing.

**Fallback Mechanisms**

Implement fallback mechanisms when BERT's predictions are ambiguous. For instance:

- If BERT fails to extract a clear price, use regular expressions and heuristics to identify and extract the price.

## Performance Metrics and Evaluation

- **Accuracy**: Evaluated by comparing the extracted data against known correct values.
- **Precision and Recall**: Calculated for attribute extraction to understand the model's effectiveness in correctly identifying and extracting relevant information.

## Security Considerations

- **Input Validation**: Sanitized HTML inputs to prevent injection attacks.
- **Rate Limiting**: Implemented rate limiting to prevent abuse of the API.

## Future Improvements

- **Scalability**: Implement load balancing to handle high traffic.
- **Enhanced Model**: Fine-tune BERT for better performance on e-commerce data.

## Comparative Analysis

BERT was chosen over other models like LLaMA or Vicuna due to its strong performance in text processing tasks, well-balanced trade-off between complexity and availability of pre-trained models. Future iterations could explore these models for potentially improved performance or specific advantages in understanding HTML content.
