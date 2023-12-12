import argparse
import grpc
import reddit_pb2
import reddit_pb2_grpc

def retrieve_post_content(stub, post_id):
    #create a request object with the specified post ID
    request = reddit_pb2.PostRequest(id=post_id)
    response = stub.RetrievePostContent(request)

    # Check if the response contains a valid post
    if response.id == post_id:
        print(f"Post ID: {response.id}")
        print(f"Title: {response.title}")
        print(f"Content: {response.text}")
    else:
        print(f"Post with ID {post_id} not found.")

def run():
    parser = argparse.ArgumentParser(description='Reddit gRPC Client')
    parser.add_argument('--host', type=str, default='localhost', help='Server host (default: localhost)')
    parser.add_argument('--port', type=int, default=50051, help='Server port (default: 50051)')
    args = parser.parse_args()

    server_address = f'{args.host}:{args.port}'
    with grpc.insecure_channel(server_address) as channel:
        stub = reddit_pb2_grpc.RedditServiceStub(channel)
        # Example: Retrieve content of post with ID '37'
        post_id = '100'
        retrieve_post_content(stub, post_id)

if __name__ == '__main__':
    run()
