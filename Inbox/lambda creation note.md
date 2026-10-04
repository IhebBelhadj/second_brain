![[Pasted image 20261004100043.png]]
this is the form for creating a lamdba

![[Pasted image 20261004100114.png]]
here is how the lambda page looks like when you open a created lambda

![[Pasted image 20261004100212.png]]

![[Pasted image 20261004100407.png]]

policy creatoin on the iam service form 
![[Pasted image 20261004100435.png]]

![[Pasted image 20261004101523.png]]
creating a role form on IAM 

![[Pasted image 20261004101640.png]]

![[Pasted image 20261004101852.png]]

![[Pasted image 20261004101920.png]]

the created role dashboard : 
![[Pasted image 20261004102014.png]]

to assume a role you need to create a policy for sts role assumption (so for example if you want to create an access to a lambda function which external users can use you would need a policy for that lambda execution - > a role with this execution policy -> a policy for role assumption for the created role )

![[Pasted image 20261004102224.png]]

after that you create the user to consume this role (that allows you to assume role using sts)
for this user we don't want to give it access to the aws console or any other permissions we want to only give it access to this role assumption policy 

here is the user creation form : 
![[Pasted image 20261004102620.png]]

here is the user dashbaord ui  for the newly created user 
![[Pasted image 20261004102725.png]]

you can create user credentials for that user , set up mfa , set up access keys , etc ..

we are intresetd in access keys : 
![[Pasted image 20261004102841.png]]

![[Pasted image 20261004103108.png]]

let us now try to access this lambda using the newly created access key that would allow us to connect with this user that has role assumption policy which grants you access to execute the lambda function we created : 

![[Pasted image 20261004103325.png]]

![[Pasted image 20261004103455.png]]