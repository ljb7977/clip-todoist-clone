import json
import boto3
import base64
import uuid
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random


dynamodb = boto3.resource('dynamodb',region_name='ap-northeast-2')
user_table = dynamodb.Table('users')
# 실제로는 이렇게 안하겠지만 일단은 개발용
KEY = b'thisissuperimportantkey'

def encrypt(key, source, encode=True):
    key = SHA256.new(key).digest()  # use SHA-256 over our key to get a proper-sized AES key
    IV = Random.new().read(AES.block_size)  # generate IV
    encryptor = AES.new(key, AES.MODE_CBC, IV)
    padding = AES.block_size - len(source) % AES.block_size  # calculate needed padding
    source += (chr(padding) * padding)
    print(source, padding)
    data = IV + encryptor.encrypt(source)  # store the IV at the beginning and encrypt
    return base64.b64encode(data).decode("utf-8") if encode else data

def decrypt(key, source, decode=True):
    if decode:
        source = base64.b64decode(source.encode("utf-8"))
    key = SHA256.new(key).digest()  # use SHA-256 over our key to get a proper-sized AES key
    IV = source[:AES.block_size]  # extract the IV from the beginning
    decryptor = AES.new(key, AES.MODE_CBC, IV)
    data = decryptor.decrypt(source[AES.block_size:]) # decrypt
    padding = data[-1]
    return data[:-padding].decode()

def signup(event, context):
    try:
        new_user = event['user']
    except:
        return { "statusCide": 400, "message": "data should be capsuled in body.user"}
    
    NEED_KEYS = ['id', 'name', 'password']
    input_keys = new_user.keys()
    if not all(k in NEED_KEYS for k in input_keys):
        return { "statusCide": 400, "message": "필요 정보를 모두 입력해주세요 (id, name, password)"}
    # 중복방지
    exist_user = user_table.get_item( Key={ 'id': new_user['id']})
    if 'Item' in exist_user:
        return { "statusCide": 400, "message": "중복된 아이디가 존재합니다."}

    # encrypt
    new_user['password'] = encrypt(KEY, new_user['password'])
    # new_user['token'] = ''
    user_table.put_item(
        Item = new_user
    )
    body = {
        "message": "User Create SUCCESS",
        "input": event,
        "user": {
            'id': new_user['id'],
            'name': new_user['name'],
        }
    }
    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }
    return response

def signin(event, context):
    try:
        input_user = event['user']
    except:
        return { "statusCide": 400, "message": "data should be capsuled in body.user"}
    input_user = {
        'id': 'test1',
        'password': 'qlalfqjsgh'
    }
    NEED_KEYS = ['id', 'password']
    input_keys = input_user.keys()
    if not all(k in NEED_KEYS for k in input_keys):
        return { "statusCide": 400, "message": "아이디 또는 비밀번호를 입력하지 않으셨습니다."}
    db_user = user_table.get_item( Key={ 'id': input_user['id'] })
    if 'Item' not in db_user:
        return { "statusCide": 400, "message": "No exist Id "}

    db_user = db_user['Item']
    key = decrypt(KEY, db_user['password'])
    print(input_user['password'])
    if key != input_user['password']:
        return { "statusCide": 400, "message": "Wrong Id or Password"}
    
    response_user = user_table.update_item(
        Key={ 'id': input_user['id'] },
        UpdateExpression="set user_token = :t",
        ExpressionAttributeValues={
            ':t': str(uuid.uuid1())
        },
        ReturnValues= "ALL_NEW",
    )['Attributes']
    response_user.pop('password',None)
    response = {
        "statusCode": 200,
        "body": json.dumps(response_user)
    }
    return response
    

def get(event, context):
    user = user_table.get_item(
        Key={ 'id': 'etranger'}
    )
    response = {
        "statusCode": 200,
        "body": json.dumps(user)
    }
    print(event)
    print(response)
    return response

