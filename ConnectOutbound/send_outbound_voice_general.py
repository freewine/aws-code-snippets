import boto3

client = boto3.client('connect')

# CLI: aws connect start-outbound-voice-contact --region us-west-2 --destination-phone-number +13343774004 --contact-flow-id 8039ecc7-fa2e-4b10-b03d-a67aa355994e --instance-id 0986d350-0ebf-46ed-8c88-db4b40e93690 --source-phone-number +13467668061
response = client.start_outbound_voice_contact(
    Name='outbound-voice',
    Description='demo outbound voice',
    DestinationPhoneNumber='+13343774004',
    ContactFlowId='8039ecc7-fa2e-4b10-b03d-a67aa355994e',
    InstanceId='0986d350-0ebf-46ed-8c88-db4b40e93690',
    ClientToken='freewine-demo-outbound-normal',
    QueueId='9cd1edcd-5679-4bfa-9721-6bf1dec63ac2',
    Attributes={
        'FirstName': 'Wantao'
    },
    CampaignId='01cdf0d7-a38a-4f5e-86f1-7928c8d0542b',
    TrafficType='GENERAL'
)


print(response)