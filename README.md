# AWS VM Uptime Notifications
- *The implementation of an AWS lambda function that issues email notifications if a specific AWS VM instance is running and exceeds an uptime of more than 2 hours*
- *The lambda function is linked to a rule, which uses an event scheduler to run the function periodically (every 30 minutes)*
- *The lambda function was written in python*
- *Developed in June 2023*

<br>

# How to set up AWS Notifications

## Step 1: Create the lambda function
1. Navigate to the `Lambda` section in the AWS Console. Select the `Functions` tab on the left-hand side, and click on the `Create Function` button.
2. In the following window, choose a function name, Python 3.10 as the runtime environment, and x86_64 as the architecture. Leave the rest as default. <br><br>
![How to Create a Lambda Function](/Images/Lambda/CreateFunction.png)
3. Once you have created your lambda function, click on its name in the list of functions, and navigate to the `Code Source` section.
4. Copy and paste the code from `/src/lambda_function.py` into the code editor.
5. In your code, you must change the `instance_id` and `sns_topic_arn` to your VM instance's id and your SNS Topic's arn, respectively (we will create the SNS Topic in Step 3 below). We will create these as environment variables.
6. Click on the `Configuration` tab inside of the lambda function. Then, click on the `Environment variables` tab on the left-hand side.
7. Press `Edit` in the top right corner, and add two new environment variables. The first will be called `INSTANCE_ID` and the second will be called `SNS_TOPIC_ARN`. Use these names as the `key` for the environment variables.
8. The `value` for each environment variable will be the instance id of your VM and the ARN for your SNS Topic, respectively.
9. After configuring the environment variables, click the `Save` button in the bottom right corner.
10. Your code will now pull the environment variables from the AWS Console using `os.environ['key_name']`. This is used to keep confidential data hidden from your code.

## Step 2: Set up a rule that runs every 30 minutes
1. Navigate to the `CloudWatch` section in the AWS Console. Click on the `Events` drop-down menu on the left-hand side, and select `Rules`. 
2. Click on `Create Rule`. In the following window, enter a name and description for the rule, choose `default` as the event bus, and choose `Schedule` for rule type. <br><br>
![Rule Details](/Images/Rule/RuleDetails.png)
3. When you are done, click on the `Continue to create rule` button in the bottom left corner.
4. Set up the schedule pattern with the following configurations and hit `Next`. <br><br>
![Schedule Pattern](/Images/Rule/SchedulePattern.png)
5. Choose `AWS Service` as the target type, `Lambda function` as the target, and your lambda function that you created earlier as the function. Then, hit `Next`. <br><br>
![Schedule Target](/Images/Rule/ScheduleTarget.png)
6. Hit `Next` again to skip over the `Tags` section.
7. Review the rule and click on `Create rule` when ready.

## Step 3: Create an SNS (Simple Notification Service) Topic
1. Navigate to `SNS` in the AWS Console and click on `Topics` on the left-hand side.
2. Configure the topic type as `Standard`, and enter a name/description for the topic. Leave the optional settings as default and create the topic. <br><br>
![Topic Details](/Images/Topic/TopicDetails.png)
3. Once you have created your SNS Topic, click on its name in the list of topics, and press the `Create Subscription` button.
4. Select `Email` as the protocol, and enter an email address as the endpoint. <br><br>
![Topic Subscriptions](/Images/Topic/TopicSubscriptions.png)
5. Repeat steps 3 and 4 to add more email addresses to this SNS Topic.
6. After adding an email address to the SNS Topic, you will receive a confirmation email. Confirm the new subscription by clicking on the link in this email. After confirmation, navigate back to your SNS Topic, where you can confirm the status of your subscription.<br><br>
![Email Confirmation](/Images/Topic/EmailConfirmation.png)

### Everything should now be setup, and you should have functioning AWS Email Notifications!