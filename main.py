import time
from module.backend import *

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
    #project="Website_name"
    path=pro_path+"\\"+project
    print("Project Detail will save at "+path)
    project_foldr=sp.getstatusoutput("mkdir "+path)
    if project_foldr[0]==0:
        print("Project folder created")
    else:
        print("Project folder not created")
        print(project_foldr)
    print("Your website name is :",project)
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
        instance=create_instance(keyname=project+"_key_pair",sgname=project+"_sg",save_file=path+"\\"+project+"_detail.txt",save_file_mode="a",save=True,instance_type="t2.micro",image_id="ami-0f1fb91a596abf28d")
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

# get absolute path of current file
pro_path=os.path.dirname(os.path.abspath(__file__))
main()
