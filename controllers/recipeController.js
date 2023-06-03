const Recipe = require('../models/Recipe');
const axios = require('axios');

exports.generateRecipe = async (req, res) => {
  const { ingredients, mealType, numberOfPeople } = req.body;

  // Call OpenAI GPT-3.5 API for recipe generation
  const openAIResponse = await axios.post('https://api.openai.com/v1/engines/davinci-codex/completions', {
    prompt: `Generate a ${mealType} recipe for ${numberOfPeople} people using the following ingredients: ${ingredients.join(', ')}`,
    max_tokens: 500,
  }, {
    headers: {
      'Authorization': `Bearer ${process.env.OPENAI_API_KEY}`
    }
  });

  // Call Azure OpenAI for recipe generation
  const azureResponse = await axios.post('https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/{appId}?verbose=true&timezoneOffset=0&subscription-key={subscriptionKey}&q={q}', {
    prompt: `Generate a ${mealType} recipe for ${numberOfPeople} people using the following ingredients: ${ingredients.join(', ')}`,
    max_tokens: 500,
  }, {
    headers: {
      'Ocp-Apim-Subscription-Key': `${process.env.AZURE_OPENAI_API_KEY}`
    }
  });

  // Save the recipe to the database
  const recipe = new Recipe({
    title: openAIResponse.data.choices[0].text,
    ingredients: ingredients,
    instructions: azureResponse.data.choices[0].text,
    // Add other fields as necessary
  });

  try {
    const savedRecipe = await recipe.save();
    res.json(savedRecipe);
  } catch (err) {
    res.json({ message: err });
  }
};
