import subprocess as sp

def create_key(keyname):
    print("create key")
    key=sp.getstatusoutput("aws ec2 create-key-pair --key-name {0} --query KeyMaterial --output text > {0}.pem".format(keyname))
    print(key)
#create_key("kush2")

def create_sg():
    print("creted Security Group")