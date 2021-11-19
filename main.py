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
    #project=input("Enter your website name :")
    project="Website"
    path=pro_path+"\\"+project
    print("Project Detail will save at "+path)
    project_foldr=sp.getstatusoutput("mkdir "+path)
    if project_foldr[0]==0:
        print("Project folder created")
    else:
        print("Project folder not created")
        print(project_foldr)

    print("Your website name is :",project)
    """
    try:
        create_key(project+"_key_pair")
        os.system("move {0} {1}".format(project+"_key_pair_webserver_accesskey.pem",path))
    except:
        print("Key pair already exist")
    """
    
    sg_id=get_data_from_file(file_name=project+"_sg.txt",mode="r",file_path=path)
    if sg_id==None or sg_id=="":
        print("Sg not exist, creating SG")
        sg_id=create_sg(sgname=project+"_sg",save_file=path+"\\"+project+"_detail.txt",save_file_mode="a",save=True,description="Sg_for_"+project)
        create_file(file_name=project+"_sg.txt",file_path=path,data=sg_id,mode="w")
        create_sg_rule(sg_id,80,"tcp")
        create_sg_rule(sg_id,22,"tcp")
    print("Sg id is :",sg_id)
    """
    try:        
        instance=create_instance(keyname=project+"_key_pair",sgname=project+"_sg",save_file=project+"_detail.txt",save_file_mode="a",save=True,instance_type="t2.micro",image_id="ami-0f1fb91a596abf28d")
        print("Instance ID is :",instance)
        create_file(file_name="instance_id.txt",file_path=path,data=instance[0],mode="w")
        print("Instance is booting.Wait 10 sec")
        sleep(15)
        print("Instance is running")
    except:
        print("Instance already exist")
        id=get_data_from_file(file_name="instance_id.txt",file_path=path,mode="r")
        ip=get_instance_ip(id)
        if ip=="":
            print("Instance is not running")
        else:
            instance=(id,ip)
    url=upload_code(key_pair=project+"_key_pair_webserver_accesskey.pem",ip=instance[1],source_path=os.path.dirname(os.path.abspath(__file__))+"/Webcode/*",destination_path=project+"_code")
    create_file(file_name="url.txt",file_path=path,data=url,mode="w")
    """
    return 0

pro_path=os.path.dirname(os.path.abspath(__file__))
main()
