function handler(event) {
  var mobliePrefix = "m-"
  var request = event.request;
  var headers = request.headers;
  
  var host = request.headers.host.value;
  var useMoblieUrl = host.startsWith(mobliePrefix)

  var desktopDomain = useMoblieUrl ? host.slice(mobliePrefix.length) :  host
  var mobileDomain = useMoblieUrl ?  host : mobliePrefix + host

  var uri = request.uri;
  var newHost = host;
  
  console.log('Original host: ' + JSON.stringify(request));
  if (headers['cloudfront-is-mobile-viewer'] && headers['cloudfront-is-mobile-viewer'].value == "true") {
      newHost = mobileDomain;
  } else {
      newHost = desktopDomain;
  }
console.log("useMoblieUrl:"+ useMoblieUrl +  "---desktopDomain:" + desktopDomain +  "---mobileDomain:" + mobileDomain+"---newHost:"+ newHost + "---host:"+ host )

  if(newHost != host) {
      var newUrl = `https://${newHost}`;
      console.log('Request uri set to ' + newUrl);
      var response = {
          statusCode: 302,
          statusDescription: 'OK',
          headers: {
              //'host': { value: newHost },
              'location': { value: newUrl+uri }
          }
      }
      return response;
  }

  return request;
}