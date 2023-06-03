const mongoose = require('mongoose');

const UserSchema = mongoose.Schema({
  name: String,
  email: String,
  password: String,
  // Add other fields as necessary
});

module.exports = mongoose.model('User', UserSchema);
