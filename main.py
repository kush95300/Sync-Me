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
    print("Your website name is :",project)
    create_key(project+"_key_pair")
    sg_id=create_sg(sgname=project+"_sg",save_file=project+"_detail.txt",save_file_mode="a",save=True,description="Sg_for_"+project)
    print("Security Group ID:",sg_id)
    create_sg_rule(sg_id,80,"tcp")
    create_sg_rule(sg_id,22,"tcp")
    instance_id=create_instance(keyname=project+"_key_pair",sgname=project+"_sg",save_file=project+"_detail.txt",save_file_mode="a",save=True,instance_type="t2.micro",image_id="ami-0f1fb91a596abf28d")
    print("Instance ID is :",instance_id)
    return 0

main()