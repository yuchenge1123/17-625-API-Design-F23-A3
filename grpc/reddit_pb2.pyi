from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PostState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    POST_NORMAL: _ClassVar[PostState]
    POST_LOCKED: _ClassVar[PostState]
    POST_HIDDEN: _ClassVar[PostState]

class CommentState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    COMMENT_NORMAL: _ClassVar[CommentState]
    COMMENT_HIDDEN: _ClassVar[CommentState]

class SubredditVisibility(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PUBLIC: _ClassVar[SubredditVisibility]
    PRIVATE: _ClassVar[SubredditVisibility]
    HIDDEN: _ClassVar[SubredditVisibility]
POST_NORMAL: PostState
POST_LOCKED: PostState
POST_HIDDEN: PostState
COMMENT_NORMAL: CommentState
COMMENT_HIDDEN: CommentState
PUBLIC: SubredditVisibility
PRIVATE: SubredditVisibility
HIDDEN: SubredditVisibility

class ApiResponse(_message.Message):
    __slots__ = ("success", "message", "modified_id", "post_count", "post_score", "comment_score")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    MODIFIED_ID_FIELD_NUMBER: _ClassVar[int]
    POST_COUNT_FIELD_NUMBER: _ClassVar[int]
    POST_SCORE_FIELD_NUMBER: _ClassVar[int]
    COMMENT_SCORE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    modified_id: str
    post_count: int
    post_score: int
    comment_score: int
    def __init__(self, success: bool = ..., message: _Optional[str] = ..., modified_id: _Optional[str] = ..., post_count: _Optional[int] = ..., post_score: _Optional[int] = ..., comment_score: _Optional[int] = ...) -> None: ...

class User(_message.Message):
    __slots__ = ("id", "username")
    ID_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    id: str
    username: str
    def __init__(self, id: _Optional[str] = ..., username: _Optional[str] = ...) -> None: ...

class Post(_message.Message):
    __slots__ = ("id", "title", "text", "video_url", "image_url", "author", "score", "state", "publication_date", "subreddit_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    VIDEO_URL_FIELD_NUMBER: _ClassVar[int]
    IMAGE_URL_FIELD_NUMBER: _ClassVar[int]
    AUTHOR_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    PUBLICATION_DATE_FIELD_NUMBER: _ClassVar[int]
    SUBREDDIT_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    title: str
    text: str
    video_url: str
    image_url: str
    author: User
    score: int
    state: PostState
    publication_date: _timestamp_pb2.Timestamp
    subreddit_id: str
    def __init__(self, id: _Optional[str] = ..., title: _Optional[str] = ..., text: _Optional[str] = ..., video_url: _Optional[str] = ..., image_url: _Optional[str] = ..., author: _Optional[_Union[User, _Mapping]] = ..., score: _Optional[int] = ..., state: _Optional[_Union[PostState, str]] = ..., publication_date: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., subreddit_id: _Optional[str] = ...) -> None: ...

class Comment(_message.Message):
    __slots__ = ("id", "author", "text", "score", "state", "publication_date", "parent_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    AUTHOR_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    PUBLICATION_DATE_FIELD_NUMBER: _ClassVar[int]
    PARENT_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    author: User
    text: str
    score: int
    state: CommentState
    publication_date: _timestamp_pb2.Timestamp
    parent_id: str
    def __init__(self, id: _Optional[str] = ..., author: _Optional[_Union[User, _Mapping]] = ..., text: _Optional[str] = ..., score: _Optional[int] = ..., state: _Optional[_Union[CommentState, str]] = ..., publication_date: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., parent_id: _Optional[str] = ...) -> None: ...

class Subreddit(_message.Message):
    __slots__ = ("id", "name", "visibility", "tags")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    VISIBILITY_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    visibility: SubredditVisibility
    tags: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., visibility: _Optional[_Union[SubredditVisibility, str]] = ..., tags: _Optional[_Iterable[str]] = ...) -> None: ...

class UpvoteDownvoteRequest(_message.Message):
    __slots__ = ("id", "is_upvote")
    ID_FIELD_NUMBER: _ClassVar[int]
    IS_UPVOTE_FIELD_NUMBER: _ClassVar[int]
    id: str
    is_upvote: bool
    def __init__(self, id: _Optional[str] = ..., is_upvote: bool = ...) -> None: ...

class PostRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class CommentsRequest(_message.Message):
    __slots__ = ("post_id", "limit", "offset")
    POST_ID_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    post_id: str
    limit: int
    offset: int
    def __init__(self, post_id: _Optional[str] = ..., limit: _Optional[int] = ..., offset: _Optional[int] = ...) -> None: ...

class ExpandRequest(_message.Message):
    __slots__ = ("comment_id", "comment_num")
    COMMENT_ID_FIELD_NUMBER: _ClassVar[int]
    COMMENT_NUM_FIELD_NUMBER: _ClassVar[int]
    comment_id: str
    comment_num: int
    def __init__(self, comment_id: _Optional[str] = ..., comment_num: _Optional[int] = ...) -> None: ...

class CommentsResponse(_message.Message):
    __slots__ = ("comments", "has_comment")
    COMMENTS_FIELD_NUMBER: _ClassVar[int]
    HAS_COMMENT_FIELD_NUMBER: _ClassVar[int]
    comments: _containers.RepeatedCompositeFieldContainer[Comment]
    has_comment: bool
    def __init__(self, comments: _Optional[_Iterable[_Union[Comment, _Mapping]]] = ..., has_comment: bool = ...) -> None: ...
