function objectToQueryString(obj) {
  var params = {};

  Object.keys(obj).sort().forEach(key => {
      params[key] = obj[key].value;
  });
  return querystring.stringify(params);
}
var querystring = require('querystring');
function handler(event) {
  var mobliePrefix = "m-"
  var request = event.request;
  var headers = request.headers;
  
  var host = headers.host.value;
  var useMoblieUrl = host.startsWith(mobliePrefix);

  var desktopDomain = useMoblieUrl ? host.slice(mobliePrefix.length) :  host;
  var mobileDomain = useMoblieUrl ?  host : mobliePrefix + host;

  var uri = request.uri;
  var newHost = host;
  
  if (headers['cloudfront-is-mobile-viewer'] && headers['cloudfront-is-mobile-viewer'].value == "true") {
    newHost = mobileDomain;
  } else {
    newHost = desktopDomain;
  }
  
  if(newHost != host) {
    var redirectUrl = "";

    if (Object.keys(request.querystring).length) {
      redirectUrl = `https://${newHost}${uri}?${objectToQueryString(request.querystring)}`;
    }
    else {
      redirectUrl = `https://${newHost}${uri}`;
    }

    var response = {
        statusCode: 302,
        statusDescription: 'Found',
        headers: {
            'location': { value: redirectUrl }
        }
    }
    return response;
  }

  return request;
}