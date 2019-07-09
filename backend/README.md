# todoist backend
## Tech
> serverless, lamda, python

## Install
At First you need to install serverless
```
sudo npm install -g serverless
```

Set AWS Credential
```
serverless config credentials --provider aws --key <ACCESS KEY ID> --secret <SECRET KEY>
```
If you stored the key/secret to the credential files, we can use the different Serverless commands by designtating the profile at each command:
```
serverless deploy --aws-profile serverless
```

## Deploy
```
export AWS_PROFILE="serverless"
serverless deploy
```