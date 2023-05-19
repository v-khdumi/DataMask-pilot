module.exports = async function(context, req) {
    // Replace this with real user data
    const users = {
      'Pharma1': 'Pass1',
      'Pharma2': 'Pass2'
    };
  
    const { username, password } = req.body;
    
    if (users[username] && users[username] === password) {
      context.res = { body: 'Login successful!' };
    } else {
      context.res = { status: 403, body: 'Invalid username or password' };
    }
  };
  