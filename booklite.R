library(RSQLite)
library(dplyr)
library(magrittr)

Bookdata <- as.data.frame(read.table("test.txt",sep = ",",stringsAsFactors = FALSE),stringsAsFactor = FALSE)
Userdata <- as.data.frame(read.table("test2.txt",sep = ",",stringsAsFactors = FALSE),stringsAsFactor = FALSE)
Listingdata <- as.data.frame(read.table("test3.txt",sep = ",",stringsAsFactors = FALSE),stringsAsFactor = FALSE)
Biddata <- as.data.frame(read.table("test4.txt",sep = ",",stringsAsFactors = FALSE),stringsAsFactor = FALSE)

(bookdb = src_sqlite("~wangtianyi/Documents/Study/Database316/316-Project/bookdb.sqlite", create = TRUE))
bookdb <- dbConnect(SQLite(), dbname="bookdb.sqlite")

dbSendQuery(conn = bookdb,
            "CREATE TABLE User(
              email TEXT NOT NULL PRIMARY KEY,
              name TEXT NOT NULL,
              phone_Number TEXT NOT NULL UNIQUE,
              major TEXT, 
              CONSTRAINT email CHECK(email LIKE '%@duke.edu' OR email LIKE '%@duke.%.edu')
              );"
)

dbSendQuery(conn = bookdb,
            "CREATE TABLE Book(
              ISBN TEXT NOT NULL PRIMARY KEY,
              title TEXT NOT NULL,
              edition INTEGER NOT NULL,
              author TEXT NOT NULL
              );"
)

dbSendQuery(conn = bookdb,
            "CREATE TABLE Bid(
              bid_time INTEGER NOT NULL,
              bid_price REAL NOT NULL,
              bidder_email TEXT NOT NULL REFERENCES User(email),
              seller_email TEXT NOT NULL REFERENCES User(email),
              book_ISBN TEXT NOT NULL REFERENCES Book(ISBN),
              listing_start_time INTEGER NOT NULL REFERENCES Listing(start_time),
              PRIMARY KEY (bidder_email, bid_time, book_ISBN, seller_email, listing_start_time)
              CONSTRAINT bidPrice CHECK(bid_price >= 0)
              CONSTRAINT bidderNotSeller CHECK(NOT(bidder_email = seller_email))
              CONSTRAINT bidAfterList CHECK(bid_time > listing_start_time)
              );"
)

dbSendQuery(conn = bookdb,
            "CREATE TABLE Listing
             (start_time INTEGER NOT NULL,
              seller_email TEXT NOT NULL,
              book_ISBN TEXT NOT NULL,
              is_auction INTEGER NOT NULL,
              is_buy_it_now INTEGER NOT NULL,
              condition TEXT NOT NULL,
              description TEXT,
              start_price REAL,
              buy_it_now_price REAL,
              title TEXT NOT NULL,
              current_bid REAL,
              PRIMARY KEY(seller_email, book_ISBN, start_time)
              FOREIGN KEY(seller_email) REFERENCES Seller(email)
              FOREIGN KEY(book_ISBN) REFERENCES Book(ISBN)
              CONSTRAINT Cond CHECK(condition = 'New' OR condition = 'Likenew' OR condition = 'Used')
              CONSTRAINT IsAuc CHECK((is_auction = 1 AND start_price IS NOT NULL AND start_price >= 0) 
                                  OR (is_auction = 0 AND start_price IS NULL))
              CONSTRAINT IsBuy CHECK((is_buy_it_now = 1 AND buy_it_now_price IS NOT NULL AND buy_it_now_price >= 0) 
                                                OR (is_buy_it_now = 0 AND buy_it_now_price IS NULL))
              CONSTRAINT BuyAuc CHECK(is_auction + is_buy_it_now > 0)
              CONSTRAINT twoprice CHECK((is_auction*is_buy_it_now = 0) OR (start_price < buy_it_now_price))
              CONSTRAINT curPrice CHECK(NOT((is_auction  = 0 AND current_bid IS NOT NULL) OR (is_auction = 1 AND current_bid IS NULL)))
            )"
)


# Triggers:
#   1. Once a new record is inserted to table Listing, if it is auction, check current bid = start bid
#   if current bid is NULL or current bid != start bid, let current bid = start bid

#   2. When a new record is inserted to bid, check bid_price >= current bid + 0.01. If not, throw an error; 
#   If yes, update the current bid for the same listing in Listing table with the new high bid.

#   3. ALso, need to check new bid's listing is auction
#   4. When a new bid is inserted, the listing with buy_it_now = 1 should turn is_buy_it_now = 0

#   5. At first all users' information is invisible to other users. For example, a potential buyer cannot see any seller's information
#   we can make sellers' email address partially visible so the buyers know who post each listing. 

#   6. When the window period of 7 days for each listing has passed, delete it from the VIEW. Also,
#   if possible, send the seller an email notifying his listing has been ended (THIS FEATURE IS NOT INCLUDED IN TRIGGER)
#   Also, when the listing is ended, if the type is auction and there is at least one bid, then send an email to the seller
#   notifying him the highest bid and highest bidder's name, phone number, email and major. Also, 
#   Send the highest bidder an email notifying the seller's contact info. (THIS FEATURE IS NOT INCLUDED IN TRIGGER).

#   7. (TRIGGER NOT CREATED) Give the seller an option (on the website) of ending a listing. Once the listing is 
#   ended by the seller then deleted it from the VIEW (Which can be controlled by view definition)

#   8. (TRIGGER NOT CREATED) Give the seller an option (on the website) of relisting a listing. Once the listing
#   relisted then create a new record wit heverything the same except for set current_bid and start_time.

#   9. (TRIGGER NOT CREATED) For a listing with biy_it_now option, once a buyer has clicked Buy_it_now, then the listing will
#   be ended immediately (delete it from the VIEW), and send the seller an email notifying the seller the buyer's all
#   contact information. Send the buyer an email notifying the seller's contact info.
#   10. Check expiration periodically.
#   11, Tianyi: delete status and create a view to display.
#   12. No need to send real message, just demo, talk to machine.

dbSendQuery(conn = bookdb,
            "CREATE TRIGGER insert_listing_match_startprice_curbid AFTER INSERT ON Listing

              --Once a new record is inserted to table Listing, if it is auction, check current bid = start bid
              WHEN ((NEW.current_bid IS NULL) OR (NEW.start_price <> NEW.current_bid))
              BEGIN 
                UPDATE Listing SET current_bid = NEW.start_price WHERE seller_email = NEW.seller_email
                                                                     AND book_ISBN = NEW.book_ISBN
                                                                    AND start_time = NEW.start_time;
              END;"   
)

dbSendQuery(conn = bookdb,
            "CREATE TRIGGER insert_bid_constraint AFTER INSERT ON Bid

              --check new bid's listing is auction
              WHEN (0 = (SELECT is_auction FROM Listing WHERE seller_email = NEW.seller_email
                                                          AND book_ISBN = NEW.book_ISBN
                                                        AND start_time = NEW.listing_start_time))
              BEGIN 
                SELECT RAISE (FAIL, 'Bid is only for an auction-type listing.');
              END;   

              --check bid_price >= current bid + 0.01
              WHEN (NEW.bid_price - 0.01 < (SELECT current_bid FROM Listing WHERE seller_email = NEW.seller_email
                                                          AND book_ISBN = NEW.book_ISBN
                                                        AND start_time = NEW.listing_start_time))
              BEGIN 
                SELECT RAISE (FAIL, 'Bid should be higher than current bid price');
              END;"
)

dbSendQuery(conn = bookdb,
            "CREATE TRIGGER insert_bid_remove_buyItNow AFTER INSERT ON Bid
              
              --When a new bid is inserted, the listing with buy_it_now = 1 should turn is_buy_it_now = 0
              WHEN (1 = (SELECT is_buy_it_now FROM Listing WHERE seller_email = NEW.seller_email
                                                               AND book_ISBN = NEW.book_ISBN
                                                              AND start_time = NEW.listing_start_time))
              BEGIN 
                UPDATE Listing SET is_buy_it_now = 0, buy_it_now_price = NULL  WHERE seller_email = NEW.seller_email
                                                          AND book_ISBN = NEW.book_ISBN
                                                         AND start_time = NEW.listing_start_time;
              END;"   
)

dbSendQuery(conn = bookdb,
            "CREATE TRIGGER insert_bid_update_cur_bid AFTER INSERT ON Bid
              
              --When a new record is inserted to bid, check bid_price >= current bid + 0.01.
              --If yes, update the current bid for the same listing in Listing table with the new high bid.
              WHEN (NEW.bid_price - 0.01 >= (SELECT current_bid FROM Listing WHERE seller_email = NEW.seller_email
                                                          AND book_ISBN = NEW.book_ISBN
                                                        AND start_time = NEW.listing_start_time))
              BEGIN 
                UPDATE Listing SET current_bid = NEW.bid_price  WHERE seller_email = NEW.seller_email
                                                          AND book_ISBN = NEW.book_ISBN
                                                         AND start_time = NEW.listing_start_time;
              END;"   
)

dbRemoveTable(bookdb,"Listing")
dbRemoveTable(bookdb,"Book")
dbRemoveTable(bookdb,"User")
dbRemoveTable(bookdb,"Bid")

# dbListTables(bookdb)

dbSendQuery(conn = bookdb, "SELECT * FROM Book") %>% 
     dbFetch()


dbSendQuery(conn = bookdb, "SELECT * FROM User") %>% 
  dbFetch()

dbSendQuery(conn = bookdb, "SELECT * FROM Listing") %>% 
  dbFetch()


dbSendQuery(conn = bookdb, "SELECT * FROM Bid") %>% 
  dbFetch()


insert_book <- function(dfrow){
  dbSendQuery(conn = bookdb, paste("INSERT INTO Book VALUES ", paste0("(",paste(shQuote(as.character(dfrow)), collapse=", "),")"),sep = ""))
}

insert_user <- function(dfrow){
  dbSendQuery(conn = bookdb, paste("INSERT INTO User VALUES ", paste0("(",paste(shQuote(as.character(dfrow)), collapse=", "),")"),sep = ""))
}

insert_listing <- function(dfrow){
  dbSendQuery(conn = bookdb, paste("INSERT INTO Listing VALUES ", paste0("(",paste(shQuote(as.character(dfrow)), collapse=", "),")"),sep = ""))
}

insert_bid <- function(dfrow){
  dbSendQuery(conn = bookdb, paste("INSERT INTO Bid VALUES ", paste0("(",paste(shQuote(as.character(dfrow)), collapse=", "),")"),sep = ""))
}

apply(Bookdata,1,insert_book)
apply(Userdata,1,insert_user)
apply(Listingdata,1,insert_listing)
apply(Biddata,1,insert_bid)


#NO NEED:

# 
# dbSendQuery(conn = bookdb,
#             "CREATE INDEX index_user ON User (email);"        
# )
# 
# dbSendQuery(conn = bookdb,
#             "CREATE INDEX index_book ON Book (ISBN);"        
# )
# 
# dbSendQuery(conn = bookdb,
#             "CREATE INDEX index_bid ON Bid (bidder_email, bid_time, book_ISBN, seller_email, listing_start_time);"        
# )
# 
# dbSendQuery(conn = bookdb,
#             "CREATE INDEX index_listing ON Listing (seller_email, book_ISBN, start_time);"        
# )


# dbSendQuery(conn = bookdb,
#             "DROP TRIGGER insert_listing_match_startprice_curbid;"        
# )
# dbSendQuery(conn = bookdb,
#             "DROP TRIGGER insert_bid_constraint;  "            
# )
# dbSendQuery(conn = bookdb,
#             "DROP TRIGGER insert_bid_remove_buyItNow;  "          
# )
# dbSendQuery(conn = bookdb,
#             "DROP TRIGGER insert_bid_update_cur_bid;"          
# )
# 
('Grace.Carpenter@duke.edu', 'Grace Carpenter', '(999) 222-5021', 'African and African American Studies')

# "('72478527', 'Basic Econometrics','1','Nina Bawden')"
# 
# paste0("(",paste(shQuote(as.character(Bookdata[1,])), collapse=", "),")")
# as.character(Bookdata[1,])
# dbDisconnect(bookdb)  

# --UPDATE Bid SET bid_time = DATETIME('NOW')  WHERE bid_price = NEW.bid_price;
# dbWriteTable(conn = bookdb, name = "Book", value = "Bookdata",
#              row.names = FALSE, header = TRUE)
# 
# 
# dbSendQuery(conn = bookdb, paste("INSERT INTO Book VALUES ", paste0("(",paste(shQuote(as.character(Bookdata[1,])), collapse=", "),")"),sep = ""))
# 
# dbSendQuery(conn = bookdb, "INSERT INTO Bid VALUES (1446541320,122.4,'Claretha.Haith@duke.edu','Cindy.Hayes@duke.edu',70311366,1446483518)")








