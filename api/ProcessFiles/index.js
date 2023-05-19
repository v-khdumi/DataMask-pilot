const multer = require('multer');
const upload = multer({ dest: 'uploads/' });

module.exports = async function(context, req) {
  context.log('JavaScript HTTP trigger function processed a request.');

  upload.single('file')(req, res, function (err) {
    if (err) {
      context.res = { status: 500, body: err.toString() };
      return context.done();
    }

    context.res = { body: 'File uploaded successfully!'
