import os
import subprocess
from kubernetes import client, config
from os import path
import yaml
import logging
import time

logging.basicConfig(filename='MyscriptLog.log', filemode='w+', format='%(asctime)s- %(levelname)s - %(message)s',
                    level=logging.DEBUG)

def install_tools_in_machine():
    """
    This method will install basic tools used on the ubuntu to install another softwares
    """ 
    curl_status = os.system("curl google.com")
    if (curl_status!=0):
        logging.info("curl not present on the system installing curl ")
        os.system("echo '''Chetan@12345''' | sudo -S -v")
        installing_curl = os.system("sudo apt install curl")
        if installing_curl !=0:
            logging.critical("Installation of curl failed may be have not enternet connection")
        else:
            logging.info("Installation of curl successfull")
    else:
        logging.info("Curl already present ")
        print("Curl already installed ")
    os.system("sudo apt-get update")
    os.system("sudo apt-get -y upgrade")
    os.system("sudo apt -y install python3-pip")
    os.system("pip3 install  kubernetes")
    

def check_Oracle_virtualBox():
    """
    This method will check the existance of the Oracle Virtual Box and it's version
    """
    if os.system("vboxmanage --version") != 0:
        logging.debug("ORACLE virtual box not found and installing now")
        print("ORACLE virtual box not found and installing now")
        # Installing orcale virtual box 
        install_Oracle_virtualBox()
        logging.info("Oracel virtual Box installed successfully and version is "+str(os.system("vboxmanage --version")))
    else:
        vBox_version = subprocess.getoutput("vboxmanage --version")
        logging.info("the version of the our oracle virtual box is ",vBox_version)
        print("Virtual box already installed ")
    # if vBox_version



def install_Oracle_virtualBox():
    # I have seen another method to install particular method first download it and then install it using terminal
    # $ dpkg -i "download file name"
    # $ apt-get -f -y install 
    os.system("echo '''Chetan@12345''' | sudo -S -v")
    os.system("sudo add-apt-repository multiverse && sudo apt-get update")
    os.system("sudo apt install -y virtualbox")


def check_virtualization_support():
    """
    This method will check whether the virtualiztion is supported by the vm or not
    If not supported then abort the entire installion
    """
    virtualization_support = os.system("grep -E --color 'vmx|svm' /proc/cpuinfo")
    if virtualization_support == 0:
        print("Yes your system support virtualization we can proceed further")
    else:
        print("Your vm does not support virtualization we can't proceed further")
        exit(0)

def check_kubectl_installation():
    """
    this method will check the installation  of kubectl on the host machine
    If it is not installed then it will again install the kubectl
    """
    kubectl_version = os.system("kubectl version")
    if kubectl_version ==0:
        print("Congrates kubectl is installed................. ")
    else:
        print("installing kubectl............................. ")
        install_kubectl()


def install_kubectl():
    """
    this method will install 1.15 version of kubectl on the host machine
    """
    kubectl_status = os.system("kubectl version")
    if kubectl_status == 0:
        print("kubectl is already installed ")
        return
    else:
        print("kubectl is not installed installing it ")
        #The below command will install latest version of the kubectl 
        # os.system("curl -LO https://storage.googleapis.com/kubernetes-release/release/`curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt`/bin/linux/amd64/kubectl")
        
        os.system("echo '''Chetan@12345''' | sudo -S -v")
        # The below command will install 1.15.0 version of the kubectl 
        os.system("curl -LO https://storage.googleapis.com/kubernetes-release/release/v1.15.0/bin/linux/amd64/kubectl")

        os.system("chmod +x ./kubectl")
        os.system("sudo mv ./kubectl /usr/local/bin/kubectl")
        os.system("kubectl version")
        time.sleep(10)
        

def check_minikube_installation():
    """ 
    This method will check the installation of the minikube 
    If it is not installed then it will install the minikube again and delete the old installation
    """
    minikube_status_var = """host: Running
    kubelet: Running
    apiserver: Running
    kubeconfig: Configured"""
    minikube_status = subprocess.getoutput("minikube status")
    if minikube_status == minikube_status_var:
        # print("Minikube instalation successfull")
        # logging.info("Minikube installation successfull")
        print("Minikube already installed ")
    else:
        print("Minikube is not installed on your system installing it ....")
        install_minikube()


def install_minikube():
    """
    This method will install the minikube 
    """
    os.system("echo '''Chetan@12345''' | sudo -S -v")
    os.system("curl -Lo minikube https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64 && chmod +x minikube")
    os.system("sudo mkdir -p /usr/local/bin/")
    print("directory created ")
    status = os.system("sudo install minikube /usr/local/bin/")
    print("Installtion of binary of minikube ................... ",status)
    print("At the end of the isntall minikube function bin is used ")

def minikube_start():
    minikube_run_status = """host: Running
    kubelet: Running
    apiserver: Running
    kubeconfig: Configured"""

    minikube_stop_status = """host: Stopped
    kubelet: 
    apiserver: 
    kubeconfig:"""

    minikube_status = subprocess.getoutput("minikube status")
    if minikube_status == minikube_run_status:
        print("minikube is already runnning .........")
    elif minikube_status == minikube_stop_status:
        print("Minikube was stopped starting it .....")
        os.system("minikube start")

def create_namespaces():
    """
    This method will create three namespaces inside the minikube environment
    and check whether the namespaces already exists or not
    """
    # creating namespace for mongo db namespace name is mongo-namespace
    mongo_namespace_status = os.system("kubectl get namespace mongo-namespace")
    if mongo_namespace_status == 0:
        print("mongo-namespace already exists no need to create it")
    else:
        print("mongo-namespace does not exists creating it..... ")
        os.system("kubectl create namespace mongo-namespace")

    # creating naemspace1
    any_namespace_status = os.system("kubectl get namespace namespace1")
    if any_namespace_status == 0:
        print("namespace1 already exists no need to create it ")
    else:
        print("namespace1 does not exists creating it...... ")
        os.system("kubectl create namespace namespace1")
    
    # creating naemspace2
    any_namespace_status = os.system("kubectl get namespace namespace2")
    if any_namespace_status == 0:
        print("namespace2 already exists no need to create it ")
    else:
        print("namespace2 does not exists creating it...... ")
        os.system("kubectl create namespace namespace2")

def create_my_delploy():
    """
    This method will create deployment in namespaec1
    """
    config.load_kube_config()

    with open(path.join(path.dirname(__file__), "con1_img_deploy.yaml")) as f:   
        dep = yaml.safe_load(f)
        k8s_apps_v1 = client.AppsV1Api()
        resp = k8s_apps_v1.create_namespaced_deployment(
            body=dep, namespace="namespace1")
        print("Deployment created. status='%s'" % resp.metadata.name)


def create_my_service():
    """
    This method will create sevice in namespaec1
    """
    config.load_kube_config()

    with open(path.join(path.dirname(__file__), "service_con1.yaml")) as f:
            dep = yaml.safe_load(f)
            k8s_apps_v1 = client.CoreV1Api()
            # resp = k8s_apps_v1.create_namespaced_deployment(body=dep, namespace="default")
            resp = k8s_apps_v1.create_namespaced_service(namespace="namespace1", body=dep)
            print("Deployment created. status='%s'" % resp.metadata.name)


# os.system("kubectl create namespace mongo-namespace")
#  creating mongo namespace 

def create_mongo_delploy():
    """
    This method will create deployment for mongo db in mongo-namespace
    """
    mongo_deploy_status = os.system("kubectl get deploy mydb-deploy --namespace mongo-namespace")
    if mongo_deploy_status == 0:
        print("Deployment already exists in the mongo-namespace")
        return
    else:
        print("Deployment does not exists in mongo-namespace creating it ")

    config.load_kube_config()

    with open(path.join(path.dirname(__file__), "mydb_deploy.yaml")) as f:
        dep = yaml.safe_load(f)
        k8s_apps_v1 = client.AppsV1Api()
        resp = k8s_apps_v1.create_namespaced_deployment(
            body=dep, namespace="mongo-namespace")
        print("Deployment created. status='%s'" % resp.metadata.name)

def create_mongo_service():
    """
    This method will create service for mongo db in mongo-namespace
    """
    mongo_service_status = os.system("kubectl get service mongodbservice --namespace mongo-namespace")
    if mongo_service_status == 0:
        print("Service already exists in the mongo-namespace")
        return
    else:
        print("Deployment does not exists in mongo-namespace creating it..... ")
    config.load_kube_config()

    with open(path.join(path.dirname(__file__), "mydb_service.yaml")) as f:
            dep = yaml.safe_load(f)
            k8s_apps_v1 = client.CoreV1Api()
            # resp = k8s_apps_v1.create_namespaced_deployment(body=dep, namespace="default")
            resp = k8s_apps_v1.create_namespaced_service(namespace="mongo-namespace", body=dep)
            print("Deployment created. status='%s'" % resp.metadata.name)


def main():
    print("installling neccessary tolls on the vm in main method ")
    install_tools_in_machine()

    print("checking the virtual box in main method ")
    check_Oracle_virtualBox()

    print("Installing virtual box inside main exection ")
    install_Oracle_virtualBox()

    print("checking virtualization support in the VM executing inside the main ")
    check_virtualization_support

    print("Checking kubectl inside the VM executing inside the main method ")
    check_kubectl_installation()

    print("Checking the minikube installation executing inside the main method ")
    check_minikube_installation()

    print("Installing the minikube executing inside the main method ")
    install_minikube()
    print("installation of minikube done ")

    check_minikube_installation()

    print("creating namespaces ")
    create_namespaces()

    print("creating deployment in namespace1")
    create_my_delploy()

    print("creating service in namespace1")
    create_my_service()

    print("creating deployment in mongo-namespace ")
    create_mongo_delploy()

    print("creating service in mongo-namespace ")
    create_mongo_service()


if __name__ == '__main__':
    main()

    

    

# os.system("minikube start")
# Tasks to do in the above code 

# make a readme file and mention all the functionality of your script
# make a folder in which keep all the yaml files the name must be understabel 
# change the .yaml files name so that it must be understable