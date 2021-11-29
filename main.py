import time
from module.backend import *
from module.frontend import *

# Functions

# create new Website function
def create_website(path,website_name=None,aws_region="ap-south-1",i_type="t2.micro"):
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
    if aws_region == "" or aws_region == None:
        aws_region = "ap-south-1"
    try:
        key=create_key(project+"_key_pair")
        if key:
            os.system("move {0} {1}".format(project+"_key_pair_webserver_accesskey.pem",path))
        else:
            os.system("del {0}".format(project+"_key_pair_webserver_accesskey.pem"))
    except:
        print("Key pair already exist")
    print("SG already exist or not")
    sg_id=get_data_from_file(file_name=project+"_sg.txt",mode="r",file_path=path)
    if sg_id==None or sg_id=="":
        print("Sg not exist, creating SG")
        sg_id=create_sg(sgname=project+"_sg",save_file=path+"\\"+project+"_detail.txt",save_file_mode="a",save=True,description="Sg_for_"+project)
        if sg_id == None:
            return ValueError
        create_file(file_name=project+"_sg.txt",file_path=path,data=sg_id,mode="w")
        create_sg_rule(sg_id,80,"tcp")
        create_sg_rule(sg_id,22,"tcp")
    else:
        print("Sg already exist. Getting id")
        print("Sg id is :",sg_id)
    print("Checking Instance already exists or not")
    id=get_data_from_file(file_name="instance_id.txt",file_path=path,mode="r")
    if id==None or id=="":
        print("Instance not exist, creating Instance")
        print("Fetching Latest AMI ID")
        ami_id=sp.getstatusoutput("aws ssm get-parameters --names /aws/service/ami-amazon-linux-latest/amzn2-ami-hvm-x86_64-gp2 --region {}  --query Parameters[0].Value --output text".format(aws_region))
        if ami_id[0]==0:
            print("AMI ID is :",ami_id[1])
            print("AMI ID obtained")
            
        else:
            print("AMI ID not obtained. Using Default AMI")
            if(aws_region == "ap-south-1"):
                ami_id="ami-0f1fb91a596abf28d"
            else:
                ami_id="ami-04ad2567c9e3d7893"
            
        instance=create_instance(keyname=project+"_key_pair",image_id=ami_id[1],sgname=project+"_sg",save_file=path+"\\"+project+"_detail.txt",save_file_mode="a",save=True,instance_type=i_type)
        create_file(file_name="instance_id.txt",file_path=path,data=instance[0],mode="w")
        print("Instance is booting.Please Wait few sec")
        off=True
        while off==True:
            instance_status=sp.getstatusoutput("ssh -o StrictHostKeyChecking=no -i {} ec2-user@{} hostname".format(path+"\\"+project+"_key_pair_webserver_accesskey.pem",instance[1]))
            if instance_status[0]==0:
                print("Instance is up and running")
                off=False
            else:
                print("Instance is not up. Rechecking in 5 sec")
                time.sleep(5)
                print(instance_status)
        print("Instance is up and running")
        print("Instance ID is :",instance[0])
    else:
        print("Instance already exist")
        print("Instance ID is :",id)
        print("Checking Instance start or not")
        ip=get_instance_ip(id)
        if ip=="":
            print("Instance is not running")
        else:
            print("Instance is running")
            instance=(id,ip)      
    print("checking website already hosted or not")
    get_url=get_data_from_file(file_name=project+"_url.txt",file_path=path,mode="r")
    if get_url==None or get_url=="":
        print("Website not hosted. Creating webserver")
        url=upload_code(key_pair=path+"\\"+project+"_key_pair_webserver_accesskey.pem",ip=instance[1],source_path=os.path.dirname(os.path.abspath(__file__))+"/Webcode/*",destination_path=project+"_code")
        create_file(file_name=project+"_url.txt",file_path=path,data=url,mode="w")
        dns_url=get_instance_dns_name(instance[0])
        create_file(file_name=project+"_dns_url.txt",file_path=path,data=dns_url,mode="w")
        create_file(file_name=project+"_detail.txt",file_path=path,data="Website DNS Url :"+dns_url+"\n",mode="a")
        create_file(file_name=project+"_detail.txt",file_path=path,data="Website IP Url :"+url+"\n",mode="a")
    else:
        print("Website already hosted")
        url=get_url
    print("Your website url is :",url)
    print("Your website dns url is :",get_data_from_file(file_name=project+"_dns_url.txt",file_path=path,mode="r"))

    return 0

# create new project function
def create_project():
    """
    Description:
    Create new project

    Input:
    None

    Output:
    None

    Message:
    None

    """
    project=input("Enter your project name :")
    #project="project_name"
    path=pro_path+"\\"+project
    print("Project Detail will save at "+path)
    project_foldr=sp.getstatusoutput("mkdir "+path)
    if project_foldr[0]==0:
        print("Project folder created")
    else:
        print("Project folder not created")
        print(project_foldr)
    print("Your project name is :",project)
    #aws_region=input("Enter your AWS region :")
    #aws_access_key_id=input("Enter your AWS access key id :")
    #aws_secret_access_key=input("Enter your AWS secret access key :")
    #i_type=input("Enter your instance type :")

    try:
        print("Creating Website")
        create_website(website_name=project,path=path)
        #create_project(project,path,aws_region,aws_access_key_id,aws_secret_access_key,i_type)
        print("Website created successfully")
        return 0
    except:
        print("Error in creating website")
        return 1
    

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
        path=pro_path+"\\"+project
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


app = myAPP()
app.title("Sync Me")
app.mainloop()

