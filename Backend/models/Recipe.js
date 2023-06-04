const mongoose = require('mongoose');

const RecipeSchema = mongoose.Schema({
  title: String,
  ingredients: [String],
  instructions: String,
  calories: Number,
  allergens: [String],
  // Add other fields as necessary
});

module.exports = mongoose.model('Recipe', RecipeSchema);
