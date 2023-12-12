import argparse
import grpc
import reddit_pb2
import reddit_pb2_grpc

def run():
    parser = argparse.ArgumentParser(description='Reddit gRPC Client')
    parser.add_argument('--host', type=str, default='localhost', help='Server host (default: localhost)')
    parser.add_argument('--port', type=int, default=50051, help='Server port (default: 50051)')
    #parse args
    args = parser.parse_args()
    #Establish a connection to the gRPC server
    server_address = f'{args.host}:{args.port}'
    with grpc.insecure_channel(server_address) as channel:
        #Create a stub (client)
        stub = reddit_pb2_grpc.RedditServiceStub(channel)
        #upvote for post
        post_id = '37'
        is_upvote = True
        if is_upvote == True:
            response = stub.UpvoteDownvotePost(reddit_pb2.UpvoteDownvoteRequest(id=post_id, is_upvote=is_upvote))
            if response.success and is_upvote == True:
                print(f"Upvoted post {post_id}, new score: {response.post_score}")
            if not response.success and is_upvote == True:
                print(f"Failed to upvote post {post_id}: {response.message}")

        #downvote for post
        if is_upvote == False:
            response = stub.UpvoteDownvotePost(reddit_pb2.UpvoteDownvoteRequest(id=post_id, is_upvote=is_upvote))
            if response.success:
                print(f"Downvoted post {post_id}, new score: {response.post_score}")
            if not response.success:
                print(f"Failed to downvote post {post_id}: {response.message}")

if __name__ == '__main__':
    run()
