var AWS=require("aws-sdk");
var docClient=new AWS.DynamoDB.DocumentClient();

exports.handler=(event,context,callback)=> {
    console.log("event:"+JSON.stringify(event));
    
    var customerPhone=event.Details.ContactData.CustomerEndpoint.Address;

    //let nz_date_string = new Date().toLocaleString("en-US", { timeZone: "Asia/Shanghai" });
    //console.log(nz_date_string);
    
    var params={
        TableName:"AmazonConnectSurvey",
        Item:{
            "Agent": event.Details.ContactData.Attributes.Agent,
            "Timestamp": new Date().toLocaleString(),
            "SurveyScore": event.Details.ContactData.Attributes.SurveyScore,
            "CustomerPhone": event.Details.ContactData.CustomerEndpoint.Address,
            "ContactId": event.Details.ContactData.ContactId,
            "ContactFlowName": event.Details.ContactData.Queue.Name
        }
    };
            
    docClient.put(params,function(err,data){
        if(err){
            console.error("Unable to add item. Error JSON:", JSON.stringify(err, null, 2));
            context.fail(buildResponse(false));
        } else {
            console.log("Added item:", JSON.stringify(data, null, 2));
            callback(null,buildResponse(true));
        }
    });
};

function buildResponse(isSuccess){
    if(isSuccess){
        return {
            Result:"Success"
        };
    }
    else {
        console.log("Lambda returned error to Connect");
        return{Result:"Error"};
    }
}
