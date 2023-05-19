const { ShareFileClient } = require('@azure/storage-file-share');

module.exports = async function(context, req) {
  const filePath = req.body.filePath;
  const connectionString = 'your-connection-string';
  const shareName = 'your-share-name';
  const fileName = 'your-file-name';

  const fileClient = new ShareFileClient(connectionString, shareName, fileName);
  await fileClient.uploadFile(filePath);

  context.res = { body: 'File uploaded to Azure Files successfully!' };
};
