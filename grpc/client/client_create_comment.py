import argparse
import grpc
import reddit_pb2
import reddit_pb2_grpc
import google.protobuf.timestamp_pb2
import datetime

def create_comment(stub, text, parent_id):
    # Create a Comment object
    comment = reddit_pb2.Comment(
        text=text, 
        score=0,  # initial score
        publication_date=google.protobuf.timestamp_pb2.Timestamp(seconds=int(datetime.datetime.now().timestamp())),
        parent_id=parent_id
    )

    # Make the gRPC call to the server
    response = stub.CreateComment(comment)

    # Handle the response
    if response.success:
        print(f"Comment created with ID: {response.modified_id},Comment Score: {response.comment_score}")
    else:
        print(f"Failed to create comment: {response.message}")

def run():
    parser = argparse.ArgumentParser(description='Reddit gRPC Client')
    parser.add_argument('--host', type=str, default='localhost', help='Server host (default: localhost)')
    parser.add_argument('--port', type=int, default=50051, help='Server port (default: 50051)')
    args = parser.parse_args()

    server_address = f'{args.host}:{args.port}'
    with grpc.insecure_channel(server_address) as channel:
        stub = reddit_pb2_grpc.RedditServiceStub(channel)

        text = "content of comment."
        parent_id = "52"  #id of the parent post or comment
        create_comment(stub, text, parent_id)

if __name__ == '__main__':
    run()
