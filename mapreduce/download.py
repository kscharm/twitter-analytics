from azure.storage.blob import BlockBlobService, PublicAccess

block_blob_service = BlockBlobService(account_name='project3twitter',
        account_key='<YOUR_ACCOUNT_KEY>')
container_name = 'project3'
block_blob_service.set_container_acl(container_name, public_access=PublicAccess.Container)

# actual download
block_blob_service.get_blob_to_path(container_name, 'filteredTweets.txt', 'raw.txt')
