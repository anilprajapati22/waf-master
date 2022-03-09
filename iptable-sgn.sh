main(){
    choice=$1
    if [[ ! -z $2 ]]
    then
        ipadd=$2
        clientIp=$2
    fi

    if [[ 1 == $choice ]]
    then 
        if [[ -z $2 ]]
        then
            echo -e "enter Ip Address : "
            read ipadd
        fi    
        iptables --table mangle -I PREROUTING -s $ipadd -p tcp --dport 80 -j DROP
    elif [[ 2 == $choice ]]
    then 
        if [[ -z $2 ]]
        then
            echo -e "enter Ip Address : "
            read ipadd
        fi    
        iptables --table mangle -D PREROUTING -s $ipadd -p tcp --dport 80 -j DROP
    elif [[ 3 == $choice ]]
    then 
        if [[ -z $2 ]]
        then
            echo -e "enter Ip Address : "
            read ipadd
        fi    
        iptables --table mangle -I PREROUTING -s $ipadd -p tcp --dport 22 -j ACCEPT       
    elif [[ 4 == $choice ]]
    then 
        echo -e "Blocking All SSH\n"
        if [ -z $(iptables --table mangle -C PREROUTING -p tcp --dport 22 -j DROP) ]
        then
            echo -e "Adding Blocking SHH rule\n"
            iptables --table mangle -A PREROUTING -p tcp --dport 22 -j DROP     
        else
            echo -e "Rule Already Exist\n"
        fi

    elif [[ 5 == $choice ]]
    then 
        echo -e "Saving All Changes\n"
        sudo /sbin/iptables-save
    elif [[ 6 == $choice ]]
    then 
        echo -e "Reset All Rules\n"
        iptables -F
    elif [[ 7 == $choice ]]
    then 
        echo -e "Adding Client Ip : "
        firewallIp=192.168.1.66
        if [[ -z $2 ]]
        then
            echo -e "enter Client Ip Address : "
            echo -e "enter Ip Address : "
            read clientIp
        fi    
        iptables --table nat --append PREROUTING --protocol tcp --destination $firewallIp --dport 80 --jump DNAT --to-destination $clientIp
        iptables --table nat --append POSTROUTING --protocol tcp --destination $clientIp --dport 80 --jump SNAT --to-source $firewallIp

    elif [[ 8 == $choice ]]
    then 
        echo -e "Remove Client Ip : "
        
        firewallIp=192.168.1.66
        if [[ -z $2 ]]
        then
            echo -e "enter Client Ip Address : "
            echo -e "enter Ip Address : "
            read clientIp
        fi    
        iptables --table nat -D PREROUTING --protocol tcp --destination $firewallIp --dport 80 --jump DNAT --to-destination $clientIp
        iptables --table nat -D POSTROUTING --protocol tcp --destination $clientIp --dport 80 --jump SNAT --to-source $firewallIp

    fi    
}


if [[ "$USER" != "root" ]]
then 
    echo -e "you must bo root user to use this script"
else    
    if [[ ! -z $1 ]]
    then
        echo -e "command mode\n"
        main $1 $2
    else
        echo -e "CLI mode\n"
        echo -e "Enter 1 For Adding in Black List\n2 for Removing from Black List : \n"
        echo -e "3 for Adding in WhiteList for SSH"
        echo -e "4 for Block All SSH connection"
        echo -e "5 for saving All Rules"
        echo -e "6 for Reset All Rules"
        echo -e "7 for Add Customer ip"
        echo -e "8 for Remove Customer ip"
        read choice

        main $choice

    fi        
fi