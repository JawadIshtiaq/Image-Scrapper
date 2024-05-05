import requests
from bs4 import BeautifulSoup
import json
import csv
import os
import imghdr

def get_image_urls(query, num_images=20):
    image_urls = []
    start_index = 0

    while len(image_urls) < num_images:
        search_url = f"https://www.google.com/search?q={query}&tbm=isch&start={start_index}"

        # Set a user agent to avoid bot detection
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}

        # Send an HTTP GET request to the search URL
        response = requests.get(search_url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            img_tags = soup.find_all('img')

            # Extract image URLs from img tags and filter out non-image URLs
            page_image_urls = [img['src'] for img in img_tags if img['src'].startswith(('http://', 'https://'))]

            # Take only the specified number of images
            page_image_urls = page_image_urls[:num_images - len(image_urls)]
            
            image_urls.extend(page_image_urls)
            
            # Increment the start index for the next page
            start_index += len(page_image_urls)
        else:
            print("Failed to retrieve search results for page")

    return image_urls[:num_images]

# ... (Rest of the code remains the same)


def save_to_csv(image_urls, filename):
    with open(filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Image URL"])
        for url in image_urls:
            csv_writer.writerow([url])

def download_images(image_urls, folder_path):
    os.makedirs(folder_path, exist_ok=True)
    for i, url in enumerate(image_urls):
        response = requests.get(url)
        if response.status_code == 200:
            image_data = response.content
            image_format = imghdr.what(None, h=image_data)

            if image_format == 'jpeg':
                with open(os.path.join(folder_path, f"image_{i+1}.jpg"), 'wb') as f:
                    f.write(image_data)
                print(f"Downloaded image {i+1}")
            else:
                print(f"Ignored non-JPEG image {i+1}")
        else:
            print(f"Failed to download image {i+1} from URL: {url}")

if __name__ == '__main__':
    search_query = input("Enter your search query: ")
    num_images_to_scrape = int(input("Enter the number of images to scrape: "))
    output_filename = input("Enter the CSV filename to save the results: ")
    output_folder = input("Enter the folder to save the images: ")

    image_urls = get_image_urls(search_query, num_images_to_scrape)

    # Save the image URLs to a CSV file
    save_to_csv(image_urls, output_filename)

    # Download and save only JPEG images to a folder
    download_images(image_urls, output_folder)

    print(f"Image URLs saved to {output_filename}")
    print(f"Images downloaded to {output_folder}")