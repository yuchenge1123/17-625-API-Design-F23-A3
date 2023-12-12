import argparse
import grpc
import unittest
from unittest.mock import patch, MagicMock, Mock
import reddit_pb2
import reddit_pb2_grpc
import io

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

def run_expand_comment_branch():
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

def retrieve_post_content(stub, post_id):
    #create a request object with the specified post ID
    request = reddit_pb2.PostRequest(id=post_id)
    response = stub.RetrievePostContent(request)

    #check if the response contains a valid post
    if response.id == post_id:
        print(f"Post ID: {response.id}")
        print(f"Title: {response.title}")
        print(f"Content: {response.text}")
    else:
        print(f"Post with ID {post_id} not found.")

def run_retrieve_post_content():
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

def run_retrieve_comments():
    parser = argparse.ArgumentParser(description='Reddit gRPC Client')
    parser.add_argument('--host', type=str, default='localhost', help='Server host (default: localhost)')
    parser.add_argument('--port', type=int, default=50051, help='Server port (default: 50051)')
    args = parser.parse_args()

    server_address = f'{args.host}:{args.port}'
    with grpc.insecure_channel(server_address) as channel:
        stub = reddit_pb2_grpc.RedditServiceStub(channel)

        # Example: Retrieve top 5 comments for post with ID '37'
        post_id = '66'
        limit = 1
        retrieve_comments(stub, post_id, limit)


class TestReddit(unittest.TestCase):

    #retrieve most upvoted comments under the post
    @patch('reddit_pb2_grpc.RedditServiceStub')
    #positive test for retrieve most upvoted comment
    #where there is a most upvoted comment
    def test_retrieve_comments_positive(self, mock_stub):
        # Set up mock response
        mock_response = reddit_pb2.CommentsResponse()
        comment = mock_response.comments.add()
        comment.id = "66"
        comment.score = 10
        comment.text = "Mock comment"
        mock_response.has_comment = True

        #set up the mock to return the mock response
        mock_stub_instance = mock_stub.return_value
        mock_stub_instance.RetrieveComments.return_value = mock_response

        #to retrieve the most upvoted, so the limit is 1
        with patch('sys.stdout', new_callable=io.StringIO) as fake_output:
            retrieve_comments(mock_stub_instance, "37", 1)
            output = fake_output.getvalue()

        #assert that the stub method was called with the correct parameters
        mock_stub_instance.RetrieveComments.assert_called_once_with(
            reddit_pb2.CommentsRequest(post_id="37", limit=1))

        # assert that the output contains the correct comment ID
        self.assertIn("Comment ID: 66", output)


    @patch('reddit_pb2_grpc.RedditServiceStub')
    #negative test for retrieve most upvoted comment
    #where there are no comments under the post
    def test_retrieve_comments_no_comments(self, mock_stub):
        #prepare the mock response for no comments
        mock_response = reddit_pb2.CommentsResponse()
        mock_response.has_comment = False
        #configure the mock stub
        mock_stub_instance = mock_stub.return_value
        mock_stub_instance.RetrieveComments.return_value = mock_response
        with patch('sys.stdout', new=io.StringIO()) as fake_output:
            retrieve_comments(mock_stub_instance, "66", 1)
            output = fake_output.getvalue()

        #assertion
        self.assertIn("No comments found for post 66", output)

    #positive test for retrieve post
    #check the output
    @patch('reddit_pb2_grpc.RedditServiceStub')
    def test_retrieve_post_content_positive(self, mock_stub):
        # Prepare the mock response for a valid post
        mock_response = reddit_pb2.Post()
        mock_response.id = "100"
        mock_response.title = "mock post title"
        mock_response.text = "mock post content"

        # Configure the mock stub
        mock_stub_instance = mock_stub.return_value
        mock_stub_instance.RetrievePostContent.return_value = mock_response

        # Capture the output
        with patch('sys.stdout', new=io.StringIO()) as fake_output:
            retrieve_post_content(mock_stub_instance, "100")
            output = fake_output.getvalue()

        # Assertions
        self.assertIn("Post ID: 100", output)
        self.assertIn("Title: mock post title", output)
        self.assertIn("Content: mock post content", output)

    #negative test for retrieve post
    #where there are no post found
    @patch('reddit_pb2_grpc.RedditServiceStub')
    def test_retrieve_post_content_negative(self, mock_stub):
        # Prepare the mock response for post not found
        mock_response = reddit_pb2.Post()
        mock_response.id = ""

        # Configure the mock stub
        mock_stub_instance = mock_stub.return_value
        mock_stub_instance.RetrievePostContent.return_value = mock_response

        # Capture the output
        with patch('sys.stdout', new=io.StringIO()) as fake_output:
            retrieve_post_content(mock_stub_instance, "101")
            output = fake_output.getvalue()

        # Assertions
        self.assertIn("Post with ID 101 not found", output)

    #positive test for expand comment
    #most upvoted so limit == 1
    #check the output
    @patch('reddit_pb2_grpc.RedditServiceStub')
    def test_expand_positive(self, mock_stub):
        #mock response with comments
        mock_response = reddit_pb2.CommentsResponse()
        comment = mock_response.comments.add()
        comment.id = "101"
        comment.score = 5
        comment.text = "mock comment"
        mock_response.has_comment = True

        #mock stub
        mock_stub_instance = mock_stub.return_value
        mock_stub_instance.ExpandCommentBranch.return_value = mock_response
        with patch('sys.stdout', new=io.StringIO()) as fake_output:
            expand_comment_branch(mock_stub_instance, "66", 1)
            output = fake_output.getvalue()

        #assertions
        self.assertIn("Expanded comments for root comment 66", output)
        self.assertIn("ID: 101", output)
        self.assertIn("Score: 5", output)
        self.assertIn("mock comment", output)
        self.assertTrue("More comments are available under the expanded comments." in output)


    #negative test for expand comment
    #most upvoted so limit == 1
    #no comments under root comment
    @patch('reddit_pb2_grpc.RedditServiceStub')
    def test_expand_comment_branch_no_comments(self, mock_stub):
        #mock response for no comments
        mock_response = reddit_pb2.CommentsResponse()
        mock_response.has_comment = False
        #mock stub
        mock_stub_instance = mock_stub.return_value
        mock_stub_instance.ExpandCommentBranch.return_value = mock_response
        with patch('sys.stdout', new=io.StringIO()) as fake_output:
            expand_comment_branch(mock_stub_instance, "66", 1)
            output = fake_output.getvalue()

        #assertions
        self.assertIn("No comments found for root comment 66", output)

    

if __name__ == '__main__':
    unittest.main()
