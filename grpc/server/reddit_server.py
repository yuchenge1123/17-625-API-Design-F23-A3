import grpc
import argparse
import random
from concurrent import futures
import time
import reddit_pb2
import reddit_pb2_grpc

#use list to store posts and comments
posts = []
comments = []

class RedditServiceServicer(reddit_pb2_grpc.RedditServiceServicer):
    

    #the method to create posts
    #return general response and post_id
    def CreatePost(self, request, context):
        #generate a number between 1 and 100
        random_number = random.randint(1, 100)
        post = request
        #generate post_id according to post length and a random number
        post.id = str(len(posts) + random_number)  
        post.score = 0
        posts.append(post)
        return reddit_pb2.ApiResponse(success=True, message="Post created", modified_id=post.id, post_count=len(posts))

    def UpvoteDownvotePost(self, request, context):
        # Find and update post
        for post in posts:
            #post.score += 1 if request.is_upvote else -1
            if post.id == request.id:
                if request.is_upvote:
                    post.score += 1
                else:
                    post.score -= 1
                return reddit_pb2.ApiResponse(success=True, message="Post updated", modified_id=post.id, post_score=post.score)
        return reddit_pb2.ApiResponse(success=False, message="Post not found")

    def RetrievePostContent(self, request, context):
        for post in posts:
            if post.id == request.id:
                return post
        return reddit_pb2.Post()

    def CreateComment(self, request, context):
        #generate a number between 1 and 100
        random_number = random.randint(1, 100)
        comment = request
        #generate a comment_id according to comment lenth and a random number
        comment.id = str(len(comments) + random_number)
        comments.append(comment)
        return reddit_pb2.ApiResponse(success=True, message="Comment created", modified_id=comment.id)

    def UpvoteDownvoteComment(self, request, context):
        for comment in comments:
            #comment.score += 1 if request.is_upvote else -1
            if comment.id == request.id:
                if request.is_upvote:
                    comment.score += 1
                else:
                    comment.score -= 1
                return reddit_pb2.ApiResponse(success=True, message="Comment updated", modified_id=comment.id, comment_score=comment.score)
        return reddit_pb2.ApiResponse(success=False, message="Comment not found")

    def RetrieveComments(self, request, context):
        relevant_comments = []
        for comment in comments:
            if comment.parent_id == request.post_id:
                relevant_comments.append(comment)
        sorted_comments = sorted(relevant_comments, key=lambda x: x.score, reverse=True)
        return reddit_pb2.CommentsResponse(comments=sorted_comments[:request.limit])
    
    def ExpandCommentBranch(self, request, context):
        primary_comment = None
        for comment in comments:
            if comment.id == request.comment_id:
                primary_comment = comment
                break

        response_comments = []
        #return empty object if the given primary comment is not founded
        if primary_comment is None:
            return reddit_pb2.CommentsResponse()  

        #sort child comments
        child_comments = []
        for comment in comments:
            if comment.parent_id == primary_comment.id:
                child_comments.append(comment)

        sorted_child_comments = sorted(child_comments, key=lambda x: x.score, reverse=True)

        #iterate child comments
        for child_comment in sorted_child_comments[:request.comment_num]:
            response_comments.append(child_comment)
            #sort grandson comments
            grandchild_comments = []
            for comment in comments:
                if comment.parent_id == child_comment.id:
                    grandchild_comments.append(comment)

            sorted_grandchild_comments = sorted(grandchild_comments, key=lambda x: x.score, reverse=True)
            #add sorted grandson commments to response
            response_comments.extend(sorted_grandchild_comments[:request.comment_num])

        return reddit_pb2.CommentsResponse(comments=response_comments)


def serve():
    #use argparse
    parser = argparse.ArgumentParser(description='Reddit gRPC Server')
    #set default port number to 50051
    parser.add_argument('--port', type=int, default=50051, help='Port to listen on (default: 50051)')
    #parse args
    args = parser.parse_args()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    reddit_pb2_grpc.add_RedditServiceServicer_to_server(RedditServiceServicer(), server)
    #set customized port number using args
    server.add_insecure_port(f'[::]:{args.port}')
    print(f"Starting server. Listening on port {args.port}.")

    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
