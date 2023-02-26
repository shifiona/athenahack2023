from flask import Flask, request
import json
from flask_cors import CORS
import requests

app = Flask(__name__)
cors = CORS(app)

@app.route('/test', methods=["GET"])
def test():
    return json.dumps({"test1": "COOK"})

@app.route('/recipes', methods=["GET"])
def recipes():
    args = request.args
    return cookbook(int(args.get("counts")),args.get("name"))

def cookbook(x,search):
    
    #makes querystring from searched recipe
    searched = search
    querystring =  {"from":x,"size":x+1, 'q': searched}

    headers = {
	"X-RapidAPI-Key": "6f0aeaeb97msha3c99ab451b845ap1181fdjsn3b002698cd43",
	"X-RapidAPI-Host": "tasty.p.rapidapi.com"
    }  

    cookUrl = "https://tasty.p.rapidapi.com/recipes/list"
    response = requests.request("GET", cookUrl, headers=headers, params=querystring)

    if response.status_code == 200: # Status: OK
        data = response.json()
        if 'results' in data:
            data = data['results'][0]
            if 'recipes' in data:
                data = data['recipes'][0]

        image = data['thumbnail_url']
        name = data['name']
        description = data['description']
        cookTime = data['total_time_tier']
        servings = data['num_servings']
        author = data['credits'][0]['name']
        ratings = int((data['user_ratings']['score'])*100)#(cast into int)

        ingredientsList = data['sections'][0]['components']
        ingredients = ''
        length1 = len(ingredientsList)
        i = 0
        while i < length1:
            ingredient = ingredientsList[i]['raw_text']
            ingredients += ", " + ingredient
            i += 1
        
        instructionsList = data['instructions']
        instructions = ''
        j = 0
        length2 = len(instructionsList)
        while j < length2:
            steps = instructionsList[j]['display_text']
            instructions += " \n " + str(j+1) + ") "+ steps 
            j += 1
        
        recipe = [name, author, ratings, description, image, ingredients, instructions, servings, cookTime]
        
        jsonRecipe = json.dumps(recipe, indent=2)
        print (jsonRecipe)
        return jsonRecipe
        
    else:
        print('error: got response code %d' % response.status_code)
        print(response.text)
        return None


if __name__ == "__main__": 
    app.run(debug=True)
