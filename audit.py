import boto.ec2
import boto.ec2.elb
import boto.rds2

excludes = ['us-gov-west-1', 'cn-north-1']

regions = boto.ec2.regions()

for region in regions:
    if region.name not in excludes:
        try:
            print "Region:", region.name
            ec2_conn = boto.ec2.connect_to_region(region.name)
            reservations = ec2_conn.get_all_reservations()
            print "EC2 Instances"
            for reservation in reservations: 
                for instance in reservation.instances:
                    print region.name, ':',instance, ':', instance.tags
            print "Volumes"
            volumes = ec2_conn.get_all_volumes()
            for volume in volumes:
                print region.name, ':', volume
            elb_conn = boto.ec2.elb.connect_to_region(region.name)
            elbs = elb_conn.get_all_load_balancers()
            print "Load Balancers"
            for elb in elbs:
                print region.name, ':', elb

            rds_conn = boto.rds2.connect_to_region(region.name)
            response = rds_conn.describe_db_instances()
            rds_dbs  = response['DescribeDBInstancesResponse']['DescribeDBInstancesResult']['DBInstances']
            print "RDS Databases"
            for rds_db in rds_dbs:
                print region.name, ':', rds_db.name

        except boto.exception.EC2ResponseError as e:
            print e, region
