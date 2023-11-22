import https from 'https'

function getRequest(ids) {
  const url = `${process.env.AUTHORS_API_URL}/authors/v1?ids=${ids}`;

  return new Promise((resolve, reject) => {
    const req = https.get(url, res => {
      let rawData = '';

      res.on('data', chunk => {
        rawData += chunk;
      });

      res.on('end', () => {
        try {          
          resolve(JSON.parse(rawData));
        } catch (err) {
          reject(new Error(err));
        }
      });
    });

    req.on('error', err => {
      reject(new Error(err));
    });
  });
}

export const handler = async (event, context) => {
  try {
    let authorIds = []
    for (let i = 0; i < event.length; i++) {
      let element = event[i];
      authorIds.push(element.source.authorId);
    }

    const result = await getRequest(authorIds);
    
    return result;
  } catch (error) {
    console.log('Error is: 👉️', error);
    return {
      statusCode: 400,
      body: error.message,
    };
  }
};