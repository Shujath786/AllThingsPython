import boto3
import os
import logging

# AWS credentials
AWS_ACCESS_KEY_ID = ##########
AWS_SECRET_ACCESS_KEY = #######

# Local directory to backup
LOCAL_DIRECTORY = ##########

# S3 bucket name
S3_BUCKET_NAME = #########

# Initialize AWS S3 client
s3 = boto3.client('s3',
                  aws_access_key_id=AWS_ACCESS_KEY_ID,
                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def backup_data():
    try:
        for root, dirs, files in os.walk(LOCAL_DIRECTORY):
            for file in files:
                local_path = os.path.join(root, file)
                s3_key = os.path.relpath(local_path, LOCAL_DIRECTORY)
                s3.upload_file(local_path, S3_BUCKET_NAME, s3_key)
                logger.info(f"Uploaded {local_path} to S3")
    except Exception as e:
        logger.error(f"An error occurred during backup: {str(e)}")

def restore_data():
    try:
        response = s3.list_objects_v2(Bucket=S3_BUCKET_NAME)
        objects = response['Contents']
        for obj in objects:
            s3_key = obj['Key']
            local_path = os.path.join(LOCAL_DIRECTORY, s3_key)
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            s3.download_file(S3_BUCKET_NAME, s3_key, local_path)
            logger.info(f"Downloaded {s3_key} from S3")
    except Exception as e:
        logger.error(f"An error occurred during recovery: {str(e)}")

# Perform backup
backup_data()

# Perform recovery
restore_data()
