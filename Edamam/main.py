import requests
import json
import os
import re
import shutil

def writingToFiles(nameOfTheFile,content):
	pass

def isBlank (myString):
    return not (myString and myString.strip())

def payloadConstructor(q,mealType,diet,health,cuisineType,dishType,):
	apid = "4cd0ab6b"
	apkey = "fa1ac224ed371e8aab696b447e424a22"
	payload ={}
	payload['type'] = 'public'
	payload['q'] = q
	payload['app_id'] = "4cd0ab6b"
	payload['app_key']  = "fa1ac224ed371e8aab696b447e424a22"
	if not isBlank(mealType):
		payload['mealType'] = mealType
	if not isBlank(health):
		payload['health'] = health
	if not isBlank(cuisineType):
		payload['cuisineType'] = cuisineType
	if not isBlank(dishType):
		payload['dishType'] = dishType

	
	print(payload)
	return payload
	



# apid = "4cd0ab6b"
# apkey = "fa1ac224ed371e8aab696b447e424a22"

ingredientsList = input('Insert the ingredients :' )
mealType = input('Insert the mealType :' )
diet = input('Insert the diet :' )
health = input('Insert the health :' )
cuisineType = input('Insert the cuisineType :' )
dishType = input('Insert the dishType :' )

print('List of the ingredients inserted : '+ ingredientsList)
print('List of the mealType inserted : '+ mealType)
print('List of the health inserted : '+ health)
print('List of the cuisineType inserted : '+ cuisineType)
print('List of the dishTyped inserted : '+ dishType)

payload = payloadConstructor(ingredientsList,mealType,diet,health,cuisineType,dishType)

payloadTemplate = {
	'type': 'public',
	'q': ingredientsList,
	'app_id' : apid,
	'app_key' : apkey
	# 'mealType' : ' '
}

r = requests.get('https://api.edamam.com/api/recipes/v2',params = payload ,timeout=3)

print(r.url)
print(r.ok)
print(r.status_code)
try:
	if(r.ok):
		r_dict = r.json()
		r_dict_hits = r_dict['hits']


		responses_path = 'responses'
		recipe_path = 'responses/recipes'

		try:
		    shutil.rmtree(responses_path)
		except OSError as e:
		    print("Error: %s : %s" % (responses_path, e.strerror))


		try:
			os.mkdir(responses_path)
		except OSError as e:
			print("Error: %s : %s" % (responses_path, e.strerror))


		try:
			os.mkdir(recipe_path)
		except Exception as e:
			print("Error: %s : %s" % (recipe_path, e.strerror))


		print("Writing responses/response.json")
		with open('responses/response.json','w') as f:
			json.dump(r_dict,f,indent = 2)

		print("Writing responses/responseHits.json")
		with open('responses/responseHits.json','w') as f:
			json.dump(r_dict['hits'],f,indent = 2)

		with open('responses/responseRecipe1.json','w') as f:
			json.dump(r_dict_hits[0], f, indent = 2)

		i = 0
		for recipe in r_dict_hits:
			responseRecipeName = 'responses/responseRecipe'+str(i)+'.json'
			print("writing "+responseRecipeName)
			with open(responseRecipeName,'w', encoding='utf-8')as f:
				json.dump(recipe,f,indent =2 )
				i = i + 1

		i = 0
		for recipe in r_dict_hits:
			recipes = recipe['recipe']
			recipeName = recipes['label']
			recipeIngredients = recipes['ingredientLines']
			recipeURL = recipes['url']
			recipeSource = recipes['source']
			recipeImgUrl = recipes['image']
			recipeLabels = recipes['healthLabels']
			recipeDietLabels = recipes['dietLabels']
			recipeContains = recipes['cautions']
			recipeCalories = recipes['calories']
			recipeTotalWeight = recipes['totalWeight']
			recipeTotalTime = recipes['totalTime']
			recipeCuisineType = recipes['cuisineType']
			recipeMealType = recipes['mealType']
			recipesDishType = recipes['dishType']
			recipeDetailedIngredientList = recipes['ingredients']
			recipeIngredientName = 'responses/recipes/' + str(recipeName) + '.txt'
			recipeIngredientName = re.sub(':','',recipeIngredientName)

			print('writing '+recipeIngredientName)
			print('Source : ' + recipes['source'])
			with open(recipeIngredientName,'w', encoding = 'utf-8') as f:
				f.write('Recipe Name : %s\n'% str(recipeName))
				f.write('\n')
				f.write('Recipe URL : %s\n'% str(recipeURL))
				f.write('\n')
				f.write('Recipe IMG URL : %s\n'% str(recipeImgUrl))
				f.write('\n')
				f.write('Recipe is free of : %s\n'% str(recipeLabels))
				f.write('\n')
				f.write('Recipe contains : %s\n'% str(recipeContains))
				f.write('\n')
				f.write('Recipe Calories : %s\n'% str(recipeCalories))
				f.write('\n')
				f.write('Recipe Weight : %s\n'% str(recipeTotalWeight))
				f.write('\n')
				f.write('Recipe Time : %s\n'% str(recipeTotalTime))
				f.write('\n')
				f.write('Recipe Cuisine Tyoe : %s\n'% str(recipeCuisineType))
				f.write('\n')
				f.write('Recipe Diet Label : %s\n'% str(recipeDietLabels))
				f.write('\n')
				f.write('Recipe Meal Type : %s\n'% str(recipeMealType))
				f.write('\n')
				f.write('Recipe Dish Type : %s\n'% str(recipesDishType))
				f.write('\n')



				for line in recipeIngredients:
					f.write("%s\n" % line);
				f.write('\n')
				f.write('\n')
				json.dump(recipeDetailedIngredientList,f,indent=2)
				# for line in recipeDetailedIngredientList:
				# 	f.write("%s\n" % line)

				i = i + 1
		print("Number of recipes :%d\n" %i)
	else:
		print("Error : " + str(r.status_code))
except requests.exceptions.RequestException as e:
	raise SystemExit(e)
