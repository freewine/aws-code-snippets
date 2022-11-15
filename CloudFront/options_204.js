function handler(event) {
  var request = event.request;
  var headers = request.headers;
  var response = event.response ? event.response : {};
  if (request.method.toUpperCase() === 'OPTIONS') {
     Object.assign(response, {
      statusCode: 204,
      statusDescription: 'Found',
      headers: {
        'access-control-allow-origin': { value: '*' },
        'access-control-allow-methods': {value: '*'},
        'access-control-allow-headers': {value: '*'},
        'access-control-allow-credentials': { value: 'true' }
      }
    });
    return response;
  }
 return request;
}