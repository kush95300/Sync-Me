import subprocess as sp
import os
def create_key(keyname):
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
#create_key("kush2")

def create_sg():
    print("creted Security Group")

def key_security_mode_linux(user,keyname):
    os.system("chmod 400 {1}_webserver_accesskey.pem".format(keyname))
    os.system("chown {0} {1}_webserver_accesskey.pem".format(user,keyname))
    print("Key Security Mode Set")

def key_security_mode_windows(user,keyname):
    os.system("icacls.exe {0} /reset".format(keyname+"_webserver_accesskey.pem"))
    os.system("icacls {0}_webserver_accesskey.pem /grant {1}:R".format(keyname,user))
    os.system("icacls {0}_webserver_accesskey.pem /inheritance:r".format(keyname))
    print("Key Security Mode Set")






create_sg()