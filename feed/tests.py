# TestCase
from django.test import TestCase
from django.contrib.auth import get_user_model
from model_bakery import baker
from django.core.files.uploadedfile import SimpleUploadedFile
import os
from django.contrib.contenttypes.models import ContentType
# API TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
import json

from .models import FeedPost, FeedPost, Comment, Tags
from exercises.models import Exercise # type: ignore
from datetime import datetime, timezone
from community.models import Community # type: ignore
# Create your tests here.


class FeedPostTestCase(TestCase):
    def test_create_user_post(self):
        User = get_user_model()
        user = baker.make(User)
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        content = "Test User_Post Content"
        media = SimpleUploadedFile(
            'small.gif', small_gif, content_type='image/gif')
        user_post = FeedPost.objects.create(
            poster=user, text=content, media=media, likes=1)
        tags = baker.make(Tags, tag='Gay')
        user_post.tags.add(tags)
        lover = baker.make(User)
        user_post.likers.add(lover)

        saved_user_post = FeedPost.objects.get()
        self.assertEqual(saved_user_post.poster, user)
        self.assertEqual(saved_user_post.likes, 1)
        self.assertEqual(saved_user_post.text, content)
        self.assertEqual(saved_user_post.media.name, media.name)
        # many to many check
        for x in saved_user_post.tags.all():
            self.assertEqual(x,tags)

        # many to many checks
        for x in saved_user_post.tags.all():
            self.assertEqual(x,tags)
        for x in saved_user_post.likers.all():
            self.assertEqual(x,lover)

        # Clean up .gif file produced
        dir_path = os.getcwd()
        dir_path = os.path.join(dir_path, 'static/media')
        files = os.listdir(dir_path)
        for file in files:
            if file.endswith('.gif'):
                os.remove(os.path.join(dir_path, file))

    def test_delete_user_post(self):
        """Test that FeedPost can be deleted properly"""
        post = baker.make(FeedPost)
        FeedPost.objects.get(pk=post.id).delete()
        with self.assertRaises(FeedPost.DoesNotExist):
            FeedPost.objects.get(pk=post.id)
    
    def test_delete_poster(self):
        """To test whether post is not deleted after poster is deleted"""
        User = get_user_model()
        user = baker.make(User)
        post = baker.make(FeedPost,poster=user)
        self.assertIsInstance(post, FeedPost)
        post_id = post.id
        User.objects.get(pk=user.id).delete()
        updated_post =  FeedPost.objects.get(pk=post.id)
        self.assertEqual(updated_post.id, post_id)
        self.assertEqual(updated_post.poster, None)

    def test_update_user_post(self):
        """Test that FeedPost can be updated"""
        post = baker.make(FeedPost)
        updated_content = "New Post Content"
        post.text = updated_content
        post.save()
        updated_post = FeedPost.objects.get(pk=post.id)
        self.assertEqual(updated_post.text, updated_content)

class UserCommentTestCase(TestCase):
    User = get_user_model()

    def test_create_user_comment(self):
        User = get_user_model()
        post = baker.make(FeedPost)
        # Check that FeedPost was created
        self.assertIsInstance(post, FeedPost)
        user = User.objects.create_user(
            email='testuser@gmail.com', password='12345')
        content = "Test FeedPost Comment Content"
        ct = ContentType.objects.get_for_model(FeedPost)
        comment = post.comments.create(
            text=content, poster=user)
        self.assertEqual(comment.text, content)
        self.assertEqual(comment.poster, user)
        self.assertEqual(comment.parent_type, ct)
        self.assertEqual(comment.parent_id, post.id)

    def test_delete_commenter(self):
        """To test whether comment is not deleted after commenter is deleted"""
        User = get_user_model()
        user = baker.make(User)
        comment = baker.make(Comment, poster=user)
        self.assertIsInstance(comment, Comment)
        comment_id = comment.id
        User.objects.get(pk=user.id).delete()
        updated_comment =  Comment.objects.get(pk=comment.id)
        self.assertEqual(updated_comment.id, comment_id)
        self.assertEqual(updated_comment.poster, None)

    def test_delete_post_deletes_comment(self):
        """Test that deleting Post deletes its comments"""
        user = baker.make('users.AppUser')
        post = baker.make(FeedPost)
        
        comment = post.comments.create(poster=user, text='content')
        self.assertIsInstance(comment, Comment)
        post.delete()
        with self.assertRaises(Comment.DoesNotExist):
            Comment.objects.get(pk=comment.id)

    def test_delete_comment(self):
        """Test that we cannot retrieve comment once deleted"""
        comment = baker.make(Comment)
        Comment.objects.get(pk=comment.id).delete()
        with self.assertRaises(Comment.DoesNotExist):
            Comment.objects.get(pk=comment.id)

    def test_update_comment(self):
        """Test that comment is updated"""
        comment = baker.make(Comment)
        updated_content = "Updated FeedPostComment Content"
        comment.text = updated_content
        comment.save()
        new_comment = Comment.objects.get(pk=comment.id)
        self.assertEqual(new_comment.text, updated_content)

"""Write more test cases for Community Posts and Comments"""

class FeedPostTestCase(TestCase):
    def test_create_community_post(self):
        community = baker.make('community.Community')
        post = baker.make(FeedPost,community=community)
        self.assertIsInstance(post, FeedPost)
    
    def test_delete_community_deletes_posts(self):
        """Test that deleting Community deletes its posts"""
        community = baker.make('community.Community')
        post = baker.make(FeedPost,community=community)
        self.assertIsInstance(post, FeedPost)
        community.delete()
        with self.assertRaises(FeedPost.DoesNotExist):
            FeedPost.objects.get(pk=post.id)
    
    def test_read_community_post(self):
        post = baker.make(FeedPost)
        content = post.text 
        likes = post.likes 
        read_post = FeedPost.objects.get(pk=post.id)
        self.assertEqual(content, read_post.text)
        self.assertEqual(likes, read_post.likes)
        
    def test_update_community_post(self):
        post = baker.make(FeedPost)
        updated_content = "Updated Content"
        updated_likes = 2

        post.text = updated_content
        post.likes = updated_likes
        post.save()
        updated_post = FeedPost.objects.get(pk=post.id)
        self.assertEqual(updated_post.text, updated_content)
        self.assertEqual(updated_post.likes, updated_likes)
        
    def test_delete_community_post(self):
        post = baker.make(FeedPost)
        FeedPost.objects.get(pk=post.id).delete()
        with self.assertRaises(FeedPost.DoesNotExist):
            FeedPost.objects.get(pk=post.id)
            

class FeedPostCommentTestCase(TestCase):
    def test_create_community_post_comment(self):
        User = get_user_model()
        user = baker.make('users.AppUser')
        post = baker.make(FeedPost, poster=user)
        
        user = User.objects.create_user(
            email='testuser@gmail.com', password='12345')
        content = "Test FeedPost Comment Content"
        comment = post.comments.create(poster=user, text=content)
        ct = ContentType.objects.get_for_model(FeedPost)
        self.assertIsInstance(comment, Comment)
        self.assertEqual(comment.text, content)
        self.assertEqual(comment.poster, user)
        self.assertEqual(comment.parent_type, ct)
        self.assertEqual(comment.parent_id, post.id)


"""
API TestCase
"""
class FeedPostCreateViewTests(APITestCase):
    def test_create_user_post(self):
        """Ensure we can create user_post in FeedPost Model"""
        url = reverse('create_user_post')
        User = get_user_model()
        user = User.objects.create_user(
            email='testuser@gmail.com', password='12345')
        text = "Test FeedPost Content"
        title = "Test Title"
        data = {
            "text": text,
            "privacy_level": 1,
            "title": title
        }
        # Check that data cannot be accessed if you are not logged in
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.force_authenticate(user=user)
        # Check that user_post creates once user is autheticated
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user_post = FeedPost.objects.get()
        self.assertEqual(user_post.text, text)
        self.assertEqual(user_post.privacy_level, 1)
        # Check no text
        data = {
            "privacy_level": 1,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class FeedPostUpdateViewTests(APITestCase):
    def test_update_user_post(self):
        """Ensure we can update data in FeedPost Model"""
        url = reverse('update_feed_post')
        User = get_user_model()
        user = baker.make(User)
        user_post = baker.make(FeedPost, poster=user)
        text = "actually im gay"
        data = {
            "id": user_post.id,
            "text": text
        }
        # Check that data cannot be accessed if you are not logged in
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # check that data cannot be accessed if wrong user
        user2 = baker.make(User)
        self.client.force_authenticate(user=user2)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Check that user_post edits once user is autheticated
        self.client.force_authenticate(user=user)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(FeedPost.objects.get(pk=user_post.id).text, text)
        # Test that view will return status code 400 when id is not in data
        data = {
            "text": text
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Test that view will return status code 404 when id is wrong
        data = {
            "id": 696969,
            "text": text
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class FeedPostDetailViewTests(APITestCase):
    def test_user_post_detail(self):
        user = baker.make('users.AppUser')
        user_post = baker.make(FeedPost)
        
        comment = user_post.comments.create(poster=user, text='content')
        url = reverse('feed_post_detail', kwargs={"pk": user_post.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(data["likes"], user_post.likes)
        self.assertEqual(data["text"], user_post.text)
        self.assertEqual(data["poster"], user_post.poster)
        self.assertEqual(data["comments"][0], comment.id)
        url = reverse('feed_post_detail', kwargs={"pk": 69})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class FeedPostListViewTests(APITestCase):
    def test_user_post_list(self):
        """test the list method"""
        url = reverse('feed_post_list')
        post_no = 2
        posts = [baker.make(FeedPost) for i in range(post_no)]
        data = {
            "feed_posts": [post.id for post in posts]
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        for i, post in enumerate(posts):
            retrieved_post = data[i]
            self.assertEquals(post.id, retrieved_post["id"])
            self.assertEquals(post.text, retrieved_post["text"])
            self.assertEquals(post.poster, retrieved_post["poster"])
    
class FeedPostDeleteViewTests(APITestCase):
    def test_delete_user_post(self):
        user = baker.make('users.AppUser')
        post = baker.make(FeedPost, poster=user)
        url = reverse('delete_feed_post', kwargs={"pk": post.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response.client.force_authenticate(user=user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        with self.assertRaises(FeedPost.DoesNotExist):
            FeedPost.objects.get(pk=post.id)

class CommentCreateViewTests(APITestCase):
    def test_create_comment(self):
        """Ensure we can create comment in Comment Model"""
        url = reverse('create_comment')
        User = get_user_model()
        post = baker.make(FeedPost)
        user = User.objects.create_user(
            email='testuser@gmail.com', password='12345')
        text = "Test FeedPost Comment Content"
        ct = ContentType.objects.get_for_model(FeedPost)
        data = {
            "text": text,
            "parent_type": ct.id,
            "parent_id": post.id
        }
        # Check that data cannot be accessed if you are not logged in
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.force_authenticate(user=user)
        # Check that comment creates once user is autheticated
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        comment = Comment.objects.get()
        self.assertEqual(comment.text, text)
        self.assertEqual(comment.parent_object, post)
        # Check parent type
        data = {
            "text": text,
            "parent_type": 696969,
            "parent_id": post.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # check parent id
        data = {
            "text": text,
            "parent_type": ct.id,
            "parent_id": 696969
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class CommentUpdateViewTests(APITestCase):
    def test_update_comment(self):
        """Ensure we can update data in Comment Model"""
        url = reverse('update_comment')
        User = get_user_model()
        user = baker.make(User)
        comment = baker.make(Comment, poster=user)
        text = "actually im gay"
        data = {
            "id": comment.id,
            "text": text
        }
        # Check that data cannot be accessed if you are not logged in
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # check that data cannot be accessed if wrong user
        user2 = baker.make(User)
        self.client.force_authenticate(user=user2)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Check that comment edits once user is autheticated
        self.client.force_authenticate(user=user)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Comment.objects.get(pk=comment.id).text, text)
        # Test that view will return status code 400 when id is not in data
        data = {
            "text": text
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Test that view will return status code 404 when id is wrong
        data = {
            "id": 696969,
            "text": text
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
class CommentDetailViewTests(APITestCase):
    def test_get_comment(self):
        comment = baker.make(Comment)
        url = reverse('comment_detail', kwargs={"pk": comment.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(data["likes"], comment.likes)
        self.assertEqual(data["text"], comment.text)
        self.assertEqual(data["poster"], comment.poster)
        url = reverse('comment_detail', kwargs={"pk": 69})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class CommentListViewTests(APITestCase):
    def test_comment_list(self):
        """test the list method"""
        url = reverse('comment_list')
        post_no = 2
        posts = [baker.make(Comment) for i in range(post_no)]
        data = {
            "comments": [post.id for post in posts]
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        for i, post in enumerate(posts):
            retrieved_post = data[i]
            self.assertEquals(post.id, retrieved_post["id"])
            self.assertEquals(post.text, retrieved_post["text"])
            self.assertEquals(post.poster, retrieved_post["poster"])
    
class CommentDeleteViewTests(APITestCase):
    def test_delete_comment(self):
        user = baker.make('users.AppUser')
        post = baker.make(Comment, poster=user)
        url = reverse('delete_comment', kwargs={"pk": post.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response.client.force_authenticate(user=user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        with self.assertRaises(Comment.DoesNotExist):
            Comment.objects.get(pk=post.id)        

class CommPostCreateViewTests(APITestCase):
    def test_create_community_post(self):
        """Ensure we can create community_post in FeedPost Model"""
        url = reverse('create_community_post')
        User = get_user_model()
        community = baker.make('community.Community')
        user = User.objects.create_user(
            email='testuser@gmail.com', password='12345')
        text = "Test FeedPost Content"
        data = {
            "text": text,
            "title": "hello",
            "community_id": community.id
        }
        # Check that data cannot be accessed if you are not logged in
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.force_authenticate(user=user)
        # Check that community_post creates once user is autheticated
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        community_post = FeedPost.objects.get()
        self.assertEqual(community_post.text, text)
        # check no community
        data = {
            "text": text,
            "title": "hi",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # check community id
        data = {
            "text": text,
            "community_id": 696969,
            "title": "hi",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class UpdateShareViewTests(APITestCase):
    def test_update_share(self):
        url = reverse('update_feed_post_share')
        user = baker.make('users.AppUser')
        post = baker.make(FeedPost, poster=user)
        comment = baker.make(Comment)
        ct = ContentType.objects.get_for_model(Comment)
        data = {
            'id': post.id,
            'shared_id': comment.id,
            'shared_type': ct.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response.client.force_authenticate(user=user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_post = FeedPost.objects.get()
        self.assertEqual(updated_post.shared_object, comment)
        # test no id
        data = {
            'shared_id': comment.id,
            'shared_type': ct.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # test bad shared id
        data = {
            'id': post.id,
            'shared_id': 6969,
            'shared_type': ct.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # test bad shared type
        data = {
            'id': post.id,
            'shared_id': comment.id,
            'shared_type': 6969,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class DeleteShareViewTests(APITestCase):
    def test_delete_share(self):
        user = baker.make('users.AppUser')
        post = baker.make(FeedPost, poster=user)
        community_post = baker.make(FeedPost)
        post.shared_object = community_post
        post.save()
        url = reverse('delete_feed_post_share', kwargs={"pk": post.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response.client.force_authenticate(user=user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_post = FeedPost.objects.get(pk=post.id)
        # many to many checks
        self.assertEqual(updated_post.shared_object, None)

class DeleteLikesViewTests(APITestCase):
    def test_delete_likes(self):
        post = baker.make(Comment, likes=69)
        likes = post.likes
        user = baker.make('users.AppUser')
        post.likers.add(user)
        url = reverse('delete_comment_likes', kwargs={"pk": post.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response.client.force_authenticate(user=user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_post = Comment.objects.get()
        self.assertEqual(updated_post.likes,likes - 1)
        # many to many checks
        self.assertFalse(updated_post.likers.all().exists())
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class UpdateTagsViewTests(APITestCase):
    def test_update_tags(self):
        user = baker.make('users.AppUser')
        post = baker.make(FeedPost, poster=user)
        tag = baker.make(Tags)
        url = reverse('update_feed_post_tags')
        data = {
            'tags': [tag.tag],
            'id': post.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response.client.force_authenticate(user=user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # many to many checks
        for x in post.tags.all():
            self.assertEqual(x,tag)

class DeleteTagsViewTests(APITestCase):
    def test_delete_tags(self):
        user = baker.make('users.AppUser')
        post = baker.make(FeedPost, poster=user)
        tag = baker.make(Tags, tag="hi")
        post.tags.add(tag)
        updated_post = FeedPost.objects.get()
        url = reverse('delete_feed_post_tags', kwargs={"pk_post": post.id, "tag_name": tag.tag})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        updated_post = FeedPost.objects.get()
        response.client.force_authenticate(user=user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_post = FeedPost.objects.get()
        # many to many checks
        self.assertFalse(updated_post.tags.all().exists())
        
class LatestFeedPostViewTests(APITestCase):
    def test_get_latest_user_posts(self):
        url = reverse('latest_feed_post')
        User = get_user_model()
        user = baker.make(User)
        posts = [baker.make(FeedPost, poster=user) for i in range(21)]
        data = {
            "set_no": 0,
            "user_id": user.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content)
        # Checks that last 10 entries of posts we generated are indeed returned by comparing the posted_at times
        for i, post in enumerate(response_data):
            self.assertEqual(posts[-(i+1)].posted_at, datetime.strptime(post["posted_at"], '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=timezone.utc))
        data["set_no"] = 1
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content)
        # Checks that newest set of entries (latest 10 posts) are returned by comparing the posted_at times
        for i, post in enumerate(response_data):
            self.assertEqual(posts[-(i+11)].posted_at, datetime.strptime(post["posted_at"], '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=timezone.utc))

class LatestCommPostViewTests(APITestCase):
    def test_get_latest_community_posts(self):
        url = reverse('latest_community_post')
        community = baker.make(Community)
        posts = [baker.make(FeedPost, community=community) for i in range(21)]
        data = {
            "set_no": 0,
            "community_id": community.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content)
        # Checks that last 10 entries of posts we generated are indeed returned by comparing the posted_at times
        for i, post in enumerate(response_data):
            self.assertEqual(posts[-(i+1)].posted_at, datetime.strptime(post["posted_at"], '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=timezone.utc))
        data["set_no"] = 1
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content)
        # Checks that newest set of entries (latest 10 posts) are returned by comparing the posted_at times
        for i, post in enumerate(response_data):
            self.assertEqual(posts[-(i+11)].posted_at, datetime.strptime(post["posted_at"], '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=timezone.utc))

class UserFeedViewTests(APITestCase):
    def test_get_user_feed(self):
        url = reverse('user_feed')
        User = get_user_model()
        user = baker.make(User)
        user_friend = baker.make(User)
        post = baker.make(FeedPost, poster=user_friend)
        community = baker.make('community.Community')
        post2 = baker.make(FeedPost, poster=user_friend, community=community)
        data = {
            "set_no": 0,
            "user_id": user.id
        }
        self.client.force_authenticate(user=user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content)
        self.assertEqual(len(response_data), 0)
        user.following.add(user_friend)
        user.communities.add(community)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content)
        self.assertEqual(len(response_data), 2)
        self.assertEqual(response_data[0]["id"], post.id)
        self.assertEqual(response_data[1]["id"], post2.id)

class CommunityPostSearchViewTests(APITestCase):
    def test_search_community_posts(self):
        url = reverse('search_community_posts')
        community = baker.make(Community)
        shag_post = baker.make(FeedPost, community=community, likes=69, title="Shag Post")
        shaggy_post = baker.make(FeedPost, community=community, likes=420, title="Shaggy Shagabus Post")
        response = self.client.post(url, {})
        # Check that 400 status code is given when no data is sent
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Check that 400 status code is sent when content is missing
        response = self.client.post(url, {"community_id": community.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Check that 400 status code is sent when community_id is missing
        response = self.client.post(url, {"content": "shag"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Test that filtering for title works
        data = {
            "community_id": community.id,
            "content": "shaggy"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content)
        self.assertEqual(response_data[0]['title'], shaggy_post.title)
        self.assertEqual(response_data[0]["likes"], shaggy_post.likes)
        data["content"] = "Post"
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content)
        self.assertEqual(response_data[0]["title"], shaggy_post.title)
        self.assertEqual(response_data[0]["likes"], shaggy_post.likes)
        self.assertEqual(response_data[1]['title'], shag_post.title)
        self.assertEqual(response_data[1]['likes'], shag_post.likes)
        
class FeedPostSearchViewTests(APITestCase):
    def test_get_feed_posts(self):
        url = reverse('search_feed_posts')
        community = baker.make(Community)
        shag_post = baker.make(FeedPost, community=community, likes=69, title="Shag Post")
        shaggy_post = baker.make(FeedPost, likes=420, title="Shaggy Shagabus Post")
        response = self.client.post(url, {})
        # Check that 400 status code is given when no data is sent
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Check that 400 status code is sent when content is missing
        data = {
            "content": "shaggy"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content)
        self.assertEqual(response_data[0]['title'], shaggy_post.title)
        self.assertEqual(response_data[0]["likes"], shaggy_post.likes)
        data["content"] = "Post"
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content)
        self.assertEqual(response_data[0]["title"], shaggy_post.title)
        self.assertEqual(response_data[0]["likes"], shaggy_post.likes)
        self.assertEqual(response_data[1]['title'], shag_post.title)
        self.assertEqual(response_data[1]['likes'], shag_post.likes)