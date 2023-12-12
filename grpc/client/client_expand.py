import argparse
import grpc
import reddit_pb2
import reddit_pb2_grpc

def expand_comment_branch(stub, comment_id, comment_num):
    #create an ExpandRequest object
    request = reddit_pb2.ExpandRequest(comment_id=comment_id, comment_num=comment_num)

    #make the gRPC call to the server
    response = stub.ExpandCommentBranch(request)

    #handle the response
    if response.comments:
        print(f"Expanded comments for root comment {comment_id}:")
        for comment in response.comments:
            print(f"\tID: {comment.id}, Author: {comment.author.username}, Score: {comment.score}, Text: {comment.text}")
        if response.has_comment:
            print("More comments are available under the expanded comments.")
    else:
        print(f"No comments found for root comment {comment_id}.")

def run():
    parser = argparse.ArgumentParser(description='Reddit gRPC Client')
    parser.add_argument('--host', type=str, default='localhost', help='Server host (default: localhost)')
    parser.add_argument('--port', type=int, default=50051, help='Server port (default: 50051)')
    args = parser.parse_args()

    server_address = f'{args.host}:{args.port}'
    with grpc.insecure_channel(server_address) as channel:
        stub = reddit_pb2_grpc.RedditServiceStub(channel)

        #expand comment branch for a comment with ID '66', retrieving 1 comments
        comment_id = '66'
        comment_num = 1
        expand_comment_branch(stub, comment_id, comment_num)

if __name__ == '__main__':
    run()
