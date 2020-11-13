# tcp-tunnel 
基于TCP极其简单的socket穿透

代替花生壳等类似ddns服务，阿里云服务器最小买5年，100块一年。还是非常划算的。速度和服务比花生壳优秀得多

===

因为很多服务的内网没有公网ip，阿里云的服务器又太贵。所以采取阿里云作为proxy到内网机器的网络构架。目前所有服务全部采取http的方式，所以根据需求做了http穿透，用于实现类似ddns服务。

主要原理是服务端监听双端口，比如 8888端口所有tcp链接转发到8889端口。如果建立连接，通知内网机器发起连接到8889，内网机器对服务端口发起连接。从而实现穿透

``` 8888 -> 8889 <--> client:8889 -> 80```

从而实现公网8888到内网80端口的socket映射

功能简单，代码也简单


==
联系方式

mail: sqxccdy@icloud.com
github地址： [https://github.com/sqxccdy/tcp-tunnel](https://github.com/sqxccdy/tcp-tunnel)
