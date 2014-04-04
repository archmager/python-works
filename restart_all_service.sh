#!/bin/bash


#common command
TOMCAT_RESTART=/home/q/tools/bin/restart_tomcat.sh

#check dubbo service whether service exported
dubbocheck(){
  echo "====check dubbo: $1 service===="
  for i in {1..20} ;do
    resultTxt=$(echo ls | nc -i 1 127.0.0.1 $1)
    if [ "$resultTxt" != "" ];then
      echo "====Start $2 Dubbo Service Succeed!!===="
      break
    fi
    sleep 1
  done
  if [ "$resultTxt" = "" ];then
    echo "====dubbo: $2 Dubbo service failures===="
    exit 1
  fi
}

#check tts java service whether starts succeed
httpcheck(){
  echo "====check http status===="
  for i in {1..20} ;do
    status=`curl -o /dev/null -s -w %{http_code} "http://127.0.0.1:$1" `
    if [ $status -eq 200 ];then
      echo "====start http succeed===="
      break
    fi
    sleep 1
  done
  if [ $status -ne 200 ];then
      echo "====start http failure==="
      exit 1
  fi
}



#restart public
echo "==1==restart public service===="
sudo $TOMCAT_RESTART public
dubbocheck 20885 public

#restart voucher
echo "==2==restart voucher service===="
sudo $TOMCAT_RESTART voucher
dubbocheck 20992 voucher

#restart invoice
echo "==3==restart invoice service===="
sudo $TOMCAT_RESTART invoice
dubbocheck 20890 invoice

#restart policy
echo "==4==restart policy service===="
sudo $TOMCAT_RESTART policy
dubbocheck 20886 policy

#restart b2b
echo "==5==restart b2b service===="
sudo $TOMCAT_RESTART b2b
dubbocheck 20891 b2b

#restart pay
echo "==6==restart pay service===="
sudo $TOMCAT_RESTART pay
dubbocheck 20887 pay

#restart ticket
echo "==7==restart ticket service===="
sudo $TOMCAT_RESTART ticket
dubbocheck 20888 ticket

#restart ttsinsurance
echo "==8==restart ttsinsurance service===="
sudo $TOMCAT_RESTART ttsinsurance
dubbocheck 20987 ttsinsurance

#restart ttssearch
echo "==9==restart ttssearch service===="
sudo $TOMCAT_RESTART ttssearch
httpcheck "8085/healthcheck.html"
dubbocheck 20889 ttssearch


#restart ttsroundtripsearch
echo "==10==restart ttsroundtripsearch service===="
sudo $TOMCAT_RESTART ttsroundtripsearch
dubbocheck 20789 ttsroundtripsearch


#restart tts_core
echo "==11==restart tts java===="
sudo $TOMCAT_RESTART ttstw
dubbocheck 13839 ttstw
httpcheck "8080/config/healthcheck.jsp"
