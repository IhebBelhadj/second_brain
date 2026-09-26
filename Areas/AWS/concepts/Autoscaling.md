---
type: note
created: 2026-09-26
topic:
tags: []
---
# Autoscaling

> Amazon EC2 Auto Scaling helps you ensure that you have the correct number of Amazon EC2 instances available to handle the load for your application. You create collections of EC2 instances, called _Auto Scaling groups_. You can specify the minimum number of instances in each Auto Scaling group, and Amazon EC2 Auto Scaling ensures that your group never goes below this size



You can specify the maximum number of instances in each Auto Scaling group, and Amazon EC2 Auto Scaling ensures that your group never goes above this size. If you specify the desired capacity, either when you create the group or at any time thereafter, Amazon EC2 Auto Scaling ensures that your group has this many instances. If you specify scaling policies, then Amazon EC2 Auto Scaling can launch or terminate instances as demand on your application increases or decreases.

For example, the following Auto Scaling group has a minimum size of four instances, a desired capacity of six instances, and a maximum size of twelve instances. The scaling policies that you define adjust the number of instances, within your minimum and maximum number of instances, based on the criteria that you specify

![[Pasted image 20260926092430.png]]

The following are key features of Amazon EC2 Auto Scaling:

**Monitoring the health of running instances**

Amazon EC2 Auto Scaling automatically monitors the health and availability of your instances using EC2 health checks and replaces terminated or impaired instances to maintain your desired capacity.

**Custom health checks**

In addition to the built-in health checks, you can define custom health checks that are specific to your application to verify that it's responding as expected. If an instance fails your custom health check, it's automatically replaced to maintain your desired capacity.

**Balancing capacity across Availability Zones**

You can specify multiple Availability Zones for your Auto Scaling group, and Amazon EC2 Auto Scaling balances your instances evenly across the Availability Zones as the group scales. This provides high availability and resiliency by protecting your applications from failures in a single location.

**Multiple instance types and purchase options**

Within a single Auto Scaling group, you can launch multiple instance types and purchase options (Spot and On-Demand Instances), allowing you to optimize costs through Spot Instance usage. You can also take advantage of Reserved Instance and Savings Plans discounts by using them in conjunction with On-Demand Instances in the group.

**Automated replacement of Spot Instances**

If your group includes Spot Instances, Amazon EC2 Auto Scaling can automatically request replacement Spot capacity if your Spot Instances are interrupted. Through Capacity Rebalancing, Amazon EC2 Auto Scaling can also monitor and proactively replace your Spot Instances that are at an elevated risk of interruption.

**Load balancing**

You can use Elastic Load Balancing load balancing and health checks to ensure an even distribution of application traffic to your healthy instances. Whenever instances are launched or terminated, Amazon EC2 Auto Scaling automatically registers and deregisters the instances from the load balancer.

**Scalability**

Amazon EC2 Auto Scaling also provides several ways for you to scale your Auto Scaling groups. Using auto scaling allows you to maintain application availability and reduce costs by adding capacity to handle peak loads and removing capacity when demand is lower. You can also manually adjust the size of your Auto Scaling group as needed.

**Instance refresh**

The instance refresh feature provides a mechanism to update instances in a rolling fashion when you update your AMI or launch template. You can also use a phased approach, known as a canary deployment, to test a new AMI or launch template on a small set of instances before rolling it out to the whole group.

**Lifecycle hooks**

Lifecycle hooks are useful for defining custom actions that are invoked as new instances launch or before instances are terminated. This feature is particularly useful for building event-driven architectures, but it also helps you manage instances through their lifecycle.

**Support for stateful workloads**

Lifecycle hooks also offer a mechanism for persisting state on shut down. To ensure continuity for stateful applications, you can also use scale-in protection or custom termination policies to prevent instances with long-running processes from terminating early.

## Auto scaling example

> Here is the diagram for the desired architecture 

![[Pasted image 20260924204451.png]]


**Note**: in order for the auto scale group to know how to instantiate a new EC2 instance you need to provide a launch template for that 
![[Pasted image 20260924204403.png]]

when creating the launch template there is a warning when assigning subnet for that you need to remove subnet for ec2 auto scaling

![[Pasted image 20260924204543.png]]

don't forget to enable auto assign public IP address to have a public IP for each generated instance 

![[Pasted image 20260924204914.png]]

this is the multi step form for creating an auto scaling group 

We can assign a load balancer to that auto scaling group we are creating which would show us the target group we created since the load balancer is already assigned to that target group (see the diagram above for the whole architecture as reference)
![[Pasted image 20260924205033.png]]

![[Pasted image 20260924205226.png]]
<span style="color:rgb(0, 112, 192)">What is the VPC lattice service ? </span> I don't know yet (==to be studied==)

![[Pasted image 20260924205344.png]]

for health checks make sure to turn on elastic load balancing health checks which will make this auto scale group react to health check returns of instances 

![[Pasted image 20260924205449.png]]

This is the step where we put our desired capacity 
<span style="color:rgb(255, 192, 0)">Scaling policies </span> : in this step you can set a custom scaling policy 
A **scaling policy** is the **rule that tells an Auto Scaling Group when and how to change the number of EC2 instances**

example : 

```
IF average CPU utilization > 70% THEN increase capacity
```
### Important distinction

The **scaling policy belongs to the ASG**, but the **metric usually comes from <span style="color:rgb(0, 112, 192)">CloudWatch</span>**.

```
                 CloudWatch
                     │
              observes metrics
                     │
                     ▼
              Scaling Policy
                     │
              "what should
               happen?"
                     │
                     ▼
                    ASG
                     │
              changes capacity
                     │
            ┌────────┴────────┐
            ▼                 ▼
       Launch EC2        Terminate EC2
```

![[Pasted image 20260924205626.png]]

The notification step is the step where you can push to an <span style="color:rgb(0, 112, 192)">SNS topic</span> events from the auto scale group

### Load balancers and auto scale groups

<span style="color:rgb(255, 192, 0)">Important Note :</span> lets understand the relationship between load balancers , target groups , and auto scaling groups 

```
┌───────────────────────┐
│ ALB                   │
│ "Where should traffic │
│  go?"                 │
└──────────┬────────────┘
           │
           ▼
┌───────────────────────┐
│ Target Group          │
│ "Which targets are    │
│  available?"          │
└──────────┬────────────┘
           │
           ▼
┌───────────────────────┐
│ EC2 Instances         │
│ "Run my application"  │
└──────────┬────────────┘
           │
           ▲
┌──────────┴────────────┐
│ Auto Scaling Group    │
│ "How many instances   │
│  should exist?"       │
└───────────────────────┘
```


Here is an example architecture of how all this is connected together in a real world scenario : 

```
                                  ┌──────────────────────┐
                                  │       INTERNET       │
                                  │                      │
                                  │   Users / Clients    │
                                  └──────────┬───────────┘
                                             │
                                             │ HTTP / HTTPS
                                             ▼
                         ┌────────────────────────────────────┐
                         │       ELASTIC LOAD BALANCING       │
                         │                                    │
                         │   Application Load Balancer (ALB) │
                         │                                    │
                         │   Listener :443 / :80             │
                         └────────────────┬───────────────────┘
                                          │
                                          │ Forward
                                          ▼
                         ┌────────────────────────────────────┐
                         │          TARGET GROUP              │
                         │                                    │
                         │   Protocol: HTTP                   │
                         │   Port: 8080                       │
                         │                                    │
                         │   Health Checks                    │
                         │   /health                          │
                         └───────┬──────────┬──────────┬──────┘
                                 │          │          │
                         ┌───────▼───┐ ┌────▼─────┐ ┌──▼────────┐
                         │ EC2       │ │ EC2       │ │ EC2       │
                         │ Instance  │ │ Instance  │ │ Instance  │
                         │           │ │           │ │           │
                         │ App       │ │ App       │ │ App       │
                         │ :8080     │ │ :8080     │ │ :8080     │
                         └─────▲─────┘ └────▲──────┘ └────▲──────┘
                               │             │             │
                               │             │             │
                    ┌──────────┴─────────────┴─────────────┴──────┐
                    │                                             │
                    │          AUTO SCALING GROUP (ASG)           │
                    │                                             │
                    │  Min: 2        Desired: 3       Max: 10   │
                    │                                             │
                    │  Maintains desired number of instances     │
                    └──────────────────────┬──────────────────────┘
                                           │
                                           │ Launch new instances
                                           ▼
                              ┌────────────────────────┐
                              │     LAUNCH TEMPLATE    │
                              │                        │
                              │ AMI                    │
                              │ Instance Type           │
                              │ Security Group          │
                              │ IAM Role                │
                              │ User Data               │
                              │ EBS configuration       │
                              └────────────────────────┘


        ┌────────────────────────────────────────────────────────────┐
        │                        CLOUDWATCH                          │
        │                                                            │
        │  EC2 CPU / Network / custom metrics                        │
        │  ALB RequestCount / ResponseTime / etc.                    │
        │                                                            │
        │             Scaling Policy                                 │
        │                 │                                          │
        │                 ▼                                          │
        │        "CPU > 70% → Scale Out"                            │
        │        "CPU < 30% → Scale In"                             │
        └──────────────────────┬─────────────────────────────────────┘
                               │
                               │ Scaling decision
                               ▼
                        ┌───────────────┐
                        │      ASG      │
                        │               │
                        │ +1 / -1 EC2   │
                        └───────────────┘
```

<span style="color:rgb(255, 192, 0)">One important distinction</span> : A scaling policy **doesn't create EC2 instances itself**

```
Scaling Policy
      ↓
changes desired capacity
      ↓
Auto Scaling Group
      ↓
uses Launch Template
      ↓
creates/terminates EC2 instances
      ↓
instances register/deregister
      ↓
Target Group
      ↓
ALB sends traffic to healthy instances
```

### Relationship between desired , min , max and instantiation logic

#### Core idea

An **Auto Scaling Group (ASG)** continuously tries to make the **actual number of healthy EC2 instances match the desired capacity**.

A **scaling policy** changes the desired capacity. The ASG then takes care of launching or 
terminating EC2 instances to reach that desired capacity

```
Scaling Policy
      │
      │ changes desired capacity
      ▼
     ASG
      │
      │ reconciles actual capacity
      ▼
 EC2 Instances
```

The fundamental constraint is:  <span style="color:rgb(146, 208, 80)"><b>Min ≤ Desired ≤ Max</b></span>

This means the ASG is currently trying to maintain **4 instances**, but automatic scaling can only move the desired capacity between <span style="color:rgb(146, 208, 80)"><b>Min and max</b></span>

## Links
* Docs link : [What is Amazon EC2 Auto Scaling? - Amazon EC2 Auto Scaling](https://docs.aws.amazon.com/autoscaling/ec2/userguide/what-is-amazon-ec2-auto-scaling.html)
* [AWS EC2 Auto Scaling : Step By Step Tutorial ( Part - 10) - YouTube](https://www.youtube.com/watch?v=fwfkSxb1T-s&list=PL7iMyoQPMtAN4xl6oWzafqJebfay7K8KP&index=10)