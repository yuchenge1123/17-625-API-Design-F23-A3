import argparse
import grpc
import reddit_pb2
import reddit_pb2_grpc

def upvote_downvote_comment(stub, comment_id, is_upvote):
   response = stub.UpvoteDownvoteComment(reddit_pb2.UpvoteDownvoteRequest(id=comment_id, is_upvote=is_upvote))
   if is_upvote == True:
        if response.success and is_upvote == True:
            print(f"Upvoted comment {comment_id}, new score: {response.comment_score}")
        if not response.success and is_upvote == True:
            print(f"Failed to upvote comment {comment_id}: {response.message}")

    #downvote for comment
   if is_upvote == False:
        if response.success:
            print(f"Downvoted comment {comment_id}, new score: {response.comment_score}")
        if not response.success:
            print(f"Failed to downvote comment {comment_id}: {response.message}")

def run():
    parser = argparse.ArgumentParser(description='Reddit gRPC Client')
    parser.add_argument('--host', type=str, default='localhost', help='Server host (default: localhost)')
    parser.add_argument('--port', type=int, default=50051, help='Server port (default: 50051)')
    args = parser.parse_args()

    server_address = f'{args.host}:{args.port}'
    with grpc.insecure_channel(server_address) as channel:
        stub = reddit_pb2_grpc.RedditServiceStub(channel)
        comment_id = '33'
        is_upvote = True
        upvote_downvote_comment(stub, comment_id, is_upvote=is_upvote)
        

if __name__ == '__main__':
    run()
