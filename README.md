# ESP32_DHT11_Get_temp_humi  
ESP32连接DHT11获取温湿度数据，显示在OLED屏幕上，通过中间层将数据上传到mysql数据库并且通过网页显示出来  


## 网页展示  

![image](https://github.com/hemo528/ESP32_DHT11_Get_temp_humi/assets/40025914/19ad7f7b-0747-4181-9943-4890cf07c9cb)  


部署方式：  
## 一、ESP32部分
1、刷入micropython固件  
2、安装库文件：(使用Thonny进行开发)  
点击 工具——>管理包，搜索安装如下库  
![image](https://github.com/hemo528/ESP32_DHT11_Get_temp_humi/assets/40025914/58e34d0d-6081-4e83-bb92-f7b91aba721c)  

3、将代码保存为main.py到ESP32，这样ESP32上电以后会自动运行  
![image](https://github.com/hemo528/ESP32_DHT11_Get_temp_humi/assets/40025914/640d7aed-c7e8-42fa-8a73-800ac2aab547)  

## 二、中间层部署（使用中间层去访问数据可以增加安全性）
1、安装库文件  

```
pip install request  
pip install flask  
pip install pymysql
pip install flask_cors
pip install jsonify
pip install logging  
```
2、分别启动两个中间层（一个用来处理ESP32的请求，上传数据到数据库，另一个接受网页的请求，从数据库中读取数据，并且返回json给网页）  

运行如下  
![image](https://github.com/hemo528/ESP32_DHT11_Get_temp_humi/assets/40025914/d6e3023c-9180-48b2-bc7a-1558044c3fd9)  


![image](https://github.com/hemo528/ESP32_DHT11_Get_temp_humi/assets/40025914/b10c2cdf-0ca2-4f33-81c6-2fb255986b64)  

<font color=red>请一定一定确保两个中间层的端口不要冲突</font>  

## 三、网页的部署（以Ubuntu服务器为例）  

1、安装基础web服务  

```
sudo apt-get update
sudo apt-get install apache2  
```

2、上传网页到服务器的/var/www/html文件夹下，并且命名为index.html  

![image](https://github.com/hemo528/ESP32_DHT11_Get_temp_humi/assets/40025914/f2362433-2de1-4080-b717-bc23f768a1ab)  

## 四、数据库生成  


```
create table temp_moisture
(
    id       int auto_increment
        primary key,
    time     varchar(64) not null,
    temp     double      not null,
    moisture double      not null
);
```



