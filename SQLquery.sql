 /* Return whole table */
SELECT * FROM dbo.tweets;

 /* Return maximum likes from table */
SELECT MAX (post_likes) FROM dbo.tweets;

 /* Return tweet data for specific person */
 /* You'll notice there is duplicate data.
 This is due to GET requests retrieving the same tweets multiple times */
SELECT *
FROM dbo.tweets
WHERE user_name LIKE 'UsersName';