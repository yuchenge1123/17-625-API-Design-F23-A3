import argparse
import grpc
import reddit_pb2
import reddit_pb2_grpc

def retrieve_comments(stub, post_id, limit):
    # Create a CommentsRequest object
    request = reddit_pb2.CommentsRequest(post_id=post_id, limit=limit)

    # Make the gRPC call to the server
    response = stub.RetrieveComments(request)

    # Handle the response
    if response.comments:
        print(f"Comments for post {post_id}:")
        for comment in response.comments:
            print(f"\tComment ID: {comment.id}, Comment Score: {comment.score}, Text: {comment.text}")
        if response.has_comment:
            print("More comments are available.")
    else:
        print(f"No comments found for post {post_id}.")

def run():
    parser = argparse.ArgumentParser(description='Reddit gRPC Client')
    parser.add_argument('--host', type=str, default='localhost', help='Server host (default: localhost)')
    parser.add_argument('--port', type=int, default=50051, help='Server port (default: 50051)')
    args = parser.parse_args()

    server_address = f'{args.host}:{args.port}'
    with grpc.insecure_channel(server_address) as channel:
        stub = reddit_pb2_grpc.RedditServiceStub(channel)

        # Example: Retrieve top 2 comments for post with ID '37'
        post_id = '37'
        limit = 2
        retrieve_comments(stub, post_id, limit)

if __name__ == '__main__':
    run()
