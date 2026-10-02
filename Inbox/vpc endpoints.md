
here is the problem its trying to solve 
![[Pasted image 20261002202513.png]]

this is how we would do it with vpc endpoints , traffic does not leave aws cloud network 
but you need to set security group settings to all inbound traffic from the ec2 instance in the vpc endpoint security group settings and allow outbound traffic into the vpc endpoint from the ec2 security group perspective in order for this to work 

![[Pasted image 20261002202806.png]]

why not do it with nat if not for traffic leaving the aws network well the reason is that nat gateways are very exensive they are chargedd by the hour and unless you need to try avoid using them as much as possible

### creation process 

in order to create this setup we need to first create our security groups because creating vpc endpoint or a lambda would prompt us to have our  created security group (lets create them as placeholders though since we don't have the components created to set them in the rules )

![[Pasted image 20261002203946.png]]

the creation form of an endpoint : 
![[Pasted image 20261002204151.png]]