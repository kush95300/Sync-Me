import subprocess as sp
import os
from time import sleep

# All Functions are mentioned below

#function to create key pair
def create_key(keyname,profile):
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
    key=sp.getstatusoutput("aws ec2 create-key-pair --profile {1} --key-name {0}  --query KeyMaterial --output text > {0}_webserver_accesskey.pem".format(keyname,profile))
    if(key[0]==0):
        print("Key Created")
        if os.name == 'nt':
            key_security_mode_windows(os.getlogin(),keyname)
        else:
            key_security_mode_linux(os.getlogin(),keyname)
        print("Key Security Mode Set")
        return True
    else:
        print("Key Not Created")
        return False

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
def create_sg(sgname,profile,description="None",save_file="sg.txt",save_file_mode="a",save=True):
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
    # creating security group
    if(description=="None"):
        sg=sp.getstatusoutput("aws ec2 create-security-group --group-name {0} --description {0} --profile {1}".format(sgname,profile))
    else:
        sg=sp.getstatusoutput("aws ec2 create-security-group --group-name {0} --description {1} --profile {2} ".format(sgname,description,profile))
    if(sg[0]==0):
        # Security Group Created
        print("Security Group Created")
        sg_id=sp.getstatusoutput("aws ec2 describe-security-groups --group-names {0} --profile {1} --query SecurityGroups[0].GroupId --output text".format(sgname,profile))
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
def create_sg_rule(sgname,profile,port,protocol,type="ingress",cidr="0.0.0.0/0",source_sg=None):
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
        sg_rule=sp.getstatusoutput("aws ec2 authorize-security-group-ingress --profile {4} --group-id {0} --protocol {1} --port {2} --cidr {3}".format(sgname,protocol,port,cidr,profile))
    else:
        sg_rule=sp.getstatusoutput("aws ec2 authorize-security-group-ingress --profile {4} --group-id {0} --protocol {1} --port {2} --source-group {3}".format(sgname,protocol,port,source_sg,profile))
    if(sg_rule[0]==0):
        print("Security Group Rule Created")
    else:
        print("Security Group Rule Not Created")
        print("Error Code:",sg_rule)


#function to create instance
def create_instance(profile,keyname,sgname=None,instance_type="t2.micro",image_id="ami-0f1fb91a596abf28d",security_group_ids=None,save_file="instance.txt",save_file_mode="a",save=True):
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
    (Instance Id, Instance IP) or None

    Message:
    Instance Created or Not Created

    """
    if( sgname==None):
        instance=sp.getstatusoutput("aws ec2 run-instances  --image-id {0} --count 1 --instance-type {1} --key-name {2} --security-group-ids {3} --query Instances[].InstanceId  --output text  --profile {4}".format(image_id,instance_type,keyname,security_group_ids,profile))
    else:
        instance=sp.getstatusoutput("aws ec2 run-instances  --image-id {0} --count 1 --instance-type {1} --key-name {2} --security-groups {3}   --query Instances[].InstanceId --output text --profile {4}".format(image_id,instance_type,keyname,sgname,profile))
    if (instance[0]==0):
        instance_id=instance[1]
        print("Instance Created. Starting in 30 sec")
        sleep(25)
        instance_ip=sp.getstatusoutput("aws ec2 describe-instances  --instance-ids {0} --profile {1} --query  Reservations[0].Instances[0].PublicIpAddress --output text".format(instance_id,profile))
        if(instance_ip[0]==0):
            print("Instance ID Obtained")
            file=open(save_file,save_file_mode)
            file.write("Instance ID: "+instance_id+"\n")
            file.write("Instance IP: "+instance_ip[1]+"\n")
            file.close()
            print("Instance ID Written to File")
            return (instance_id,instance_ip[1])
        else:
            print("Instance ID Not Obtained")
            print("Error Code:",instance_ip)
            return None
    else:    
        print("Instance Not Created")
        print("Error Code:",instance)
        return None

# upload code to instance
def upload_code(key_pair,ip,user_name="ec2-user",source_path="webcode/*",destination_path="/home/ec2-user/webcode"):
    """
    Description:
    Upload code to instance

    Input:
    instance_id: instance id
    file_name: file name
    file_path: file path
    save_file: file name to save instance id
    save_file_mode: file mode to save instance id
    save: True or False

    Output:
    None

    Message:
    Code Uploaded or Not Uploaded

    """
    
    dest_dir=sp.getstatusoutput("ssh -o StrictHostKeyChecking=no -i {}  {}@{} mkdir -p {} ".format(key_pair,user_name,ip,destination_path))  
    if(dest_dir[0]==0):
        print("Destination Directory Created")
    else:
        print("Destination Directory Not Created")
        print("Error Code:",dest_dir)
        return None
    print("Uploading Code to Instance. This might take few minutes based on your internet speed.")    
    code=sp.getstatusoutput("scp -o StrictHostKeyChecking=no -i {} -rp {} {}@{}:{}".format(key_pair,source_path,user_name,ip,destination_path))
    if(code[0]==0):
        print("Code Uploaded")
    else:
        print("Code Not Uploaded")
        print("Error Code:",code)
        return None
    webserver=sp.getstatusoutput("ssh -o StrictHostKeyChecking=no -i {} {}@{} sudo yum install httpd php -y ".format(key_pair,user_name,ip))
    if(webserver[0]==0):
        print("Web Server Installed")   
    else:
        print("Web Server Not Installed")
        print("Error Code:",webserver)
        return None

    configure_webserver=sp.getstatusoutput("ssh -o StrictHostKeyChecking=no -i {} {}@{} /usr/bin/sudo mv /home/ec2-user/{}/* /var/www/html/".format(key_pair,user_name,ip,destination_path))
    if (configure_webserver[0]==0):
        print("Web Server Configured")
    else:
        print("Web Server Not Configured")
        print("Error Code:",configure_webserver)
        return None
    start_webserver=sp.getstatusoutput("ssh -o StrictHostKeyChecking=no -i {} {}@{}   /usr/bin/sudo systemctl start httpd".format(key_pair,user_name,ip))
    if (start_webserver[0]==0):
        print("Web Server Started")
    else:
        print("Web Server Not Started")
        print("Error Code:",start_webserver)
        return None
    if not(code[0] and dest_dir[0] and webserver[0] and configure_webserver[0] and start_webserver[0]):
        print("Code Uploaded")
        return "http://{}".format(ip)
    else:
        print("Code Not Uploaded")
        return None

# To create a local file
def create_file(file_name,data,file_path,mode="w"):
    """
    Description:
    Create a local file

    Input:
    data: data to be written in file
    file_name: file name
    file_path: file path
    file_mode: file mode

    Output:
    None

    Message:
    File Created or Not Created

    """
    # try:
    #     file=open(file_path+"/"+file_name,mode)
    #     file.write(data)
    #     file.close()
    #     print("File Created")
    # except:
    #     print("File Not Created")

    file=open(file_path+"/"+file_name,mode)
    file.write(data)
    file.close()
    
# getter function

# To get data from local file
def get_data_from_file(file_name,file_path=os.path.dirname(os.path.abspath(__file__)),mode="r"):
    """
    Description:
    Get data from local file

    Input:
    file_name: file name
    file_path: file path

    Output:
    data: data from file

    Message:
    Data Obtained or Not Obtained

    """
    try:
        file=open(file_path+"/"+file_name,mode)
        data=file.read()
        file.close()
        print("Data Obtained")
        return data
    except:
        print("Data Not Obtained")
        return None

# get instance ip 
def get_instance_ip(id,profile):
    """
    Description:
    Get instance ip

    Input:
    id: instance id

    Output:
    ip: instance ip

    Message:
    IP Obtained or Not Obtained

    """
    try:
        ip=sp.getstatusoutput("aws ec2 describe-instances  --instance-ids {0} --query  Reservations[0].Instances[0].PublicIpAddress --output text --profile {1}".format(id,profile))
        if(ip[0]==0):
            print("IP Obtained")
            return ip[1]
        else:
            print("IP Not Obtained")
            print("Error Code:",ip)
            return None
    except:
        print("IP Not Obtained")
        return None

# get instance dns name
def get_instance_dns_name(id,profile):
    """
    Description:
    Get instance dns name

    Input:
    id: instance id

    Output:
    dns_name: instance dns name

    Message:
    DNS Name Obtained or Not Obtained

    """
    try:
        dns_name=sp.getstatusoutput("aws ec2 describe-instances  --instance-ids {0} --query  Reservations[0].Instances[0].PublicDnsName --output text --profile {1}".format(id,profile))
        if(dns_name[0]==0):
            print("DNS Name Obtained")
            return "http://"+dns_name[1]
        else:
            print("DNS Name Not Obtained")
            print("Error Code:",dns_name)
            return None
    except:
        print("DNS Name Not Obtained")
        return None

# Functions

# create new Website function
def create_website(path,website_name,aws_access_key_id,aws_secret_access_key,aws_region="ap-south-1",i_type="t2.micro"):
    """
    Description:
    Create new website

    Input:
    website_name : name of website
    path : path of project folder (where detail file will be saved)

    Output:
    None

    Message:
    None

    """
    project = website_name
    # Create Key Pair
    try:
        key=create_key(project+"_key_pair",profile=website_name)
        if key:
            # Key Pair Created
            os.system("move {0} {1}".format(project+"_key_pair_webserver_accesskey.pem",path))
            create_file(file_path=path, file_name="output_data.txt",data="==> Key Created Successfully. [5% done] \n==> Key Mode Changed. [10% done]\n==> Key Saved Locally [15% done]\n",mode="a")
        else:
            # Key Pair Not Created
            os.system("del {0}".format(project+"_key_pair_webserver_accesskey.pem"))
            create_file(file_path=path, file_name="output_data.txt",data="Key Not created. Something Went wrong [ Failed ]\n",mode="a")
            return False
    except:
        # Key Pair already exists
        print("Key pair already exist")
        create_file(file_path=path, file_name="output_data.txt",data="==> Key Already Exists [15% done]\n",mode="a")

    # Check if Security Group Exists
    print("SG already exist or not")
    create_file(file_path=path, file_name="output_data.txt",data="\nChecking  Security Group Exists or not\n",mode="a")
    
    # Get Security Group Id
    sg_id=get_data_from_file(file_name=project+"_sg.txt",mode="r",file_path=path)
    if sg_id==None or sg_id=="":
        # Security Group Not Exists
        print("Sg not exist, creating SG")
        create_file(file_path=path, file_name="output_data.txt",data="\n==> Security Group Not Exists. Creating Security Group\n",mode="a")
        
        # Creating Security Group
        sg_id=create_sg(profile=website_name,sgname=project+"_sg",save_file=path+"/detail.txt",save_file_mode="a",save=True,description="Sg_for_"+project)
        if sg_id == None:
            # Security Group Not Created
            create_file(file_path=path, file_name="output_data.txt",data="xxxx SG Not created. Something Went wrong [Failed]\n",mode="a")
            return False
        create_file(file_name=project+"_sg.txt",file_path=path,data=sg_id,mode="w")

        # Security Group rules Created
        create_sg_rule(sgname= sg_id,port= 80,protocol="tcp",profile=website_name)
        create_sg_rule(sgname= sg_id,protocol= "tcp",port= 22,profile=website_name)
        create_file(file_path=path, file_name="output_data.txt",data="==> Security Group and its Rules added successfully. [30 % done]\n",mode="a")
        
    else:
        # Security Group Exists
        print("Sg already exist. Getting id")
        print("Sg id is :",sg_id)
        create_file(file_path=path, file_name="output_data.txt",data="==> Security Group already Exists. [30 % done]\n",mode="a")
        
    # Check instance already exists or not
    print("Checking Instance already exists or not")
    create_file(file_path=path, file_name="output_data.txt",data="\nChecking Instance already exists or not\n",mode="a")
    
    id=get_data_from_file(file_name="instance_id.txt",file_path=path,mode="r")
    if id==None or id=="":
        print("Instance not exist, creating Instance")
        print("Fetching Latest AMI ID")
        create_file(file_path=path, file_name="output_data.txt",data="==> Instance not exist, creating Instance\n==> Fetching Latest AMI ID\n",mode="a")
        ami_id=sp.getstatusoutput("aws ssm get-parameters --names /aws/service/ami-amazon-linux-latest/amzn2-ami-hvm-x86_64-gp2 --region {0} --profile {1}  --query Parameters[0].Value --output text".format(aws_region,website_name))
        if ami_id[0]==0:
            print("AMI ID is :",ami_id[1])
            print("AMI ID obtained")
            
        else:
            print("AMI ID not obtained. Using Default AMI")
            print(aws_region)
            if(aws_region == "ap-south-1"):
                ami_id=(0,'ami-0f1fb91a596abf28d')
            elif aws_region == "us-west-1":
                ami_id=(0,'ami-04ad2567c9e3d7893')
            else:
                print("Default AMI not found")
                create_file(file_path=path, file_name="output_data.txt",data="==> AMI ID Not obtained. We can't create resource in given region. [Failed]\n",mode="a")
                return False
        create_file(file_path=path, file_name="output_data.txt",data="==> AMI ID obtained. AMI ID is {}. [40% done]\n".format(ami_id[1]),mode="a")
        print("AMI ID is :",ami_id) 
        instance=create_instance(profile=website_name,keyname=project+"_key_pair",image_id=ami_id[1],sgname=project+"_sg",save_file=path+"/detail.txt",save_file_mode="a",save=True,instance_type=i_type)
        if instance == None:
            # Instance Not Created
            create_file(file_path=path, file_name="output_data.txt",data="==> Instance Not Created. [Failed]\n",mode="a")
            return False
        create_file(file_name="instance_id.txt",file_path=path,data=instance[0],mode="w")
        create_file(file_path=path, file_name="output_data.txt",data="==> Instance Created. Instance Id is {} [50% done]\n==> Instance booting up, it might take few seconds.\n".format(instance[0]),mode="a")
        print("Instance is booting.Please Wait few sec")
        off=True
        while off==True:
            instance_status=sp.getstatusoutput("ssh -o StrictHostKeyChecking=no -i {} ec2-user@{} hostname".format(path+"/"+project+"_key_pair_webserver_accesskey.pem",instance[1]))
            if instance_status[0]==0:
                print("Instance is up and running")
                create_file(file_path=path, file_name="output_data.txt",data="==> Instance Successfully booted up. [60% done]\n",mode="a")
                off=False
            else:
                print("Instance is not up. Rechecking in 5 sec")
                create_file(file_path=path, file_name="output_data.txt",data="==> Instance is not up. Rechecking in 5 seconds. \n",mode="a")
                import time
                time.sleep(5)
                print(instance_status)
        print("Instance is up and running")
        print("Instance ID is :",instance[0])
    else:
        print("Instance already exist")
        create_file(file_path=path, file_name="output_data.txt",data="==> Instance already exist. [50% done]\n",mode="a")
        print("Instance ID is :",id)
        print("Checking Instance start or not")
        create_file(file_path=path, file_name="output_data.txt",data="\nChecking Instance start or not\n",mode="a")
        ip=get_instance_ip(id,profile=website_name)
        if ip=="":
            print("Instance is not running")
            create_file(file_path=path, file_name="output_data.txt",data="==> Instance is not running. [Failed]\n",mode="a")
            return False
        else:
            print("Instance is running")
            create_file(file_path=path, file_name="output_data.txt",data="==> Instance is running. [60% done]\n",mode="a")
            instance=(id,ip)  

    # Hosting website 
    # 
    # Check website already exists or not   
    print("checking website already hosted or not")
    create_file(file_path=path, file_name="output_data.txt",data="\nChecking website already hosted or not\n",mode="a")
    get_url=get_data_from_file(file_name=project+"_url.txt",file_path=path,mode="r")
    
    if get_url==None or get_url=="":
        print("Website not hosted. Creating webserver")
        create_file(file_path=path, file_name="output_data.txt",data="==> Website not hosted. Creating webserver\n",mode="a")
        create_file(file_path=path, file_name="output_data.txt",data="==> Creating dependecies and installing Webserver. [70% done]\n",mode="a")
        create_file(file_path=path, file_name="output_data.txt",data="==> Uploading webcode, it might take few minutes based on your internet speed. [70% done]\n",mode="a")
        url=upload_code(key_pair=path+"/"+project+"_key_pair_webserver_accesskey.pem",ip=instance[1],source_path=path+"/Code/*",destination_path=project+"_code")
        create_file(file_path=path, file_name="output_data.txt",data="==> Webserver created Successfully. [90% done]\n",mode="a")
        create_file(file_name=project+"_url.txt",file_path=path,data=url,mode="w")
        dns_url=get_instance_dns_name(instance[0],profile=website_name)
        create_file(file_name=project+"_dns_url.txt",file_path=path,data=dns_url,mode="w")
        create_file(file_name="detail.txt",file_path=path,data="Website DNS Url :"+dns_url+"\n",mode="a")
        create_file(file_name="detail.txt",file_path=path,data="Website IP Url :"+url+"\n",mode="a")
    else:
        print("Website already hosted")
        create_file(file_path=path, file_name="output_data.txt",data="==> Website already hosted. [90% done]\n",mode="a")
        url=get_url
    create_file(file_path=path, file_name="output_data.txt",data="\n Obtaining website url and DNS links. [95% done]\n",mode="a")
    print("Your website url is :",url)
    print("Your website dns url is :",get_data_from_file(file_name=project+"_dns_url.txt",file_path=path,mode="r"))
    create_file(file_path=path, file_name="output_data.txt",data="==> Website url and DNS links obtained. [100% done]\n",mode="a")
    create_file(file_path=path, file_name="output_data.txt",data="\n=====> Website URL : {0}\n=====> Website DNS: {1}\n".format(url,dns_url),mode="a")
    create_file(file_path=path, file_name="output_data.txt",data="\n\n\n For more info: Go to Detail page.\n\nThanks for using our product. Project: {} Successfully hosted over AWS.".format(website_name),mode="a")
    return True

 

# delete project function
def delete_project():
    """
    Description:
    Delete project

    Input:
    None

    Output:
    None

    Message:
    None

    """
    project=input("Enter your project name :")
    #project="project_name"
    print("Your project name is :",project)
    input_data=input("Are you sure you want to delete this project (y/n) :")
    if input_data=="y":
        path=pro_path+"/"+project
        print("Deleting Project at "+path)
        #delete_website(website_name=project,path=path)
        os.system("rmdir /s /Q "+path)
        print("Project deleted successfully")
        return 0
    else:
        print("Project not deleted")
        return 1

# get absolute path of current file
pro_path=os.path.abspath(os.path.dirname(__file__))
#create_project()
#delete_project()

# Test AWS 
def test_aws():
    """
    Description:
    Test AWS

    Input:
    None

    Output:
    None

    Message:
    None

    """
    aws = sp.getstatusoutput("aws --version")
    print(aws)
    if aws[0]!=0:
        print("AWS not installed")
        return  False
    else:
        print("AWS installed")
        return True

# Set AWS Credentials
def set_aws_credentials(profile,aws_access_key_id,aws_secret_access_key,aws_region):
    aws_set_accesskey=sp.getstatusoutput("aws configure set aws_access_key_id {} --profile={}".format(aws_access_key_id,profile))
    aws_set_secretkey=sp.getstatusoutput("aws configure set aws_secret_access_key {} --profile={}".format(aws_secret_access_key,profile))
    aws_set_region=sp.getstatusoutput("aws configure set region {} --profile={}".format(aws_region,profile))
    if aws_set_accesskey[0]==0 and aws_set_secretkey[0]==0 and aws_set_region[0]==0:  
        return True
    else:
        return False

# Get AWS Credentials
def get_aws_credentials(profile_name):
    aws_access_key_id=sp.getstatusoutput("aws configure get aws_access_key_id --profile={}".format(profile_name))
    aws_secret_access_key=sp.getstatusoutput("aws configure get aws_secret_access_key --profile={}".format(profile_name))
    aws_region=sp.getstatusoutput("aws configure get region --profile={}".format(profile_name))
    if aws_access_key_id[0]==0 and aws_secret_access_key[0]==0 and aws_region[0]==0:
        return aws_access_key_id[1],aws_secret_access_key[1],aws_region[1]
    else:
        return "","",""

# Set AWS Credentials Empty
def set_aws_credentials_empty(profile_name):
    aws_set_accesskey=sp.getstatusoutput("aws configure set aws_access_key_id '' --profile={}".format(profile_name))
    aws_set_secretkey=sp.getstatusoutput("aws configure set aws_secret_access_key '' --profile={}".format(profile_name))
    aws_set_region=sp.getstatusoutput("aws configure set region '' --profile={}".format(profile_name))
    if aws_set_accesskey[0]==0 and aws_set_secretkey[0]==0 and aws_set_region[0]==0:  
        return True
    else:
        return False

# Test AWS credentials
def test_aws_credentials(profile,aws_access_key_id,aws_secret_access_key,aws_region):
    """
    Description:
    Test AWS credentials

    Input:
    None

    Output:
    None

    Message:
    None

    """
    # Set Credentials temporarily
    set =set_aws_credentials(profile=profile,aws_access_key_id=aws_access_key_id,aws_secret_access_key=aws_secret_access_key,aws_region=aws_region)
    if set==True:
        print("AWS Credentials set successfully")
    else:
        print("AWS Credentials not set")
        
    # Test Credentials
    aws_credentials = sp.getstatusoutput("aws ec2 describe-vpcs --profile={}".format(profile))
    if aws_credentials[0]!=0:
        print("Error in AWS credentials")
        status =set_aws_credentials_empty(profile_name=profile)
        if status==True:
            print("AWS credentials set to empty")
        else:
            print("AWS credentials not set to empty")
        return False
    else:
        print("AWS credentials working")
        print(aws_credentials)
        return True