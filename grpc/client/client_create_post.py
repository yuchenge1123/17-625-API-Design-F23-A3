import argparse
import grpc
import reddit_pb2_grpc
import reddit_pb2

def create_post(stub, title, content):
    #create a Post object with the given title and content
    post_request = reddit_pb2.Post(title=title, text=content)

    #call the CreatePost method on the server
    response = stub.CreatePost(post_request)

    #return the response from the server
    return response

def run():
    parser = argparse.ArgumentParser(description='Reddit gRPC Client')
    parser.add_argument('--host', type=str, default='localhost', help='Server host (default: localhost)')
    parser.add_argument('--port', type=int, default=50051, help='Server port (default: 50051)')
    #parse args
    args = parser.parse_args()
    #establish a connection to the gRPC server
    server_address = f'{args.host}:{args.port}'
    with grpc.insecure_channel(server_address) as channel:
        # Create a stub (client)
        stub = reddit_pb2_grpc.RedditServiceStub(channel)

        #create a new post
        title = "Post 5"
        text = "content of post 5."
        response = create_post(stub, title, text)
        print(f"Response from server: {response.message}, Post ID: {response.modified_id}, Total Posts: {response.post_count}")

if __name__ == '__main__':
    run()
