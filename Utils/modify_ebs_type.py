import boto3

# Create an EC2 client
ec2 = boto3.client('ec2',region_name='us-west-2')

# List all volumes
volumes = ec2.describe_volumes(
    Filters=[
        {
            'Name': 'volume-type',
            'Values': [
                'gp2',
            ]
        },
    ]
)['Volumes']

# Change volume type to 'gp3' for each gp2 volume
for volume in volumes:
    volume_id = volume['VolumeId']
    availability_zone = volume['AvailabilityZone']
    iops = volume.get('Iops', None)  # Get IOPS value if present, else None

    # Determine the new volume type based on IOPS
    new_volume_type = 'gp3'

    print(f'volume_id:{volume_id}, AZ:{availability_zone}, IOPS: {iops}')

    # # Modify the volume
    try:
        response = ec2.modify_volume(
            DryRun=False,
            VolumeId=volume_id,
            VolumeType=new_volume_type
        )
        print(f"Volume {volume_id} modified to {new_volume_type}")
    except Exception as e:
        print(f"Error modifying volume {volume_id}: {e}")

print("Volume modification completed.")
