import subprocess as sp
import os
from time import sleep

# All Functions are mentioned below

#function to create key pair
def create_key(keyname):
    """
    Description:
    Create key pair

    Input:
    keyname: key name

    Output:
    None

    Message:
    Key Pair Created or Not Created
    """
    key=sp.getstatusoutput("aws ec2 create-key-pair --key-name {0} --query KeyMaterial --output text > {0}_webserver_accesskey.pem".format(keyname))
    if(key[0]==0):
        print("Key Created")
        if os.name == 'nt':
            key_security_mode_windows(os.getlogin(),keyname)
        else:
            key_security_mode_linux(os.getlogin(),keyname)
        print("Key Security Mode Set")
             
    else:
        print("Key Not Created")

#function to create key pair file mode for linux
def key_security_mode_linux(user,keyname):
    """
    Description:
    Create key pair file mode for linux (chmod 400)

    Input:
    user: user name
    keyname: key name

    Output:
    None

    Message:
    Key Security Mode Set or Not Set
    """
    os.system("chmod 400 {1}_webserver_accesskey.pem".format(keyname))
    os.system("chown {0} {1}_webserver_accesskey.pem".format(user,keyname))
    print("Key Security Mode Set")

#function to create key pair file mode for windows    
def key_security_mode_windows(user,keyname):
    """
    Description:
    Create key pair file mode for windows (chmod 400)

    Input:
    user: user name
    keyname: key name

    Output:
    None
      
    Message:
    Key Security Mode Set or Not Set
    """                                                                                                       
    os.system("icacls.exe {0} /reset".format(keyname+"_webserver_accesskey.pem"))
    os.system("icacls {0}_webserver_accesskey.pem /grant {1}:R".format(keyname,user))
    os.system("icacls {0}_webserver_accesskey.pem /inheritance:r".format(keyname))
    print("Key Security Mode Set")

#function to create security group
def create_sg(sgname,description="None",save_file="sg.txt",save_file_mode="a",save=True):
    """
    Description:
    Create Security Group and save security group id in a file

    Input:
    sgname: security group name
    description: description of security group
    save_file: file name to save security group id
    save_file_mode: file mode to save security group id
    save: True or False

    output:
    Security Group Id or None

    message:
    Security Group Created or Not Created
    """
    if(description=="None"):
        sg=sp.getstatusoutput("aws ec2 create-security-group --group-name {0} --description {0} ".format(sgname))
    else:
        sg=sp.getstatusoutput("aws ec2 create-security-group --group-name {0} --description {1} ".format(sgname,description))
    if(sg[0]==0):
        print("Security Group Created")
        sg_id=sp.getstatusoutput("aws ec2 describe-security-groups --group-names {} --query SecurityGroups[0].GroupId --output text".format(sgname))
        if(sg_id[0]==0):
            print("Security Group ID Obtained")
            file=open(save_file,save_file_mode)
            file.write("Security Group ID: "+sg_id[1]+"\n")
            file.close()
            print("Security Group ID Written to File")
            return sg_id[1]
        else:
            print("Security Group ID Not Obtained")
            return None
    else:
        print("Security Group Not Created")
        print("Error Code:",sg)
        return None

#function to create security group rule
def create_sg_rule(sgname,port,protocol,type="ingress",cidr="0.0.0.0/0",source_sg=None):
    """
    Input:

    sgname: security group name
    port: port number
    protocol: tcp, udp, icmp, all, ...
    type: ingress or egress
    cidr: default is 0.0.0.0/0
    source_sg: security group name or id

    Output:
    None

    Message:
    Security Group Rule Created or Not Created

    Example:
    1. Rule for all port 80
        create_sg_rule("webserver_sg_test",80,"tcp")

    2. Rule for all port ssh
        create_sg_rule("webserver_sg_test",22,"tcp","ingress")

    3. Rule for ssh port 22 from specific cidr
        create_sg_rule("webserver_sg_test",22,"tcp","ingress","192.14.23.33/32")

    4. Rule for all port 80 specific security group
    create_sg_rule("webserver_sg_test",80,"tcp","ingress","192.14.23.33/32","webserver_sg_test")
    
    """
    if(source_sg==None):
        sg_rule=sp.getstatusoutput("aws ec2 authorize-security-group-ingress --group-id {0} --protocol {1} --port {2} --cidr {3}".format(sgname,protocol,port,cidr))
    else:
        sg_rule=sp.getstatusoutput("aws ec2 authorize-security-group-ingress --group-id {0} --protocol {1} --port {2} --source-group {3}".format(sgname,protocol,port,source_sg))
    if(sg_rule[0]==0):
        print("Security Group Rule Created")
    else:
        print("Security Group Rule Not Created")
        print("Error Code:",sg_rule)


#function to create instance
def create_instance(keyname,sgname=None,instance_type="t2.micro",image_id="ami-0f1fb91a596abf28d",security_group_ids=None,save_file="instance.txt",save_file_mode="a",save=True):
    """
    Description:
    Create Instance and save instance id in a file

    Input:
    keyname: key name
    sgname: security group name
    instance_type: t2.micro, t2.small, t2.medium, t2.large, t2.xlarge, t2.2xlarge, m3.medium, m3.large, m3.xlarge, m3.2xlarge, m4.large, m4.xlarge, m4.2xlarge, m4.4xlarge, m4.10xlarge
    image_id: AMI ID (default ami-0f1fb91a596abf28d)
    security_group_ids: security group id 1, security group id 2
    instance_name: instance name
    save_file: file name to save instance id
    save_file_mode: file mode to save instance id
    save: True or False

    Output:
    Instance Id or None

    Message:
    Instance Created or Not Created

    """
    if( sgname==None):
        instance=sp.getstatusoutput("aws ec2 run-instances --image-id {0} --count 1 --instance-type {1} --key-name {2} --security-group-ids {3} --query Instances[].InstanceId  --output text".format(image_id,instance_type,keyname,security_group_ids))
    else:
        instance=sp.getstatusoutput("aws ec2 run-instances --image-id {0} --count 1 --instance-type {1} --key-name {2} --security-groups {3}   --query Instances[].InstanceId --output text".format(image_id,instance_type,keyname,sgname))
    if (instance[0]==0):
        instance_id=instance[1]
        print("Instance Created. Starting in 30 sec")
        sleep(10)
        print(instance_id)
        instance_ip=sp.getstatusoutput("aws ec2 describe-instances  --instance-ids {} --query  Reservations[0].Instances[0].PublicIpAddress --output text".format(instance_id))
        if(instance_ip[0]==0):
            print("Instance ID Obtained")
            file=open(save_file,save_file_mode)
            file.write("Instance ID: "+instance_id+"\n")
            file.write("Instance IP: "+instance_ip[1]+"\n")
            file.close()
            print("Instance ID Written to File")
            return instance_id
        else:
            print("Instance ID Not Obtained")
            print("Error Code:",instance_ip)
            return None
    else:    
        print("Instance Not Created")
        print("Error Code:",instance)
        return None


# myfunc()

def main():
    """
    Description:
    Main function

    Input:
    None

    Output:
    None

    Message:
    None

    """
    project=input("Enter your website name :")
    #print("Your website name is :",project)
    #create_key(project+"_key_pair")
    #sg_id=create_sg(sgname=project+"_sg",save_file=project+"_detail.txt",save_file_mode="a",save=True,description="Sg_for_"+project)
    #print("Security Group ID:",sg_id)
    #create_sg_rule(sg_id,80,"tcp")
    #create_sg_rule(sg_id,22,"tcp")
    instance_id=create_instance(keyname=project+"_key_pair",sgname=project+"_sg",save_file=project+"_detail.txt",save_file_mode="a",save=True,instance_type="t2.micro",image_id="ami-0f1fb91a596abf28d")
    print("Instance ID is :",instance_id)

main()