import subprocess as sp
import os

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
    None

    message:
    Security Group Created or Not Created
    """
    if(description=="None"):
        sg=sp.getstatusoutput("aws ec2 create-security-group --group-name {0} --description '{0} created for webserver' ".format(sgname))
    else:
        sg=sp.getstatusoutput("aws ec2 create-security-group --group-name {0} --description '{1}' ".format(sgname,description))
    if(sg[0]==0):
        print("Security Group Created")
        sg_id=sp.getstatusoutput("aws ec2 describe-security-groups --group-names webserver_sg_test --query 'SecurityGroups[0].GroupId' --output text")
        if(sg_id[0]==0):
            print("Security Group ID Obtained")
            file=open(save_file,save_file_mode)
            file.write("Security Group ID: "+sg_id[1]+"\n")
            file.close()
            print("Security Group ID Written to File")
        else:
            print("Security Group ID Not Obtained")
    else:
        print("Security Group Not Created")

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




