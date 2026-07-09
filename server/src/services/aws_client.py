from fastapi.concurrency import run_in_threadpool
import boto3

from src.models.bucket import BucketProvider



class AwsS3Uploader:
    def __init__(
        self,
        aws_access_id:str,
        aws_secret_key:str,
        aws_default_region:str,
        aws_bucket_name:str
    ) -> None:
        self.aws_access_id = aws_access_id
        self.aws_secret_key = aws_secret_key
        self.aws_default_region = aws_default_region
        self.aws_bucket_name = aws_bucket_name
        
        # setting up an s3 client session
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=self.aws_access_id,
            aws_secret_access_key=self.aws_secret_key,
            region_name=self.aws_default_region,
        )
        

    async def upload_files_to_bucket(self, files: list[str]) -> list[str]:
        file_urls = []

        for file in files:
            
            file_name = file.split("/")[-1] 
            
            await run_in_threadpool(
                    self.s3_client.upload_file,
                    file,
                    self.aws_bucket_name,
                    file_name
                )
            
            file_urls.append(f"https://{self.aws_bucket_name}.s3.amazonaws.com/{file_name}")
                
        return file_urls
    
    async def delete_file_from_bucket(self, file_links: list[str]) -> None:
        
        for file in file_links:
            
            file_name = file.split("/")[-1]
            
            await run_in_threadpool(
                self.s3_client.delete_object(
                Bucket=self.aws_bucket_name,    
                Key=file_name,
                )
            )
            
    @classmethod
    def client(cls, bucket: BucketProvider) -> "AwsS3Uploader":
        return cls(
            aws_access_id=bucket.credientials.ACCESS_KEY_ID,
            aws_secret_key=bucket.credientials.SECRET_ACCESS_KEY,
            aws_default_region=bucket.credientials.BUCKET_REGION,
            aws_bucket_name=bucket.credientials.BUCKET_NAME,
        )