from bs4 import BeautifulSoup
import json

html_file = "./2023/Joseph Anderson Discord Server - MAIN - dragons-den [666328861985865749] (2023-03-30 to 2023-04-03).html"

with open(html_file, "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

message_divs = soup.find_all("div", class_="chatlog__message-primary")

message_data = []

for message_div in message_divs:
    message_id = message_div.parent.parent["data-message-id"]

    img_filenames = [img["src"] for img in message_div.find_all("img")]
    valid = False
    for img_filename in img_filenames:
        if img_filename.startswith("morbchat"):
            valid = True

    if not valid:
        continue

    # delete header from html, contains user info
    for header in message_div.find_all("div", class_="chatlog__header"):
        header.decompose()

    # delete content, contained edited note
    for content in message_div.find_all("div", class_="chatlog__content"):
        content.decompose()

    user_ids = []
    imgs = message_div.find_all("img")
    for img in imgs:
        if img["src"].startswith("morbchat"):
            img["src"] = f"$$$BASE$$$/2023/morbchats/{img['src']}"
            title = img["title"]
            for word in title.split():
                if word.startswith("morbchat_"):
                    user_ids = word.split("_", 1)[1][:-4].split("_")
        else:
            img["src"] = f"$$$BASE$$$/2023/other_images/{img['src']}"

    # also fix hrefs
    for a in message_div.find_all("a"):
        if a["href"].startswith("morbchat_"):
            a["href"] = f"$$$BASE$$$/2023/morbchats/{a['href']}"

    reaction_count = 0
    reactions = message_div.find_all("div", class_="chatlog__reaction")
    for reaction in reactions:
        count = int(reaction.find("span", class_="chatlog__reaction-count").text)
        reaction_count = max(reaction_count, count)

    assert user_ids, "No user ids found"
    assert message_id, "No message id found"

    message_data.append({"message_id": message_id, "user_ids": user_ids, "content_html": str(message_div), "reaction_count": reaction_count})


with open("./markov_2023.json", "w", encoding="utf-8") as f:
    json.dump(message_data, f, ensure_ascii=False, indent=2)
