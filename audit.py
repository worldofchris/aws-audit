import boto.ec2
import boto.ec2.elb

excludes = ['us-gov-west-1', 'cn-north-1']

regions = boto.ec2.regions()

for region in regions:
    if region.name not in excludes:
        try:
            ec2_conn = boto.ec2.connect_to_region(region.name)
            reservations = ec2_conn.get_all_reservations()
            for reservation in reservations: 
                for instance in reservation.instances:
                    print region.name, ':',instance, ':', instance.tags

            elb_conn = boto.ec2.elb.connect_to_region(region.name)
            elbs = elb_conn.get_all_load_balancers()
            for elb in elbs:
                print region.name, ':', elb

        except boto.exception.EC2ResponseError as e:
            print e, region
