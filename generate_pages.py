import requests
import json
import jinja2

def queryElements(required_tags):
    matchingElements = []
    for element in elementss:
      for tag in required_tags:
        if tag not in element.tags:
          break
        matchingElementts.append(element)
    return matchingElements

templateLoader = jinja2.FileSystemLoader(searchpath="./templates")
templateEnv = jinja2.Environment(loader=templateLoader)
templateEnv.globals['queryElements'] = queryElements

# generate elements
sheetIndex = 2
response = requests.get("https://spreadsheets.google.com/feeds/list/1NXj5-cpQ7Cnn3fB-lKoRFCjJ0GTC34AULyHQF4zYek0/{}/public/values?alt=json".format(sheetIndex))
sheet = json.loads(response.content)

elements = []
for row in sheet["feed"]["entry"]:
    args = {
      "description": row["gsx$description"]["$t"],
      "id": row["gsx$name"]["$t"].replace(" ", "_").lower(),
      "name": row["gsx$name"]["$t"],
      "tags": row["gsx$tags"]["$t"].split(','),
      "weight": int(row["gsx$weight"]["$t"] or 0),
    }
    elements.append(args)
    template = templateEnv.get_template("elements.html")
    outputText = template.render(args)
    text_file = open("static/{}_page.html".format(args["id"]), "w")
    text_file.write(outputText)
    text_file.close()
with open('static/elements.json', 'w') as outfile:
    json.dump(elements, outfile)

print("encounters")
# generate encounters
sheetIndex = 1
response = requests.get("https://spreadsheets.google.com/feeds/list/1NXj5-cpQ7Cnn3fB-lKoRFCjJ0GTC34AULyHQF4zYek0/{}/public/values?alt=json".format(sheetIndex))
sheet = json.loads(response.content)

encounters = []
for row in sheet["feed"]["entry"]:
    args = {
      "id": row["gsx$id"]["$t"],
      "description": row["gsx$description"]["$t"],
      "clue_trigger": row["gsx$cluetrigger"]["$t"],
      "clue_trigger_percent": float(row["gsx$cluetriggerpercent"]["$t"] or 0),
      "trigger": row["gsx$trigger"]["$t"],
      "trigger_percent": float(row["gsx$triggerpercent"]["$t"] or 0),
      "tags": row["gsx$tags"]["$t"].split(','),
      "weight": int(row["gsx$weight"]["$t"] or 0),
    }
    encounters.append(args)
with open('static/encounters.json', 'w') as outfile:
    json.dump(encounters, outfile)

