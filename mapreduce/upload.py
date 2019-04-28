from azure.storage.blob import BlockBlobService, PublicAccess

block_blob_service = BlockBlobService(account_name='project3twitter', 
        account_key='<YOUR_ACCOUNT_KEY>')

container_name ='project3'
block_blob_service.create_container(container_name)

block_blob_service.set_container_acl(container_name, public_access=PublicAccess.Container)
block_blob_service.create_blob_from_path(container_name, 'word-count.txt', 'word-count.txt')
