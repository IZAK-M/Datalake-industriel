import boto3
import pandas as pd
import hashlib
import os 
from dotenv import load_dotenv

def create_buckets(s3_client):
    buckets = ["raw", "staging", "curated", "archive"]
    for bucket in buckets:
        try:
            s3_client.create_bucket(Bucket=bucket)
            print(f"✅ Bucket '{bucket}' créé")
        except s3_client.exceptions.BucketAlreadyOwnedByYou:
            print(f"ℹ️ Bucket '{bucket}' existe déjà")


def calculate_md5(filepath):
    hash_md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


load_dotenv()

# Connexion à MinIO
s3 = boto3.client(
    "s3",
    endpoint_url="http://localhost:9000",
    aws_access_key_id = os.getenv('MINIO_ROOT_USER'),
    aws_secret_access_key= os.getenv('MINIO_ROOT_PASSWORD')
)

files = {
    "lineA": "data/raw/LineA_Stable_10K.csv",
    "lineB": "data/raw/LineB_Flux.csv",
    "lineC": "data/raw/LineC_Turbulent.csv",
    "lineD": "data/raw/LineD_SpikeControl.csv",
    "lineE": "data/raw/LineE_SmoothRun.csv",    
}
create_buckets(s3)

for line_name, filepath in files.items():
    df = pd.read_csv(filepath)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    year = df['timestamp'].dt.year.min()
    month = df['timestamp'].dt.month.min()
    
    s3_key = f"production_lines/{line_name}/year={year}/month={month:02d}/{line_name}.csv"
    
    # MD5 avant upload
    md5_before = calculate_md5(filepath)
    
    s3.upload_file(filepath, "raw", s3_key)
    
    # Vérification après upload
    response = s3.head_object(Bucket="raw", Key=s3_key)
    etag = response["ETag"].strip('"')
    
    if md5_before == etag:
        print(f"✅ {line_name} uploadé et vérifié → {s3_key}")
    else:
        print(f"❌ {line_name} corrompu !")