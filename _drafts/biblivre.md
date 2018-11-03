1)Instalar java:
 apt-get install openjdk-7-jre openjdk-7-jre-headless

2)Instalar tomcat:
 apt-get install tomcat7

3) parar serviço: 
 /etc/init.d/tomcat7 stop

4)Colocar aplicação (arquivo.war) na pasta:
 var/lib/tomcat7/webapps/

4)Colocar usuário e dono do arquivo.war como tomcat7:
 chown -R tomcat7: arquivo.war

5)Se quiser sua aplicação como padrão:
 renomeie a pasta da aplicação e arquivo arquivo.war para ROOT e ROOT.war

6)Iniciar serviço: 
 /etc/init.d/tomcat7 start

*Dados do banco: META-INF/context.xml e biblivre3.xml


