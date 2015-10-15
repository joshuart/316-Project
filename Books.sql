CREATE TABLE Seller
(
	name VARCHAR(256) NOT NULL,
	email VARCHAR(256) NOT NULL UNIQUE PRIMARY KEY,
	CONSTRAINT email CHECK(email = '%@duke.edu' OR email = '%@duke.math.edu')
);

CREATE TABLE Book
(
	title VARCHAR(256) NOT NULL,
	course VARCHAR(256),
	professor VARCHAR(256),
	edition INTEGER,
	ISBN VARCHAR(256) NOT NULL,
	condition VARCHAR(256) NOT NULL,
	post_time timestamp NOT NULL,
	seller_email VARCHAR(256) NOT NULL REFERENCES Seller(email),
	price DECIMAL(10, 2) NOT NULL,
	display boolean NOT NULL,
	PRIMARY KEY(ISBN, seller_email,post_time),
	CONSTRAINT condition CHECK(condition = 'new' OR condition = 'like-new' OR condition = 'used and good' OR condition = 'used and poor')
	CONSTRAINT price CHECK(price >= 0)
);

CREATE FUNCTION no_more_than_three_days() RETURNS TRIGGER AS $$
BEGIN
  IF EXISTS( SELECT * FROM Book WHERE age(clock_timestamp, post_time) > 3 days AND display = true) THEN
    UPDATE Book
    SET display = false;
  --then send the seller an nofitication email, now I don't know how to do it
  END IF;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER no_more_than_three_days
  --BEFORE INSERT OR UPDATE ON Book
  FOR EACH STATEMENT
  EXECUTE PROCEDURE no_more_than_three_days();

-- Note: 
-- 1. some books might be copies of official edition books, so ISBN can no longer be part of a key.
-- 2. I added one more attribute "display" to book. When display = true, then that record remains visible
--    on the website. When display = false, we still have this record in the database, but people can'
--	  see it on the website. When a book has passed the three-day window period, we turn display to false.
--    when this seller wants to renew it, we turn display back to true.
-- 3. I'm not sure whether "age(clock_timestamp, post_time) > 3 days" is a valid argument or not.
-- 4. I'm not sure whether sql will fire the trigger every second (that's not a good idea). I don't know 
--    how to handle the trigger's timing part.





