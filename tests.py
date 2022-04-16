from datetime import datetime, timedelta
import unittest
from app import app, db
from app.models import User, Post


class UserModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u = User(username='john')
        u.set_password('qwe')
        self.assertFalse(u.check_password('rty'))
        self.assertTrue(u.check_password('qwe'))

    def test_avatar(self):
        u = User(username='hasbulla', email='hasbulla@mail.ru')
        self.assertEqual(u.avatar(128), 'https://www.gravatar.com/avatar/'
                                        '47522cd79ea90b50fd0affabce452718?d=identicon&s=128')
        self.assertEqual(u.avatar(64), 'https://www.gravatar.com/avatar/'
                                       '47522cd79ea90b50fd0affabce452718?d=identicon&s=64')

    def test_follow(self):
        u1 = User(username='hasbik', email='hasbik1337@yandex.ru', money=100)
        u2 = User(username='ramzik', email='ramzik228@yandex.ru', money=1000)
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(u1.followed.all(), [])
        self.assertEqual(u2.followed.all(), [])

        u1.follow(u2)
        db.session.commit()
        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 1)
        self.assertEqual(u1.followed.first().username, 'ramzik')
        self.assertEqual(u2.followers.count(), 1)
        self.assertEqual(u2.followers.first().username, 'hasbik')

        u1.unfollow(u2)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 0)
        self.assertEqual(u2.followers.count(), 0)

    def test_followed_posts(self):
        # create four users
        u1 = User(username='pashok', email='pashok@example.com', money=1006)
        u2 = User(username='slavik', email='slavik@example.com', money=1003)
        u3 = User(username='iluha', email='iluha@example.com', money=1005)
        u4 = User(username='sevka', email='sevka@example.com', money=1004)
        u5 = User(username='vanek', email='vanek@example.com', money=10)
        db.session.add_all((u1, u2, u3, u4, u5))
        db.session.commit()

        # create four posts
        now = datetime.now()
        p1 = Post(title='title1 from pashok', body='body1 from pashok', author=u1,
                  created=now + timedelta(seconds=1))
        p2 = Post(title='title from slavik', body='body from slavik', author=u2,
                  created=now + timedelta(seconds=2))
        p3 = Post(title='title from iluha', body='body from iluha', author=u3,
                  created=now + timedelta(seconds=3))
        p4 = Post(title='title from sevka', body='body from sevka', author=u4,
                  created=now + timedelta(seconds=4))
        p5 = Post(title='title2 from pashok', body='body2 from pashok', author=u1,
                  created=now + timedelta(seconds=5))
        db.session.add_all((p1, p2, p3, p4, p5))
        db.session.commit()

        # setup the followers
        u1.follow(u3)   # pashok follows iluha
        u1.follow(u2)   # pashok follows slavik
        u3.follow(u1)   # iluha follows pashok
        u2.follow(u3)   # slavik follows iluha
        db.session.commit()

        # check the followed posts from each user
        f1 = u1.followed_posts().all()
        f2 = u2.followed_posts().all()
        f3 = u3.followed_posts().all()
        f4 = u4.followed_posts().all()
        f5 = u5.followed_posts().all()
        self.assertEqual(f1, [p5, p3, p2, p1])
        self.assertEqual(f2, [p3, p2])
        self.assertEqual(f3, [p5, p3, p1])
        self.assertEqual(f4, [p4])
        self.assertEqual(f5, [])


if __name__ == '__main__':
    unittest.main(verbosity=2)
