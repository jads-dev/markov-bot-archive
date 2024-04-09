# %%
from bs4 import BeautifulSoup
import json

html_file = "./2024/Joseph Anderson Discord Server - MAIN - dragons-den [666328861985865749].html"

with open(html_file, "r", encoding="utf-8") as f:
    html = f.read()

print("parsing html")
soup = BeautifulSoup(html, "lxml")

print("getting message divs")
message_divs = soup.find_all("div", class_="chatlog__message-container")
# %%
message_data = []


for message_div in message_divs:

    message_id = message_div["data-message-id"]

    author_span = message_div.find("span", class_="chatlog__author")
    if not author_span:
        continue
    user_id = author_span["data-user-id"]

    if not user_id or user_id != "959116994614022145":
        continue

    user_name = message_div.find("span", class_="chatlog__author").text

    message_content = message_div.find("div", class_="chatlog__content").text

    reaction_count = 0
    reactions = message_div.find_all("div", class_="chatlog__reaction")
    for reaction in reactions:
        count = int(reaction.find("span", class_="chatlog__reaction-count").text)
        reaction_count = max(reaction_count, count)

    message_data.append(
        {
            "message_id": message_id,
            "content_html": str(message_div),
            "user_name": user_name,
            "message_content": message_content,
            "reaction_count": reaction_count,
        }
    )



with open("./markov_2024.json", "w", encoding="utf-8") as f:
    json.dump(message_data, f, ensure_ascii=False, indent=2)

# %%
