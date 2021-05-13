import asyncio
from pprint import pprint
from typing import List

from aiogram import Dispatcher
from aiogram.utils.executor import Executor
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from app.config import res_dir
from app.misc import loop, asyncio_executor
from app.models.movie import Movie, Genre, Actor, Director

KINORIUM_BASE_URL = "https://ua.kinorium.com"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
browser = webdriver.Chrome(options=chrome_options, executable_path=res_dir / "chromedriver.exe")


def parse_movies_on_page(page: int, per_page: int = 200) -> List[dict]:
    browser.get(
        f"{KINORIUM_BASE_URL}/R2D2/?order=rating&page={page}&perpage={per_page}&"
        f"nav_type%5B%5D=movie&kr_rating_min=7&imdb_rating_min=7#")
    WebDriverWait(browser, 5).until(EC.presence_of_element_located(
        (By.CSS_SELECTOR,
         "body > div.modalBluring > div > div.table.main-table_content.main-table.table-single-cell."
         "main-container_experimentFixedMenu > div.table-row.table-single-cell > div > div > div.filmList > "
         "div:nth-child(2) > div.filmList__item-content > div.info-box.filmList__item-title-wrap > "
         "div.filmList__item-wrap-title > a > div > i")))
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    soup = BeautifulSoup(browser.page_source, "lxml")
    raw_movies = soup.find_all("div", {"class": "filmList__item-content"})
    movies = []
    for raw_movie in raw_movies:
        movie = {
            "name": raw_movie.find("i", {"class": [
                "movie-title__text",
                "filmList__item-title-link-popup",
                "link-info-movie-type-film"]
            }).text.strip().replace("\xa0", " ").replace("\u200b", "").replace("\xa0", " "),
            "year": raw_movie.find("div", {"class": "select-wrap"}).find("span").text.split(",")[-1].strip(),
        }
        movie_id = raw_movie.find("div", {"class": ["info-box", "filmList__item-title-wrap"]}).get("rel")
        browser.get(f"{KINORIUM_BASE_URL}/{movie_id}")
        movie_page = BeautifulSoup(browser.page_source, "lxml")
        movie["description"] = movie_page.find("meta", {"property": "og:description"}).get("content")
        movie["genres"] = [genre.get("content") for genre in
                           movie_page.find_all("li", {"itemprop": "genre"})]
        movie["actors"] = [
            actor.text.strip() for actor in movie_page.find_all("span", {
                "class": ["cast__name-wrap", "cast__name-wrap_cut"],
                "itemprop": "name"
            })
        ]
        movie["directors"] = list({
            director.find("span", {"class": "cast__name-wrap"}).text.strip()
            for director in movie_page.find_all("div", {
                "class": "item",
                "itemtype": "http://schema.org/Person",
                "itemprop": "director"
            })
        })
        movies.append(movie)
        pprint(movie)
    return movies


async def main():
    for page in range(1, 10):
        movies = await loop.run_in_executor(asyncio_executor, parse_movies_on_page, page, 200)
        await asyncio.sleep(0.5)
        for movie in movies:
            genres = [(await Genre.get_or_create(name=genre))[0] for genre in movie["genres"]]
            directors = [(await Director.get_or_create(name=director))[0] for director in movie["directors"]]
            actors = [(await Actor.get_or_create(name=actor))[0] for actor in movie["actors"]]
            db_movie = await Movie.create(
                name=movie["name"],
                year=movie["year"],
                description=movie["description"]
            )
            await db_movie.genres.add(*genres)
            await db_movie.directors.add(*directors)
            await db_movie.actors.add(*actors)



async def on_startup(_dp: Dispatcher):
    await main()


def setup(executor: Executor):
    executor.on_startup(on_startup)
